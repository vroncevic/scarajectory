# -*- coding: UTF-8 -*-

'''
Module
    stream_playback_controller_test.py
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
    Unit tests for StreamPlaybackController and StreamPlaybackControllerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import (
    BinaryFrameBuilderFactory,
)
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.state.session_factory import SessionFactory
from scarajectory.core.service.streaming.istream_playback_controller import (
    IStreamPlaybackController,
)
from scarajectory.infrastructure.barrier.flow_barrier_factory import (
    FlowBarrierFactory,
)
from scarajectory.infrastructure.connection.stream_connection_manager import (
    StreamConnectionManager,
)
from scarajectory.infrastructure.connection.stream_connection_manager_factory import (
    StreamConnectionManagerFactory,
)
from scarajectory.infrastructure.connection.stream_raw_transceiver import (
    StreamRawTransceiver,
)
from scarajectory.infrastructure.connection.stream_raw_transceiver_factory import (
    StreamRawTransceiverFactory,
)
from scarajectory.infrastructure.state.stream_state_machine import (
    StreamStateMachine,
)
from scarajectory.infrastructure.state.stream_state_machine_factory import (
    StreamStateMachineFactory,
)
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher import (
    StreamObserverDispatcher,
)
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import (
    StreamObserverDispatcherFactory,
)
from scarajectory.infrastructure.streaming.stream_control_transmitter import (
    StreamControlTransmitter,
)
from scarajectory.infrastructure.streaming.stream_control_transmitter_factory import (
    StreamControlTransmitterFactory,
)
from scarajectory.infrastructure.streaming.stream_playback_controller import (
    StreamPlaybackController,
)
from scarajectory.infrastructure.streaming.stream_playback_controller_factory import (
    StreamPlaybackControllerFactory,
)
from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.transport_factory import (
    TransportFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockExecutionWorker:
    '''Mock execution worker for testing.'''

    def __init__(self) -> None:
        self.started: bool = False
        self.paused: bool = False
        self.resumed: bool = False
        self.stopped: bool = False

    def start(self, session: StreamSession) -> None:
        '''Record start execution call.'''
        _ = session
        self.started = True

    def start_program(
        self, session: StreamSession, program: BinaryProgram
    ) -> None:
        '''Record program execution call.'''
        _ = (session, program)
        self.started = True

    def pause(self) -> None:
        '''Record pause execution call.'''
        self.paused = True

    def resume(self) -> None:
        '''Record resume execution call.'''
        self.resumed = True

    def stop(self) -> None:
        '''Record stop execution call.'''
        self.stopped = True

    def is_running(self) -> bool:
        '''Check if worker is actively executing.'''
        return self.started and not self.stopped


class StreamPlaybackControllerTest(TestCase):
    '''Unit tests for StreamPlaybackController.'''

    def setUp(self) -> None:
        transport: TransportBundle = (
            TransportFactory.create_default_transport()
        )
        self.connection: StreamConnectionManager = (
            StreamConnectionManagerFactory.create(
                transport.connection,
                protocol_mode=ProtocolMode.BINARY,
            )
        )
        barrier = FlowBarrierFactory.create()
        self.state_machine: StreamStateMachine = (
            StreamStateMachineFactory.create()
        )
        dispatcher: StreamObserverDispatcher = (
            StreamObserverDispatcherFactory.create()
        )
        self.worker: MockExecutionWorker = MockExecutionWorker()
        session: StreamSession = SessionFactory.create()
        frame_builder = BinaryFrameBuilderFactory.create()
        raw_transceiver: StreamRawTransceiver = (
            StreamRawTransceiverFactory.create(
                connection=transport.connection,
                transceiver=transport.transceiver,
            )
        )
        control_transmitter: StreamControlTransmitter = (
            StreamControlTransmitterFactory.create(
                raw_transceiver=raw_transceiver,
                frame_builder=frame_builder,
            )
        )
        self.controller: StreamPlaybackController = (
            StreamPlaybackControllerFactory.create(
                connection=self.connection,
                barrier_coordinator=barrier,
                state_machine=self.state_machine,
                dispatcher=dispatcher,
                worker=self.worker,
                control_transmitter=control_transmitter,
                session=session,
                protocol_mode=ProtocolMode.BINARY,
            )
        )

    def test_satisfies_protocol(self) -> None:
        '''Tests that controller satisfies IStreamPlaybackController.'''
        self.assertIsInstance(self.controller, IStreamPlaybackController)

    def test_start_streaming_offline_and_empty(self) -> None:
        '''Tests start streaming fails when disconnected or waypoints empty.'''
        waypoint: Waypoint = Waypoint(x=10.0, y=20.0, z=30.0, speed=50.0)
        self.assertFalse(self.controller.start_streaming([waypoint]))
        self.assertFalse(self.worker.started)
        self.connection.is_connected = MagicMock(return_value=True)
        self.assertFalse(self.controller.start_streaming([]))

    def test_online_streaming_lifecycle(self) -> None:
        '''Tests full start, pause, resume, and stop streaming lifecycle.'''
        self.connection.is_connected = MagicMock(return_value=True)
        waypoint: Waypoint = Waypoint(x=10.0, y=20.0, z=30.0, speed=50.0)
        self.assertTrue(self.controller.start_streaming([waypoint]))
        self.assertTrue(self.worker.started)
        self.assertEqual(self.state_machine.state, StreamState.STREAMING)

        self.controller.pause_streaming()
        self.assertTrue(self.worker.paused)
        self.assertEqual(self.state_machine.state, StreamState.PAUSED)

        self.controller.resume_streaming()
        self.assertTrue(self.worker.resumed)
        self.assertEqual(self.state_machine.state, StreamState.STREAMING)

        self.controller.stop_streaming()
        self.assertTrue(self.worker.stopped)
        self.assertEqual(self.state_machine.state, StreamState.STOPPED)

    def test_factory_get_version(self) -> None:
        '''Tests factory get_version.'''
        self.assertEqual(
            StreamPlaybackControllerFactory.get_version(), __version__
        )


if __name__ == '__main__':
    main()
