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
    Worker thread managing streaming transmission concurrency and state.
'''

from __future__ import annotations

from threading import Event, Thread
from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.service.barrier.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.core.service.worker.istream_loop_runner import IStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamExecutionWorker:
    '''
        Worker thread managing streaming transmission concurrency and state.

        It defines:

            :attributes:
                | _loop_runner - IStreamLoopRunner managing execution loops and lines.
                | _barrier_coordinator - Injected IFlowBarrierCoordinator managing synchronization.
                | _worker_thread - Active background worker thread.
                | _stop_event - Event signaling streaming loop termination.
                | _pause_event - Event signaling transmission pause.
                | _session - Active trajectory streaming session metrics.
                | _is_running - Flag indicating whether worker thread is actively executing.
            :methods:
                | __init__ - Initializes the streaming execution worker with loop runner and barrier.
                | start - Launches the background streaming thread for the active session.
                | pause - Signals the worker loop to pause waypoint transmission.
                | resume - Resumes the paused transmission loop.
                | stop - Aborts transmission loop and cleans up synchronization events.
                | is_running - Checks if background thread is active.
                | handle_incoming_line - Evaluates incoming response line and stops on fatal error.
    '''

    _loop_runner: IStreamLoopRunner
    _barrier_coordinator: IFlowBarrierCoordinator
    _worker_thread: Thread
    _stop_event: Event
    _pause_event: Event
    _session: StreamSession
    _is_running: bool

    def __init__(
        self,
        *,
        loop_runner: IStreamLoopRunner,
        barrier_coordinator: IFlowBarrierCoordinator,
    ) -> None:
        '''
            Initializes the streaming execution worker with loop runner and barrier coordinator.

            :param loop_runner: IStreamLoopRunner managing execution loops and lines.
            :param barrier_coordinator: IFlowBarrierCoordinator managing synchronization barriers.
            :exceptions: None.
        '''
        self._loop_runner: Final[IStreamLoopRunner] = loop_runner
        self._barrier_coordinator: Final[IFlowBarrierCoordinator] = (
            barrier_coordinator
        )
        self._worker_thread: Thread = Thread(target=tuple)
        self._stop_event: Final[Event] = Event()
        self._pause_event: Final[Event] = Event()
        self._session: StreamSession = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        self._is_running: bool = False

    def start(self, *, session: StreamSession) -> None:
        '''
            Launches the background streaming thread for the active session.

            :param session: Active StreamSession tracking waypoints and transmission counters.
            :exceptions: None.
        '''
        self._session = session
        self._is_running = True
        self._stop_event.clear()
        self._pause_event.clear()
        self._worker_thread = Thread(
            target=self._loop_runner.run_loop,
            kwargs={
                'session': self._session,
                'stop_event': self._stop_event,
                'pause_event': self._pause_event,
            },
            daemon=True,
        )
        self._worker_thread.start()

    def pause(self) -> None:
        '''
            Signals the worker loop to pause waypoint transmission.

            :exceptions: None.
        '''
        self._pause_event.set()

    def resume(self) -> None:
        '''
            Resumes the paused transmission loop.

            :exceptions: None.
        '''
        self._pause_event.clear()

    def stop(self) -> None:
        '''
            Signals the worker loop to abort immediately and resets synchronization flags.

            :exceptions: None.
        '''
        self._is_running = False
        self._stop_event.set()
        self._pause_event.clear()
        self._barrier_coordinator.reset()

    def is_running(self) -> bool:
        '''
            Checks whether the background worker thread is currently running.

            :return: True if alive, False otherwise.
            :exceptions: None.
        '''
        return self._is_running and self._worker_thread.is_alive()

    def handle_incoming_line(self, line: str) -> None:
        '''
            Evaluates incoming response line and stops on fatal error.

            :param line: Raw response line string from transport.
            :exceptions: None.
        '''
        should_stop: bool = self._loop_runner.handle_incoming_line(
            line, session=self._session
        )

        if should_stop:
            self.stop()
