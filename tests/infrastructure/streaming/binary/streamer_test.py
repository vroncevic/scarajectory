# -*- coding: UTF-8 -*-

'''
Module
    streamer_test.py
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
    Unit testing for BinaryStreamer.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import BinaryStep, JointStepCoordinates

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.streaming.binary.dependencies import BinaryDependencies
from scarajectory.infrastructure.streaming.binary.istreamer import IBinaryStreamer
from scarajectory.infrastructure.streaming.binary.streamer import BinaryStreamer
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryStreamer(TestCase):
    '''
        Test cases verifying BinaryStreamer compiled bytecode execution.

        It defines:

            :methods:
                | setUp - Prepares mock collaborators and BinaryStreamer instance.
                | test_satisfies_protocol - Verifies IBinaryStreamer structural contract.
                | test_stream_binary_program_disconnected - Verifies failure when offline.
                | test_stream_binary_program_empty_steps - Verifies failure when program empty.
                | test_stream_binary_program_success - Verifies worker start and state transition.
                | test_is_streaming - Verifies is_streaming delegates to state machine.
    '''

    def setUp(self) -> None:
        '''
            Prepares mock collaborators and BinaryStreamer instance.

            :exceptions: None.
        '''
        self.connection_manager = MagicMock(spec=IConnectionManager)
        self.state_machine = MagicMock(spec=IStreamStateMachine)
        self.dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        self.worker = MagicMock(spec=IExecutionWorker)
        self.session = SessionFactory.create_default()

        self.streamer = BinaryStreamer(
            dependencies=BinaryDependencies(
                connection_manager=self.connection_manager,
                stream_state_machine=self.state_machine,
                stream_observer_dispatcher=self.dispatcher,
                execution_worker=self.worker,
                session=self.session,
            )
        )

        telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=1,
            duration_us=1000,
            duration_s=0.001,
            peak_steps=AxisPeakSteps(
                peak_j1_steps=10,
                peak_j2_steps=10,
                peak_z_steps=0,
                peak_j4_steps=0,
            ),
            total_wire_bytes=16,
        )
        mock_step = MagicMock(spec=BinaryStep)
        self.program = BinaryProgram(
            steps=(mock_step,),
            raw_bytes=b'\x01' * 16,
            total_duration_us=1000,
            instruction_count=1,
            step_counts=JointStepCoordinates(j1=10, j2=10, z=0, j4=0),
            telemetry=telemetry,
        )

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies IBinaryStreamer structural contract.

            :exceptions: None.
        '''
        self.assertIsInstance(self.streamer, IBinaryStreamer)

    def test_stream_binary_program_disconnected(self) -> None:
        '''
            Verifies failure when offline.

            :exceptions: None.
        '''
        self.connection_manager.is_connected.return_value = False
        result: bool = self.streamer.stream_binary_program(self.program)
        self.assertFalse(result)
        self.dispatcher.notify_log.assert_called_with(
            '[ERR]: Cannot stream - Transport not connected'
        )

    def test_stream_binary_program_empty_steps(self) -> None:
        '''
            Verifies failure when program empty.

            :exceptions: None.
        '''
        self.connection_manager.is_connected.return_value = True
        telemetry = BinaryProgramTelemetry(
            source_instructions=0,
            compiled_steps=0,
            duration_us=0,
            duration_s=0.0,
            peak_steps=AxisPeakSteps(
                peak_j1_steps=0,
                peak_j2_steps=0,
                peak_z_steps=0,
                peak_j4_steps=0,
            ),
            total_wire_bytes=0,
        )
        empty_program = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
            telemetry=telemetry,
        )
        result: bool = self.streamer.stream_binary_program(empty_program)
        self.assertFalse(result)

    def test_stream_binary_program_success(self) -> None:
        '''
            Verifies worker start and state transition.

            :exceptions: None.
        '''
        self.connection_manager.is_connected.return_value = True
        self.worker.start_program = MagicMock()
        result: bool = self.streamer.stream_binary_program(self.program)
        self.assertTrue(result)
        self.state_machine.transition_to.assert_called_with(
            StreamState.STREAMING
        )
        self.worker.start_program.assert_called_once()
        self.dispatcher.notify_progress.assert_called_once()

    def test_is_streaming(self) -> None:
        '''
            Verifies is_streaming delegates to state machine.

            :exceptions: None.
        '''
        self.state_machine.is_active.return_value = True
        self.assertTrue(self.streamer.is_streaming())
        self.state_machine.is_active.return_value = False
        self.assertFalse(self.streamer.is_streaming())


if __name__ == '__main__':
    main()
