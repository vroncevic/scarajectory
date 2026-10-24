# -*- coding: UTF-8 -*-

'''
Module
    runner_test.py
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
    Unit tests for StreamLoopRunner implementation.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.service.protocol.iparser import IBinaryFrameParser

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.worker.dispatcher.idispatcher import IStepDispatcher
from scarajectory.infrastructure.worker.drainer.idrainer import IQueueDrainer
from scarajectory.infrastructure.worker.handler.ihandler import IStreamFrameHandler
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner
from scarajectory.infrastructure.worker.runner.loop_bundle import LoopRunnerBundle
from scarajectory.infrastructure.worker.runner.runner import StreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamLoopRunnerTestCase(TestCase):
    '''
        Unit tests for StreamLoopRunner.

        It defines:

            :methods:
                | setUp - Prepares test runner and mock collaborators.
                | test_structural_conformance - Verifies conformance to IStreamLoopRunner.
                | test_run_waypoints_loop - Verifies waypoints stream loop execution.
                | test_run_program_loop - Verifies compiled binary steps loop execution.
                | test_handle_incoming_bytes - Verifies bytes parsing and frame handling.
    '''

    def setUp(self) -> None:
        '''
            Prepares loop runner and mock collaborators.

            :exceptions: None.
        '''
        self.mock_disp = MagicMock(spec=IStepDispatcher)
        self.mock_drain = MagicMock(spec=IQueueDrainer)
        self.mock_parser = MagicMock(spec=IBinaryFrameParser)
        self.mock_handler = MagicMock(spec=IStreamFrameHandler)
        self.config = StreamPacingConfig(
            poll_delay=0.001,
            send_delay=0.001,
            throttle_delay=0.001,
        )

        bundle = LoopRunnerBundle(
            step_dispatcher=self.mock_disp,
            queue_drainer=self.mock_drain,
            frame_parser=self.mock_parser,
            frame_handler=self.mock_handler,
            pacing_config=self.config,
        )
        self.runner = StreamLoopRunner(bundle)

    def test_structural_conformance(self) -> None:
        '''
            Verifies runner satisfies IStreamLoopRunner structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.runner, IStreamLoopRunner)

    def test_run_waypoints_loop(self) -> None:
        '''
            Verifies waypoints execution loop calls dispatch and drain.

            :exceptions: None.
        '''
        wp = TrajectoryWaypoint(
            x=0.0, y=0.0, z=0.0, phi=0.0, speed=10.0, name='P1', command='G1'
        )
        session = StreamSession(
            waypoints=[wp],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )
        self.mock_disp.can_dispatch_step.side_effect = [False, True]

        def advance(s: StreamSession) -> None:
            s.sent_count = 1

        self.mock_disp.dispatch_waypoint.side_effect = advance
        stop_event = Event()
        pause_event = Event()
        pause_event.set()

        def unpause(_delay: float) -> None:
            pause_event.clear()

        with patch('scarajectory.infrastructure.worker.runner.runner.sleep', side_effect=unpause):
            self.runner.run_waypoints_loop(
                session=session,
                stop_event=stop_event,
                pause_event=pause_event,
            )

        self.mock_disp.dispatch_waypoint.assert_called_once_with(session)
        self.mock_drain.drain_queue.assert_called_once()

    def test_run_program_loop(self) -> None:
        '''
            Verifies binary program steps execution loop.

            :exceptions: None.
        '''
        mock_step = MagicMock(spec=BinaryStep)
        mock_program = MagicMock(spec=BinaryProgram)
        mock_program.steps = (mock_step,)

        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )
        self.mock_disp.can_dispatch_step.side_effect = [False, True]

        def advance(*, session: StreamSession, step: BinaryStep) -> None:
            if step is not None:
                session.sent_count = 1

        self.mock_disp.dispatch_binary_step.side_effect = advance
        stop_event = Event()
        pause_event = Event()
        pause_event.set()

        def unpause(_delay: float) -> None:
            pause_event.clear()

        with patch('scarajectory.infrastructure.worker.runner.runner.sleep', side_effect=unpause):
            self.runner.run_program_loop(
                session=session,
                program=mock_program,
                stop_event=stop_event,
                pause_event=pause_event,
            )

        self.mock_disp.dispatch_binary_step.assert_called_once()
        self.mock_drain.drain_queue.assert_called_once()

    def test_handle_incoming_bytes(self) -> None:
        '''
            Verifies feed_bytes and frame dispatching flow.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=1,
            done_count=0,
            failed_count=0,
            remote_queue_depth=1,
            start_time=100.0,
        )
        frame = BinaryFrame(msg_id=1, seq_num=1, payload=b'', crc16=0)
        self.mock_parser.feed_bytes.return_value = (frame,)
        self.mock_handler.handle_frame.return_value = True

        result = self.runner.handle_incoming_bytes(
            data=b'\x01',
            session=session,
        )
        self.assertTrue(result)
        self.mock_parser.feed_bytes.assert_called_once_with(b'\x01')
        self.mock_handler.handle_frame.assert_called_once_with(frame, session)


if __name__ == '__main__':
    main()
