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
    Unit tests for SerialTransport, TcpTransport, TransportFactory, FlowController, TrajectoryStreamer, and ConnectionRepository.
'''

from __future__ import annotations

from os.path import abspath, dirname
from pathlib import Path
from sys import path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.core.service.communication.stream.session_factory import SessionFactory
from scarajectory.core.service.communication.controller.irobot_controller import IRobotController
from scarajectory.core.service.communication.stream.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.core.model.communication.preferences.connection_preference import ConnectionPreference
from scarajectory.core.service.communication.preferences.connection_preference_factory import ConnectionPreferenceFactory
from scarajectory.infrastructure.communication.preferences.connection_repository import ConnectionRepository
from scarajectory.infrastructure.communication.preferences.connection_repository_factory import ConnectionRepositoryFactory
from scarajectory.infrastructure.communication.streamer.flow_controller_factory import FlowControllerFactory
from scarajectory.infrastructure.communication.controller.robot_controller_factory import RobotControllerFactory
from scarajectory.core.model.communication.stream.stream_state import StreamState
from scarajectory.core.model.communication.stream.stream_progress import StreamProgress
from scarajectory.infrastructure.communication.streamer.stream_state_machine import StreamStateMachine
from scarajectory.infrastructure.communication.streamer.stream_observer_dispatcher import StreamObserverDispatcher
from scarajectory.infrastructure.communication.streamer.trajectory_streamer_factory import TrajectoryStreamerFactory
from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport
from scarajectory.infrastructure.communication.transport.tcp_transport import TcpTransport
from scarajectory.infrastructure.communication.transport.transport_factory import TransportFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransport(TestCase):
    '''
        Test cases for Transport layers, FlowController, and Streamer lifecycle.

        It defines:

            :methods:
                | test_serial_transport_initial_state - Tests default properties of SerialTransport.
                | test_tcp_transport_initial_state - Tests default properties of TcpTransport.
                | test_transport_factory - Tests factory creating SerialTransport and TcpTransport.
                | test_flow_controller - Tests sliding window queue capacity and ack processing.
                | test_streamer_lifecycle - Tests SerialStreamer creation and control flags.
                | test_streamer_structural_subtyping - Tests TrajectoryStreamer implements protocols.
                | test_streamer_semantic_commands - Tests semantic robot command dispatching.
                | test_connection_repository - Tests storing and loading connection preferences.
    '''

    def test_serial_transport_initial_state(self) -> None:
        '''
            Tests initial state of SerialTransport.

            :exceptions: None.
        '''
        transport = SerialTransport()
        self.assertFalse(transport.is_connected())
        transport.disconnect()
        self.assertFalse(transport.is_connected())

    def test_tcp_transport_initial_state(self) -> None:
        '''
            Tests initial state of TcpTransport.

            :exceptions: None.
        '''
        transport = TcpTransport()
        self.assertFalse(transport.is_connected())
        transport.disconnect()
        self.assertFalse(transport.is_connected())

    def test_transport_factory(self) -> None:
        '''
            Tests TransportFactory resolving transports based on endpoint format.

            :exceptions: None.
        '''
        serial_dev = TransportFactory.create_transport('/dev/ttyACM0')
        self.assertIsInstance(serial_dev, SerialTransport)

        tcp_dev = TransportFactory.create_transport('192.168.1.50:8888')
        self.assertIsInstance(tcp_dev, TcpTransport)

        tcp_scheme = TransportFactory.create_transport('tcp://10.0.0.1:5000')
        self.assertIsInstance(tcp_scheme, TcpTransport)

    def test_flow_controller(self) -> None:
        '''
            Tests sliding window flow controller queue tracking and acknowledgments.

            :exceptions: None.
        '''
        fc = FlowControllerFactory.create(capacity=16)
        session = SessionFactory.create()
        self.assertTrue(fc.can_send(session))

        session.remote_queue_depth = 16
        self.assertFalse(fc.can_send(session))

        fc.process_response('<ACK QUEUE=5>', session)
        self.assertEqual(session.remote_queue_depth, 5)
        self.assertTrue(fc.can_send(session))

        fc.set_barrier()
        self.assertFalse(fc.can_send(session))
        fc.clear_barrier()
        self.assertTrue(fc.can_send(session))

    def test_streamer_lifecycle(self) -> None:
        '''
            Tests SerialStreamer creation and control flags.

            :exceptions: None.
        '''
        transport = SerialTransport()
        streamer = TrajectoryStreamerFactory.create(transport=transport)
        self.assertFalse(streamer.is_connected())

        streamer.pause_streaming()
        streamer.resume_streaming()
        streamer.stop_streaming()

    def test_streamer_structural_subtyping(self) -> None:
        '''
            Tests that TrajectoryStreamer satisfies ITrajectoryStreamer and RobotController satisfies IRobotController.

            :exceptions: None.
        '''
        transport = SerialTransport()
        streamer = TrajectoryStreamerFactory.create(transport=transport)

        self.assertIsInstance(streamer, ITrajectoryStreamer)
        self.assertIsInstance(streamer.get_robot_controller(), IRobotController)

    def test_streamer_semantic_commands(self) -> None:
        '''
            Tests executing semantic robot controller methods when disconnected.

            :exceptions: None.
        '''
        transport = SerialTransport()
        streamer = TrajectoryStreamerFactory.create(transport=transport)
        ctrl = streamer.get_robot_controller()

        self.assertFalse(ctrl.home())
        self.assertFalse(ctrl.enable())
        self.assertFalse(ctrl.disable())
        self.assertFalse(ctrl.set_feedrate_override(120))
        self.assertFalse(ctrl.set_vacuum_pump(True))
        self.assertFalse(ctrl.pulse_purge_valve())
        self.assertFalse(ctrl.jog('X', 10.0))
        self.assertFalse(ctrl.query_status())
        self.assertFalse(ctrl.query_position())

    def test_robot_controller_standalone(self) -> None:
        '''
            Tests dedicated RobotController component against IRobotController contract.

            :exceptions: None.
        '''
        transport = SerialTransport()
        streamer = TrajectoryStreamerFactory.create(transport=transport)
        controller = RobotControllerFactory.create(streamer)

        self.assertIsInstance(controller, IRobotController)
        self.assertFalse(controller.is_connected())
        self.assertFalse(controller.home())
        self.assertFalse(controller.enable())
        self.assertFalse(controller.disable())
        self.assertFalse(controller.set_feedrate_override(100))
        self.assertFalse(controller.set_vacuum_pump(True))
        self.assertFalse(controller.pulse_purge_valve())
        self.assertFalse(controller.set_valve(True))
        self.assertFalse(controller.jog('X', 5.0))
        self.assertFalse(controller.query_status())
        self.assertFalse(controller.query_position())

    def test_connection_repository(self) -> None:
        '''
            Tests persistence and retrieval of connection preferences.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_device.json'
            context_bundle = ContextBundleFactory.create_bundle()
            repo = ConnectionRepositoryFactory.create(context_bundle=context_bundle)
            repo._config_file = config_file

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
            def __init__(self) -> None:
                self.logs: list[str] = []
                self.progresses: list[StreamProgress] = []

            def on_stream_progress(self, progress: StreamProgress) -> None:
                self.progresses.append(progress)

            def on_serial_log(self, msg: str, is_outgoing: bool = False) -> None:
                self.logs.append(msg)

        observer = DummyObserver()
        dispatcher = StreamObserverDispatcher(observer)
        self.assertTrue(dispatcher.has_observer())

        dispatcher.notify_log('Test message', is_outgoing=True)
        self.assertEqual(len(observer.logs), 1)
        self.assertEqual(observer.logs[0], 'Test message')

        session = SessionFactory.create()
        dispatcher.notify_progress(state=StreamState.IDLE, session=session)
        self.assertEqual(len(observer.progresses), 1)
        self.assertEqual(observer.progresses[0].percentage, 0.0)


if __name__ == '__main__':
    main()

