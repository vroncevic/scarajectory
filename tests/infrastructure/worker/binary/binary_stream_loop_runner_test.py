# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_loop_runner_test.py
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
    Unit tests for BinaryStreamLoopRunner and its factory.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.worker.binary.binary_loop_runner_bundle import BinaryLoopRunnerBundle
from scarajectory.infrastructure.worker.binary.binary_stream_loop_runner import BinaryStreamLoopRunner
from scarajectory.infrastructure.worker.binary.binary_stream_loop_runner_factory import BinaryStreamLoopRunnerFactory
from scarajectory.infrastructure.worker.binary.binary_stream_runner_bundle import BinaryStreamRunnerBundle
from scarajectory.infrastructure.worker.binary.ibinary_stream_loop_runner import IBinaryStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamLoopRunnerTestCase(TestCase):
    '''
        Tests BinaryStreamLoopRunner execution and frame handling.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and loop runner.
                | test_factory_and_protocol - Tests construction and protocol adherence.
                | test_handle_incoming_bytes - Tests parsing of inbound bytes.
                | test_run_waypoints_loop - Tests waypoints loop execution.
                | test_run_program_loop - Tests binary program loop execution.
    '''

    def setUp(self) -> None:
        self.mock_flow = MagicMock()
        self.mock_strategy = MagicMock()
        self.mock_sender = MagicMock()
        self.mock_state = MagicMock()
        self.mock_state.state = StreamState.STREAMING
        self.mock_observer = MagicMock()
        self.pacing_config = StreamPacingConfig(
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )
        self.runner_bundle = BinaryStreamRunnerBundle(
            pacing_bundle=FlowPacingBundle(
                pacing_controller=self.mock_flow,
                barrier_coordinator=MagicMock(),
            ),
            packet_strategy=self.mock_strategy,
            byte_sender=self.mock_sender,
            state_controller=self.mock_state,
            observer_dispatcher=self.mock_observer,
            pacing_config=self.pacing_config,
        )
        self.runner: BinaryStreamLoopRunner = BinaryStreamLoopRunnerFactory.create(
            self.runner_bundle
        )

    def test_factory_and_protocol(self) -> None:
        '''Tests factory creation with default or injected parser and version.'''
        self.assertIsInstance(self.runner, IBinaryStreamLoopRunner)
        version: str = BinaryStreamLoopRunnerFactory.get_version()
        self.assertEqual(version, '1.0.3')

        custom_parser = BinaryFrameParserFactory.create()
        runner2 = BinaryStreamLoopRunnerFactory.create_with_parser(
            self.runner_bundle,
            custom_parser,
        )
        self.assertIsInstance(runner2, IBinaryStreamLoopRunner)

    def test_handle_incoming_bytes(self) -> None:
        '''Tests parsing of inbound bytes and stop propagation on fault.'''
        builder = BinaryFrameBuilderFactory.create()
        frame: BinaryFrame = builder.build_frame(
            msg_id=int(MessageId.RESP_ACK),
            seq_num=1,
            payload=bytes([1, 2]),
        )
        raw_bytes: bytes = builder.pack_frame(frame=frame)
        session: StreamSession = SessionFactory.create(waypoints=[])
        should_stop: bool = self.runner.handle_incoming_bytes(
            data=raw_bytes, session=session
        )
        self.assertFalse(should_stop)

        mock_fault_handler = MagicMock()
        mock_fault_handler.handle_frame.return_value = True
        fault_bundle = BinaryLoopRunnerBundle(
            step_dispatcher=MagicMock(),
            queue_drainer=MagicMock(),
            frame_parser=BinaryFrameParserFactory.create(),
            frame_handler=mock_fault_handler,
            pacing_config=self.pacing_config,
        )
        fault_runner = BinaryStreamLoopRunner(fault_bundle)
        self.assertTrue(
            fault_runner.handle_incoming_bytes(data=raw_bytes, session=session)
        )

    def test_run_waypoints_loop(self) -> None:
        '''Tests waypoints loop execution, pause, throttle, and completion.'''
        waypoints = [Waypoint(x=10.0, y=20.0, z=0.0, speed=5.0)]
        session: StreamSession = SessionFactory.create(waypoints=waypoints)
        session.done_count = 1
        stop_event: Event = Event()
        pause_event: Event = Event()
        pause_event.set()

        self.mock_flow.can_send.side_effect = [False, True]
        self.mock_strategy.format_waypoint_packet.return_value = b'\x01\x02\x03'

        with patch(
            'scarajectory.infrastructure.worker.binary.binary_stream_loop_runner.sleep'
        ) as mock_sleep:
            mock_sleep.side_effect = lambda _s: pause_event.clear()
            self.runner.run_waypoints_loop(
                session=session,
                stop_event=stop_event,
                pause_event=pause_event,
            )

        self.assertEqual(session.sent_count, 1)
        self.mock_sender.send_raw_bytes.assert_called_once_with(b'\x01\x02\x03')
        self.mock_state.set_state.assert_called_with(StreamState.COMPLETED)

    def test_run_program_loop(self) -> None:
        '''Tests binary program loop execution, pause, throttle, and completion.'''
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
            total_wire_bytes=4,
        )
        mock_step = MagicMock(spec=Step)
        mock_step.raw_bytes = b'\xAA\xBB\xCC\xDD'
        program = BinaryProgram(
            steps=(mock_step,),
            raw_bytes=b'\xAA\xBB\xCC\xDD',
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(10, 10, 0, 0),
            telemetry=telemetry,
        )
        session: StreamSession = SessionFactory.create(waypoints=[])
        session.done_count = 1
        stop_event: Event = Event()
        pause_event: Event = Event()
        pause_event.set()

        self.mock_flow.can_send.side_effect = [False, True]

        with patch(
            'scarajectory.infrastructure.worker.binary.binary_stream_loop_runner.sleep'
        ) as mock_sleep:
            mock_sleep.side_effect = lambda _s: pause_event.clear()
            self.runner.run_program_loop(
                session=session,
                program=program,
                stop_event=stop_event,
                pause_event=pause_event,
            )

        self.assertEqual(session.sent_count, 1)
        self.mock_sender.send_raw_bytes.assert_called_once_with(
            b'\xAA\xBB\xCC\xDD'
        )
        self.mock_state.set_state.assert_called_with(StreamState.COMPLETED)


if __name__ == '__main__':
    main()
