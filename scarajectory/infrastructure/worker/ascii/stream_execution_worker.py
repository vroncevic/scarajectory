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

from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.ascii.istream_loop_runner import IStreamLoopRunner
from scarajectory.infrastructure.worker.thread.iworker_thread_coordinator import IWorkerThreadCoordinator

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
        Worker thread managing streaming transmission concurrency and state.

        It defines:

            :attributes:
                | _loop_runner - IStreamLoopRunner managing execution loops and lines.
                | _coordinator - IWorkerThreadCoordinator managing thread concurrency.
                | _session - Active trajectory streaming session metrics.
            :methods:
                | __init__ - Initializes the streaming execution worker with loop runner and coordinator.
                | start - Launches the background streaming thread for the active session.
                | pause - Signals the worker loop to pause waypoint transmission.
                | resume - Resumes the paused transmission loop.
                | stop - Aborts transmission loop and cleans up synchronization events.
                | is_running - Checks if background thread is active.
                | handle_incoming_line - Evaluates incoming response line and stops on fatal error.
    '''

    _loop_runner: IStreamLoopRunner
    _coordinator: IWorkerThreadCoordinator
    _session: StreamSession

    def __init__(
        self,
        *,
        loop_runner: IStreamLoopRunner,
        coordinator: IWorkerThreadCoordinator,
    ) -> None:
        '''
            Initializes the streaming execution worker with loop runner and thread coordinator.

            :param loop_runner: IStreamLoopRunner managing execution loops and lines.
            :param coordinator: IWorkerThreadCoordinator managing background thread execution.
            :exceptions: None.
        '''
        self._loop_runner: Final[IStreamLoopRunner] = loop_runner
        self._coordinator: Final[IWorkerThreadCoordinator] = coordinator
        self._session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )

    def start(self, *, session: StreamSession) -> None:
        '''
            Launches the background streaming thread for the active session.

            :param session: Active StreamSession tracking waypoints and transmission counters.
            :exceptions: None.
        '''
        self._session = session
        self._coordinator.start_thread(
            target=self._loop_runner.run_loop,
            kwargs={'session': self._session},
        )

    def pause(self) -> None:
        '''
            Signals the worker loop to pause waypoint transmission.

            :exceptions: None.
        '''
        self._coordinator.set_paused(paused=True)

    def resume(self) -> None:
        '''
            Resumes the paused transmission loop.

            :exceptions: None.
        '''
        self._coordinator.set_paused(paused=False)

    def stop(self) -> None:
        '''
            Signals the worker loop to abort immediately and resets synchronization flags.

            :exceptions: None.
        '''
        self._coordinator.stop()

    def is_running(self) -> bool:
        '''
            Checks whether the background worker thread is currently running.

            :return: True if alive, False otherwise.
            :exceptions: None.
        '''
        return self._coordinator.is_running()

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

    @property
    def session(self) -> StreamSession:
        '''
            Returns active stream session tracking progress and telemetry.

            :return: Active StreamSession instance.
            :exceptions: None.
        '''
        return self._session

    @session.setter
    def session(self, session: StreamSession) -> None:
        '''
            Sets active stream session tracking progress and telemetry.

            :param session: Active StreamSession instance to assign.
            :exceptions: None.
        '''
        self._session = session
