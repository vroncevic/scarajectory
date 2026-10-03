# -*- coding: UTF-8 -*-

'''
Module
    transport_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scarajectory is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scarajectory is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for StreamTransport, TransportFactory, FlowController, StreamPipelineAssembler, and ConnectionRepository.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.core.service.connection.iconnection import IConnection
from scarajectory.core.service.connection.iraw_channel import IRawChannel
from scarajectory.core.service.preferences.connection_preference_factory import ConnectionPreferenceFactory
from scarajectory.core.service.state.session_factory import SessionFactory
from scarajectory.core.service.streaming.ibinary_program_streamer import IBinaryProgramStreamer
from scarajectory.core.service.streaming.istream_dispatcher import IStreamDispatcher
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.preferences.connection_repository_factory import ConnectionRepositoryFactory
from scarajectory.infrastructure.state.stream_state_machine import StreamStateMachine
from scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler import StreamPipelineAssembler
from scarajectory.infrastructure.streaming.bundle import StreamingBundle
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.istream_transport_transceiver import IStreamTransportTransceiver
from scarajectory.infrastructure.transport.transport_factory import TransportFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransport(TestCase):
    '''
        Test cases for Transport layers, FlowController, and streaming pipeline lifecycle.

        It defines:

            :methods:
                | test_serial_transport_initial_state - Tests default properties of SerialTransport.
                | test_tcp_transport_initial_state - Tests default properties of TcpTransport.
                | test_transport_factory - Tests factory creating SerialTransport and TcpTransport.
                | test_flow_controller - Tests sliding window queue capacity and ack processing.
                | test_stream_pipeline_lifecycle - Tests StreamPipelineAssembler creation and control flags.
                | test_stream_pipeline_structural_subtyping - Tests StreamPipelineAssembler contracts.
                | test_connection_repository - Tests storing and loading connection preferences.
                | test_stream_state_machine - Tests StreamStateMachine transitions and active queries.
                | test_stream_observer_dispatcher - Tests StreamObserverDispatcher logging and progress.
    '''

    def test_serial_transport_initial_state(self) -> None:
        '''
            Tests initial state of SerialTransport.

            :exceptions: None.
        '''
        bundle = TransportFactory.create_default_transport()
        self.assertIsInstance(bundle, TransportBundle)
        self.assertFalse(bundle.connection.is_connected())
        bundle.connection.disconnect()
        self.assertFalse(bundle.connection.is_connected())

    def test_tcp_transport_initial_state(self) -> None:
        '''
            Tests initial state of TcpTransport.

            :exceptions: None.
        '''
        bundle = TransportFactory.create_transport('192.168.1.1:8080')
        self.assertIsInstance(bundle, TransportBundle)
        self.assertFalse(bundle.connection.is_connected())
        bundle.connection.disconnect()
        self.assertFalse(bundle.connection.is_connected())

    def test_transport_factory(self) -> None:
        '''
            Tests TransportFactory resolving transports based on endpoint format.

            :exceptions: None.
        '''
        serial_dev = TransportFactory.create_transport('/dev/ttyACM0')
        self.assertIsInstance(serial_dev, TransportBundle)
        self.assertIsInstance(
            serial_dev.connection, IStreamTransportConnection
        )
        self.assertIsInstance(
            serial_dev.transceiver, IStreamTransportTransceiver
        )
        self.assertEqual(serial_dev.transceiver.channel_name(), 'Serial')

        tcp_dev = TransportFactory.create_transport('192.168.1.50:8888')
        self.assertIsInstance(tcp_dev, TransportBundle)
        self.assertIsInstance(
            tcp_dev.connection, IStreamTransportConnection
        )
        self.assertIsInstance(
            tcp_dev.transceiver, IStreamTransportTransceiver
        )
        self.assertEqual(tcp_dev.transceiver.channel_name(), 'TCP')

        tcp_scheme = TransportFactory.create_transport('tcp://10.0.0.1:5000')
        self.assertIsInstance(tcp_scheme, TransportBundle)
        self.assertIsInstance(
            tcp_scheme.connection, IStreamTransportConnection
        )
        self.assertIsInstance(
            tcp_scheme.transceiver, IStreamTransportTransceiver
        )
        self.assertEqual(tcp_scheme.transceiver.channel_name(), 'TCP')

    def test_flow_controller(self) -> None:
        '''
            Tests sliding window flow controller queue tracking and acknowledgments.

            :exceptions: None.
        '''
        barrier = FlowBarrierFactory.create()
        bundle = FlowPacingBundleFactory.create(barrier=barrier, capacity=16)
        pacing = bundle.pacing_controller
        barrier_coord = bundle.barrier_coordinator
        session = SessionFactory.create()
        self.assertTrue(pacing.can_send(session))

        session.remote_queue_depth = 16
        self.assertFalse(pacing.can_send(session))

        pacing.process_response('<ACK QUEUE=5>', session)
        self.assertEqual(session.remote_queue_depth, 5)
        self.assertTrue(pacing.can_send(session))

        barrier_coord.set_barrier()
        self.assertFalse(pacing.can_send(session))
        barrier_coord.clear_barrier()
        self.assertTrue(pacing.can_send(session))

        self.assertTrue(barrier_coord.is_barrier_clear())
        barrier_coord.set_barrier()
        self.assertFalse(barrier_coord.is_barrier_clear())
        barrier_coord.clear_barrier()
        self.assertTrue(barrier_coord.is_barrier_clear())

    def test_stream_pipeline_lifecycle(self) -> None:
        '''
            Tests StreamPipelineAssembler creation and playback control lifecycle.

            :exceptions: None.
        '''
        transport = TransportFactory.create_default_transport()
        bundle = StreamPipelineAssembler.assemble(transport=transport)
        self.assertFalse(bundle.connection.is_connected())

        bundle.playback_controller.pause_streaming()
        bundle.playback_controller.resume_streaming()
        bundle.playback_controller.stop_streaming()

    def test_stream_pipeline_structural_subtyping(self) -> None:
        '''
            Tests that StreamPipelineAssembler satisfies fine-grained streaming contracts.

            :exceptions: None.
        '''
        transport = TransportFactory.create_default_transport()
        bundle = StreamPipelineAssembler.assemble(transport=transport)

        self.assertIsInstance(bundle, StreamingBundle)
        self.assertIsInstance(bundle.connection, IConnection)
        self.assertIsInstance(bundle.raw_channel, IRawChannel)
        self.assertIsInstance(bundle.playback_controller, IStreamPlaybackController)
        self.assertIsInstance(bundle.dispatcher, IStreamDispatcher)
        self.assertIsInstance(bundle.binary_streamer, IBinaryProgramStreamer)

    def test_connection_repository(self) -> None:
        '''
            Tests persistence and retrieval of connection preferences.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_device.json'
            context_bundle = ContextBundleFactory.create_bundle()
            repo = ConnectionRepositoryFactory.create_with_path(
                context_bundle=context_bundle,
                config_file=config_file,
            )

            self.assertFalse(repo.has_preference())
            pref = repo.load_preference()
            self.assertEqual(pref.port, ConnectionPreferenceFactory.DEFAULT_PORT)
            self.assertEqual(pref.baud, ConnectionPreferenceFactory.DEFAULT_BAUD)

            saved = repo.save_preference(
                ConnectionPreferenceFactory.create(port='/dev/ttyUSB0', baud=115200)
            )
            self.assertTrue(saved)
            self.assertTrue(repo.has_preference())

            loaded_pref = repo.load_preference()
            self.assertEqual(loaded_pref.port, '/dev/ttyUSB0')
            self.assertEqual(loaded_pref.baud, 115200)

            # Test invalid port rejection
            self.assertFalse(
                repo.save_preference(
                    ConnectionPreferenceFactory.create(port='', baud=115200)
                )
            )
            self.assertFalse(
                repo.save_preference(
                    ConnectionPreferenceFactory.create(port='Virtual / None', baud=115200)
                )
            )

            # Test updating preference directly on repository
            self.assertTrue(
                repo.save_preference(
                    ConnectionPreferenceFactory.create(port='/dev/ttyUSB1', baud=9600)
                )
            )
            pref2 = repo.load_preference()
            self.assertEqual(pref2.port, '/dev/ttyUSB1')
            self.assertEqual(pref2.baud, 9600)

    def test_stream_state_machine(self) -> None:
        '''
            Tests StreamStateMachine transitions and active queries.
        '''
        sm = StreamStateMachine()
        self.assertEqual(sm.state, StreamState.IDLE)
        self.assertFalse(sm.is_active())

        self.assertTrue(sm.transition_to(StreamState.STREAMING))
        self.assertEqual(sm.state, StreamState.STREAMING)
        self.assertTrue(sm.is_active())

        self.assertFalse(sm.transition_to(StreamState.STREAMING))

        self.assertTrue(sm.transition_to(StreamState.PAUSED))
        self.assertTrue(sm.is_active())

        sm.reset()
        self.assertEqual(sm.state, StreamState.IDLE)
        self.assertFalse(sm.is_active())

    def test_stream_observer_dispatcher(self) -> None:
        '''
            Tests StreamObserverDispatcher logging and progress calculation.
        '''
        class DummyObserver:
            '''Dummy observer for testing dispatcher notifications.'''
            def __init__(self) -> None:
                self.logs: list[tuple[str, bool]] = []
                self.progresses: list[StreamProgress] = []

            def on_stream_progress(self, progress: StreamProgress) -> None:
                '''Record stream progress updates.'''
                self.progresses.append(progress)

            def on_serial_log(self, msg: str, is_outgoing: bool = False) -> None:
                '''Record serial log messages.'''
                self.logs.append((msg, is_outgoing))

        observer = DummyObserver()
        dispatcher = StreamObserverDispatcherFactory.create_with_observer(observer)
        self.assertTrue(dispatcher.has_observers())

        dispatcher.notify_log('Test message', is_outgoing=True)
        self.assertEqual(len(observer.logs), 1)
        self.assertEqual(observer.logs[0], ('Test message', True))

        session = SessionFactory.create()
        dispatcher.notify_progress(state=StreamState.IDLE, session=session)
        self.assertEqual(len(observer.progresses), 1)
        self.assertEqual(observer.progresses[0].percentage, 0.0)


if __name__ == '__main__':
    main()
