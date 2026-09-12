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

from os.path import abspath, dirname
from sys import path
from time import sleep, time
from unittest import TestCase, main
from unittest.mock import MagicMock

pkg_dir: str = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.communication.stream_session import StreamSession
from scarajectory.core.model.communication.stream_state import StreamState
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.communication.streamer.flow_controller import (
    FlowController,
)
from scarajectory.infrastructure.communication.streamer.stream_execution_worker import (
    StreamExecutionWorker,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamExecutionWorker(TestCase):
    '''
        Test suite validating StreamExecutionWorker concurrency, flow control, and error handling.
    '''

    def setUp(self) -> None:
        '''
            Prepares mocked callbacks and worker instance for testing.
        '''
        self._flow_controller = FlowController()
        self._sent_commands: list[str] = []
        self._progress_notifications: list[str] = []
        self._log_messages: list[tuple[str, bool]] = []
        self._state_changes: list[StreamState] = []

        self._worker = StreamExecutionWorker(
            flow_controller=self._flow_controller,
            send_command=self._mock_send_command,
            notify_progress=self._mock_notify_progress,
            notify_log=self._mock_notify_log,
            on_state_change=self._mock_on_state_change,
        )

    def _mock_send_command(self, cmd: str) -> bool:
        self._sent_commands.append(cmd)
        return True

    def _mock_notify_progress(self, error: str) -> None:
        self._progress_notifications.append(error)

    def _mock_notify_log(self, msg: str, is_outgoing: bool) -> None:
        self._log_messages.append((msg, is_outgoing))

    def _mock_on_state_change(self, state: StreamState) -> None:
        self._state_changes.append(state)

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
        self.assertTrue(self._worker._pause_event.is_set())
        self._worker.resume()
        self.assertFalse(self._worker._pause_event.is_set())

    def test_worker_stop(self) -> None:
        '''
            Verifies stop event signaling and flow controller reset.
        '''
        self._worker.stop()
        self.assertTrue(self._worker._stop_event.is_set())
        self.assertFalse(self._worker._pause_event.is_set())

    def test_handle_incoming_line_normal_ack(self) -> None:
        '''
            Verifies normal response line updates flow controller and notifies progress.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0)],
            sent_count=1,
            remote_queue_depth=1,
        )
        self._worker._session = session

        self._worker.handle_incoming_line(line='<RESP:MOVE_DONE>')
        self.assertIn(('<RESP:MOVE_DONE>', False), self._log_messages)
        self.assertGreaterEqual(len(self._progress_notifications), 1)
        self.assertEqual(session.done_count, 1)

    def test_handle_incoming_line_fatal_error(self) -> None:
        '''
            Verifies fatal error triggers worker stop and transitions state to STOPPED.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0)],
            sent_count=1,
            remote_queue_depth=1,
        )
        self._worker._session = session

        self._worker.handle_incoming_line(line='<ERR:HOMING_FAILED>')
        self.assertTrue(self._worker._stop_event.is_set())
        self.assertIn(StreamState.STOPPED, self._state_changes)

    def test_start_streaming_and_stop(self) -> None:
        '''
            Verifies starting execution loop in background thread and cleanly stopping it.
        '''
        session = StreamSession(
            waypoints=[
                Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0),
                Waypoint(x=20.0, y=30.0, z=5.0, phi=0.0),
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
