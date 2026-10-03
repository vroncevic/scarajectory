# -*- coding: UTF-8 -*-

'''
Module
    binary_program_streamer_test.py
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
    Unit tests for BinaryProgramStreamer and BinaryProgramStreamerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.binary_program_telemetry import (
    BinaryProgramTelemetry,
)
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.service.state.session_factory import SessionFactory
from scarajectory.core.service.streaming.ibinary_program_streamer import (
    IBinaryProgramStreamer,
)
from scarajectory.infrastructure.connection.stream_connection_manager_factory import (
    StreamConnectionManagerFactory,
)
from scarajectory.infrastructure.state.stream_state_machine_factory import (
    StreamStateMachineFactory,
)
from scarajectory.infrastructure.streaming.binary_program_streamer_factory import (
    BinaryProgramStreamerFactory,
)
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import (
    StreamObserverDispatcherFactory,
)
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
        self.stopped: bool = False

    def start(self, session: StreamSession) -> None:
        '''Start execution worker.'''
        _ = session
        self.started = True

    def start_program(
        self, session: StreamSession, program: BinaryProgram
    ) -> None:
        '''Start execution worker with binary program.'''
        _ = (session, program)
        self.started = True

    def pause(self) -> None:
        '''Pause execution worker.'''

    def resume(self) -> None:
        '''Resume execution worker.'''

    def stop(self) -> None:
        '''Stop execution worker.'''
        self.stopped = True

    def is_running(self) -> bool:
        '''Check if worker is running.'''
        return self.started and not self.stopped


class MockFallbackExecutionWorker:
    '''Mock execution worker lacking start_program method.'''

    def __init__(self) -> None:
        self.started: bool = False

    def start(self, session: StreamSession) -> None:
        '''Start execution worker.'''
        _ = session
        self.started = True

    def stop(self) -> None:
        '''Stop execution worker.'''


class BinaryProgramStreamerTest(TestCase):
    '''Unit tests for BinaryProgramStreamer.'''

    def setUp(self) -> None:
        transport = TransportFactory.create_default_transport()
        self.connection = StreamConnectionManagerFactory.create(
            transport.connection,
            protocol_mode=ProtocolMode.BINARY,
        )
        self.state_machine = StreamStateMachineFactory.create()
        self.dispatcher = StreamObserverDispatcherFactory.create()
        self.worker = MockExecutionWorker()
        self.session = SessionFactory.create()
        self.streamer = BinaryProgramStreamerFactory().create(
            connection=self.connection,
            state_machine=self.state_machine,
            dispatcher=self.dispatcher,
            worker=self.worker,
            session=self.session,
        )

    def test_satisfies_protocol(self) -> None:
        '''Tests that streamer satisfies IBinaryProgramStreamer.'''
        self.assertIsInstance(self.streamer, IBinaryProgramStreamer)

    def test_stream_binary_program_offline(self) -> None:
        '''Tests stream_binary_program fails when offline.'''
        telemetry = BinaryProgramTelemetry(
            source_instructions=0,
            compiled_steps=0,
            duration_us=0,
            duration_s=0.0,
            peak_j1_steps=0,
            peak_j2_steps=0,
            peak_z_steps=0,
            peak_j4_steps=0,
            total_wire_bytes=0,
        )
        program = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=(0, 0, 0, 0),
            telemetry=telemetry,
        )
        self.assertFalse(self.streamer.stream_binary_program(program))

    def test_stream_binary_program_connected_empty_steps(self) -> None:
        '''Tests stream_binary_program returns False when connected but steps empty.'''
        telemetry = BinaryProgramTelemetry(
            source_instructions=0,
            compiled_steps=0,
            duration_us=0,
            duration_s=0.0,
            peak_j1_steps=0,
            peak_j2_steps=0,
            peak_z_steps=0,
            peak_j4_steps=0,
            total_wire_bytes=0,
        )
        program = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=(0, 0, 0, 0),
            telemetry=telemetry,
        )
        self.connection.is_connected = MagicMock(return_value=True)
        self.assertFalse(self.streamer.stream_binary_program(program))

    def test_stream_binary_program_online_success(self) -> None:
        '''Tests stream_binary_program succeeds when connected with valid steps.'''
        telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=1,
            duration_us=1000,
            duration_s=0.001,
            peak_j1_steps=10,
            peak_j2_steps=10,
            peak_z_steps=0,
            peak_j4_steps=0,
            total_wire_bytes=16,
        )
        mock_step = MagicMock(spec=Step)
        program = BinaryProgram(
            steps=(mock_step,),
            raw_bytes=b'\x01' * 16,
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(10, 10, 0, 0),
            telemetry=telemetry,
        )
        self.connection.is_connected = MagicMock(return_value=True)
        self.assertTrue(self.streamer.stream_binary_program(program))
        self.assertTrue(self.worker.started)
        self.assertTrue(self.streamer.is_streaming())

    def test_stream_binary_program_fallback_worker(self) -> None:
        '''Tests stream_binary_program uses worker.start when start_program absent.'''
        fallback_worker = MockFallbackExecutionWorker()
        streamer = BinaryProgramStreamerFactory().create(
            connection=self.connection,
            state_machine=self.state_machine,
            dispatcher=self.dispatcher,
            worker=fallback_worker,
            session=self.session,
        )
        telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=1,
            duration_us=1000,
            duration_s=0.001,
            peak_j1_steps=10,
            peak_j2_steps=10,
            peak_z_steps=0,
            peak_j4_steps=0,
            total_wire_bytes=16,
        )
        mock_step = MagicMock(spec=Step)
        program = BinaryProgram(
            steps=(mock_step,),
            raw_bytes=b'\x01' * 16,
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(10, 10, 0, 0),
            telemetry=telemetry,
        )
        self.connection.is_connected = MagicMock(return_value=True)
        self.assertTrue(streamer.stream_binary_program(program))
        self.assertTrue(fallback_worker.started)

    def test_is_streaming(self) -> None:
        '''Tests is_streaming returns state machine active status.'''
        self.assertFalse(self.streamer.is_streaming())

    def test_factory_get_version(self) -> None:
        '''Tests factory get_version.'''
        self.assertEqual(
            BinaryProgramStreamerFactory().get_version(), __version__
        )


if __name__ == '__main__':
    main()
