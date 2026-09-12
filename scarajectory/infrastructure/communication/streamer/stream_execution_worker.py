# -*- coding: UTF-8 -*-

'''
Module
    stream_execution_worker.py
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
    Dedicated background worker managing trajectory streaming execution loop and microcontroller acks.
'''

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from threading import Event, Thread
from time import sleep, time
from typing import Final

from scarajectory.core.model.communication.stream_session import StreamSession
from scarajectory.core.model.communication.stream_state import StreamState
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.communication.protocol.command_formatter import (
    CommandFormatter,
)
from scarajectory.infrastructure.communication.streamer.flow_controller import (
    FlowController,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamExecutionWorker:
    '''
        Dedicated worker thread executing packet queue transmission and microcontroller ack handling.

        It defines:

            :attributes:
                | _flow_controller - Microcontroller buffer flow controller.
                | _send_command - Callback for transmitting raw command packets over transport.
                | _notify_progress - Callback for publishing updated streaming metrics.
                | _notify_log - Callback for appending log messages to observers.
                | _on_state_change - Callback signaling streaming state transitions.
                | _worker_thread - Active background worker thread.
                | _stop_event - Event signaling streaming loop termination.
                | _pause_event - Event signaling transmission pause.
                | _session - Active trajectory streaming session metrics.
            :methods:
                | __init__ - Initializes worker with flow controller and communication callbacks.
                | start - Spawns background worker thread for given streaming session.
                | pause - Signals transmission pause.
                | resume - Resumes paused transmission loop.
                | stop - Aborts transmission loop and cleans up synchronization events.
                | is_running - Checks if background thread is active.
                | handle_incoming_line - Evaluates incoming microcontroller response string.
    '''

    _flow_controller: FlowController
    _send_command: Callable[[str], bool]
    _notify_progress: Callable[[str], None]
    _notify_log: Callable[[str, bool], None]
    _on_state_change: Callable[[StreamState], None]
    _worker_thread: Thread | None
    _stop_event: Final[Event]
    _pause_event: Final[Event]
    _session: StreamSession | None

    def __init__(
        self,
        *,
        flow_controller: FlowController,
        send_command: Callable[[str], bool],
        notify_progress: Callable[[str], None],
        notify_log: Callable[[str, bool], None],
        on_state_change: Callable[[StreamState], None],
    ) -> None:
        '''
            Initializes the streaming execution worker with callbacks and flow controller.

            :param flow_controller: FlowController managing microcontroller buffer queue.
            :param send_command: Callable transmitting raw command string.
            :param notify_progress: Callable emitting progress notifications.
            :param notify_log: Callable logging communication messages.
            :param on_state_change: Callable updating streamer state enum.
            :exceptions: None.
        '''
        self._flow_controller = flow_controller
        self._send_command = send_command
        self._notify_progress = notify_progress
        self._notify_log = notify_log
        self._on_state_change = on_state_change
        self._worker_thread = None
        self._stop_event = Event()
        self._pause_event = Event()
        self._session = None

    def start(self, *, session: StreamSession) -> None:
        '''
            Launches the background streaming thread for the active session.

            :param session: Active StreamSession tracking waypoints and transmission counters.
            :exceptions: None.
        '''
        self._session = session
        self._stop_event.clear()
        self._pause_event.clear()
        self._worker_thread = Thread(target=self._run_loop, daemon=True)
        self._worker_thread.start()

    def pause(self) -> None:
        '''
            Signals the worker loop to pause packet transmission.

            :exceptions: None.
        '''
        self._pause_event.set()

    def resume(self) -> None:
        '''
            Clears the pause signal to resume packet transmission.

            :exceptions: None.
        '''
        self._pause_event.clear()

    def stop(self) -> None:
        '''
            Signals the worker loop to abort immediately and resets synchronization flags.

            :exceptions: None.
        '''
        self._stop_event.set()
        self._pause_event.clear()
        self._flow_controller.reset()

    def is_running(self) -> bool:
        '''
            Checks whether the background worker thread is currently running.

            :return: True if alive, False otherwise.
            :exceptions: None.
        '''
        return self._worker_thread is not None and self._worker_thread.is_alive()

    def _run_loop(self) -> None:
        '''
            Internal background execution loop transmitting waypoints according to flow control.

            :exceptions: None.
        '''
        if self._session is None:
            return

        session: StreamSession = self._session
        flow: FlowController = self._flow_controller

        while not self._stop_event.is_set() and session.sent_count < len(session.waypoints):
            if self._pause_event.is_set():
                sleep(0.05)
                continue

            pt: Waypoint = session.waypoints[session.sent_count]
            is_cmd: bool = bool(pt.command)

            if flow.can_send(session, is_command=is_cmd):
                pkt: str = (
                    pt.command
                    if pt.command
                    else CommandFormatter.format_move(pt)
                )
                if is_cmd:
                    flow.set_barrier()

                self._send_command(pkt)
                session.sent_count += 1
                if not is_cmd:
                    session.remote_queue_depth += 1
                self._notify_progress('')
                sleep(0.01)
            else:
                sleep(0.02)

        while (
            not self._stop_event.is_set()
            and (session.done_count + session.failed_count) < len(session.waypoints)
        ):
            sleep(0.05)

        if not self._stop_event.is_set():
            self._on_state_change(StreamState.COMPLETED)
            elapsed: float = time() - session.start_time
            end_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self._notify_progress('')
            if session.failed_count > 0:
                self._notify_log(
                    f'[{end_ts}] [MOVE FINISHED]: {session.done_count} succeeded, '
                    f'{session.failed_count} failed/rejected!',
                    False,
                )
            else:
                self._notify_log(
                    f'[{end_ts}] [MOVE COMPLETED]: All {len(session.waypoints)} waypoints finished!',
                    False,
                )
            self._notify_log(
                f'[HOST STATS]: Total Execution Time: {elapsed:.2f} s',
                False,
            )

    def handle_incoming_line(self, *, line: str) -> None:
        '''
            Evaluates incoming serial response line and updates buffer capacity counters.

            :param line: Raw response line string received from microcontroller.
            :exceptions: None.
        '''
        self._notify_log(line, False)

        if self._session is None:
            return

        fatal_error, error_msg = self._flow_controller.process_response(
            line, self._session
        )
        if fatal_error:
            self._notify_progress(error_msg or line)
            self._notify_log(f'[ERR]: {error_msg}. Aborting stream.', False)
            self.stop()
            self._on_state_change(StreamState.STOPPED)
            return

        if error_msg:
            self._notify_progress(error_msg)
        else:
            self._notify_progress('')
