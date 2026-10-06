# -*- coding: UTF-8 -*-

'''
Module
    stream_loop_runner_test.py
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
    Unit tests for StreamLoopRunner and StreamLoopRunnerFactory.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import patch

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.worker.ascii.istream_loop_runner import IStreamLoopRunner
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.state.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.worker.ascii.stream_loop_runner import StreamLoopRunner
from scarajectory.infrastructure.worker.ascii.stream_loop_runner_factory import StreamLoopRunnerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockCommandSender:
    '''
        Mock command sender recording sent raw command strings.
    '''

    def __init__(self) -> None:
        self.sent_commands: list[str] = []

    def send_raw_command(self, command: str) -> None:
        '''
            Records transmitted command string.

            :param command: Command string.
        '''
        self.sent_commands.append(command)


class TestStreamLoopRunner(TestCase):
    '''
        Test cases for StreamLoopRunner and StreamLoopRunnerFactory.

        It defines:

            :methods:
                | setUp - Initializes common dependencies for tests.
                | test_stream_loop_runner_protocol - Protocol conformance.
                | test_handle_incoming_line_normal - Response ingestion normal.
                | test_handle_incoming_line_fatal - Response ingestion fatal.
                | test_run_loop_execution - Loop waypoint transmission.
                | test_stream_loop_runner_factory - Factory construction.
    '''

    def setUp(self) -> None:
        '''
            Initializes common dependencies for tests.
        '''
        barrier = FlowBarrierFactory.create()
        self.pacing_bundle: FlowPacingBundle = FlowPacingBundleFactory.create(
            barrier=barrier
        )
        self.state_controller = StreamStateMachineFactory.create()
        self.observer_dispatcher = StreamObserverDispatcherFactory.create()
        self.command_sender = MockCommandSender()
        self.pacing_config = StreamPacingConfig(
            poll_delay=0.001,
            send_delay=0.001,
            throttle_delay=0.001,
        )
        self.runner = StreamLoopRunnerFactory.create(
            pacing_bundle=self.pacing_bundle,
            command_sender=self.command_sender,
            state_controller=self.state_controller,
            observer_dispatcher=self.observer_dispatcher,
            pacing_config=self.pacing_config,
        )

    def test_stream_loop_runner_protocol(self) -> None:
        '''
            Verifies that StreamLoopRunner satisfies IStreamLoopRunner.
        '''
        self.assertIsInstance(self.runner, IStreamLoopRunner)

    def test_handle_incoming_line_normal(self) -> None:
        '''
            Verifies response ingestion for normal response lines.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=10.0, z=0.0, speed=50.0)],
            sent_count=1,
            done_count=0,
            failed_count=0,
            remote_queue_depth=1,
            start_time=0.0,
        )

        should_stop = self.runner.handle_incoming_line(
            '<RESP:ACK#1:QUEUE=0>', session=session
        )
        self.assertFalse(should_stop)
        self.assertEqual(session.remote_queue_depth, 0)

    def test_handle_incoming_line_fatal(self) -> None:
        '''
            Verifies response ingestion on fatal error lines triggers abort.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=10.0, z=0.0, speed=50.0)],
            sent_count=1,
            done_count=0,
            failed_count=0,
            remote_queue_depth=1,
            start_time=0.0,
        )

        should_stop = self.runner.handle_incoming_line(
            'HOMING_FAILED', session=session
        )
        self.assertTrue(should_stop)
        self.assertEqual(self.state_controller.state, StreamState.STOPPED)

    def test_run_loop_execution(self) -> None:
        '''
            Verifies loop waypoint transmission and completion state.
        '''
        session = StreamSession(
            waypoints=[
                Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0),
                Waypoint(x=30.0, y=40.0, z=0.0, speed=50.0),
            ],
            sent_count=0,
            done_count=2,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        stop_event = Event()
        pause_event = Event()
        pause_event.set()

        def unpause_on_sleep(_delay: float) -> None:
            if pause_event.is_set():
                pause_event.clear()

        with patch('scarajectory.infrastructure.worker.ascii.stream_loop_runner.sleep', side_effect=unpause_on_sleep):
            with patch.object(
                self.runner._step_dispatcher,
                'can_dispatch_step',
                side_effect=[False, True, True],
            ):
                self.runner.run_loop(
                    session=session,
                    stop_event=stop_event,
                    pause_event=pause_event,
                )

        self.assertEqual(session.sent_count, 2)
        self.assertEqual(len(self.command_sender.sent_commands), 2)
        self.assertEqual(self.state_controller.state, StreamState.COMPLETED)

    def test_stream_loop_runner_factory(self) -> None:
        '''
            Verifies factory construction and version retrieval.
        '''
        self.assertIsInstance(self.runner, StreamLoopRunner)
        self.assertIsInstance(StreamLoopRunnerFactory.get_version(), str)


if __name__ == '__main__':
    main()
