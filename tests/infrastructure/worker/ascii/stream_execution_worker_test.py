# -*- coding: UTF-8 -*-

'''
Module
    stream_execution_worker_test.py
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
    Unit tests for StreamExecutionWorker background threading and ack processing.
'''

from __future__ import annotations

from time import sleep, time
from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.stream_pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.worker.ascii.stream_execution_worker_factory import StreamExecutionWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockCommandSender:
    '''Mock command sender capturing sent commands.'''

    def __init__(self, target_list: list[str]) -> None:
        self._target_list = target_list

    def send_raw_command(self, cmd: str) -> bool:
        '''Sends raw command to target list.'''
        self._target_list.append(cmd)
        return True

    def can_send(self) -> bool:
        '''Checks if sender can transmit command.'''
        return True


class MockStateController:
    '''Mock stream state controller capturing transitions.'''

    def __init__(self, target_list: list[StreamState]) -> None:
        self._state = StreamState.IDLE
        self._target_list = target_list

    @property
    def state(self) -> StreamState:
        '''Returns active stream state.'''
        return self._state

    def set_state(self, state: StreamState) -> None:
        '''Updates stream state and records transition.'''
        self._state = state
        self._target_list.append(state)


class MockObserverDispatcher:
    '''Mock observer dispatcher capturing progress and logs.'''

    def __init__(
        self,
        progress_list: list[tuple[StreamSession, str]],
        log_list: list[tuple[str, bool]],
    ) -> None:
        self._progress_list = progress_list
        self._log_list = log_list

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''Records notification message in log list.'''
        self._log_list.append((msg, is_outgoing))

    def notify_progress(
        self,
        *,
        state: StreamState,
        session: StreamSession,
        current_line: str = '',
        error: str = '',
    ) -> None:
        '''Records notification progress and session state.'''
        _ = (state, current_line)
        self._progress_list.append((session, error))


class TestStreamExecutionWorker(TestCase):
    '''
        Test suite validating StreamExecutionWorker concurrency, flow control, and error handling.
    '''

    def setUp(self) -> None:
        '''
            Prepares mocked collaborators and worker instance for testing.
        '''
        barrier = FlowBarrierFactory.create()
        self._pacing_bundle: FlowPacingBundle = FlowPacingBundleFactory.create(
            barrier=barrier
        )
        self._sent_commands: list[str] = []
        self._progress_notifications: list[tuple[StreamSession, str]] = []
        self._log_messages: list[tuple[str, bool]] = []
        self._state_changes: list[StreamState] = []

        command_sender = MockCommandSender(self._sent_commands)
        state_controller = MockStateController(self._state_changes)
        observer_dispatcher = MockObserverDispatcher(
            self._progress_notifications,
            self._log_messages,
        )
        pacing_config = StreamPacingConfigFactory.create_ascii()

        self._worker = StreamExecutionWorkerFactory.create(
            pacing_bundle=self._pacing_bundle,
            command_sender=command_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

    def test_worker_initial_state(self) -> None:
        '''
            Verifies that worker is initially not running.
        '''
        self.assertFalse(self._worker.is_running())

    def test_worker_pause_and_resume(self) -> None:
        '''
            Verifies pause and resume event signaling.
        '''
        self._worker.pause()
        self._worker.resume()
        self.assertFalse(self._worker.is_running())

    def test_worker_stop(self) -> None:
        '''
            Verifies stop event signaling and flow controller reset.
        '''
        self._worker.stop()
        self.assertFalse(self._worker.is_running())

    def test_handle_incoming_line_normal_ack(self) -> None:
        '''
            Verifies normal response line updates flow controller and notifies progress.
        '''
        session = SessionFactory.create(
            waypoints=[Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0, speed=40.0)],
            sent_count=1,
            remote_queue_depth=1,
        )
        self._worker.session = session
        self.assertEqual(self._worker.session, session)

        self._worker.handle_incoming_line(line='<RESP:MOVE_DONE>')
        self.assertIn(('<RESP:MOVE_DONE>', False), self._log_messages)
        self.assertGreaterEqual(len(self._progress_notifications), 1)
        self.assertEqual(session.done_count, 1)

    def test_handle_incoming_line_fatal_error(self) -> None:
        '''
            Verifies fatal error triggers worker stop and transitions state to STOPPED.
        '''
        session = SessionFactory.create(
            waypoints=[Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0, speed=40.0)],
            sent_count=1,
            remote_queue_depth=1,
        )
        self._worker.session = session

        self._worker.handle_incoming_line(line='<ERR:HOMING_FAILED>')
        self.assertFalse(self._worker.is_running())
        self.assertIn(StreamState.STOPPED, self._state_changes)

    def test_start_streaming_and_stop(self) -> None:
        '''
            Verifies starting execution loop in background thread and cleanly stopping it.
        '''
        session = SessionFactory.create(
            waypoints=[
                Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0, speed=40.0),
                Waypoint(x=20.0, y=30.0, z=5.0, phi=0.0, speed=40.0),
            ],
            sent_count=0,
            start_time=time(),
        )

        self._worker.start(session=session)
        sleep(0.05)
        self.assertTrue(self._worker.is_running())
        self.assertGreaterEqual(len(self._sent_commands), 1)

        self._worker.stop()
        sleep(0.1)
        self.assertFalse(self._worker.is_running())


if __name__ == '__main__':
    main()
