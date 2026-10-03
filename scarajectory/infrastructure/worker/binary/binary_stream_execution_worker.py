# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_execution_worker.py
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
    Worker thread managing binary streaming concurrency lifecycle.
'''

from __future__ import annotations

from threading import Event, Thread
from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.service.barrier.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.worker.binary.ibinary_stream_loop_runner import IBinaryStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamExecutionWorker:
    '''
        Background worker thread managing binary streaming concurrency lifecycle.

        It defines:

            :attributes:
                | _loop_runner - IBinaryStreamLoopRunner managing step execution loops.
                | _barrier_coordinator - IFlowBarrierCoordinator managing synchronization barriers.
                | _worker_thread - Active background worker thread.
                | _stop_event - Event signaling streaming loop termination.
                | _pause_event - Event signaling transmission pause.
                | _session - Active trajectory streaming session metrics.
                | _is_running - Flag indicating whether worker thread is actively executing.
            :methods:
                | __init__ - Initializes worker with injected loop runner and barrier coordinator.
                | start - Spawns background worker thread for waypoint sequence.
                | start_program - Spawns background worker thread for binary program.
                | pause - Signals transmission pause.
                | resume - Resumes paused transmission loop.
                | stop - Aborts transmission loop and cleans up.
                | is_running - Checks if background thread is active.
                | handle_incoming_bytes - Feeds raw incoming bytes into loop runner.
    '''

    _loop_runner: IBinaryStreamLoopRunner
    _barrier_coordinator: IFlowBarrierCoordinator
    _worker_thread: Thread
    _stop_event: Event
    _pause_event: Event
    _session: StreamSession
    _is_running: bool

    def __init__(
        self,
        *,
        loop_runner: IBinaryStreamLoopRunner,
        barrier_coordinator: IFlowBarrierCoordinator,
    ) -> None:
        '''
            Initializes binary stream worker with loop runner and barrier coordinator.

            :param loop_runner: IBinaryStreamLoopRunner managing execution loops.
            :param barrier_coordinator: IFlowBarrierCoordinator managing synchronization barriers.
            :exceptions: None.
        '''
        self._loop_runner: Final[IBinaryStreamLoopRunner] = loop_runner
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
            Launches background worker for active session of waypoints.

            :param session: Active StreamSession tracking waypoints and metrics.
            :exceptions: None.
        '''
        self._session = session
        self._is_running = True
        self._stop_event.clear()
        self._pause_event.clear()
        self._worker_thread = Thread(
            target=self._loop_runner.run_waypoints_loop,
            kwargs={
                'session': self._session,
                'stop_event': self._stop_event,
                'pause_event': self._pause_event,
            },
            daemon=True,
        )
        self._worker_thread.start()

    def start_program(
        self,
        *,
        program: BinaryProgram,
        session: StreamSession,
    ) -> None:
        '''
            Launches background worker for pre-compiled binary steps.

            :param program: BinaryProgram containing compiled binary steps.
            :param session: Active StreamSession tracking step progress.
            :exceptions: None.
        '''
        self._session = session
        self._is_running = True
        self._stop_event.clear()
        self._pause_event.clear()
        self._worker_thread = Thread(
            target=self._loop_runner.run_program_loop,
            kwargs={
                'program': program,
                'session': self._session,
                'stop_event': self._stop_event,
                'pause_event': self._pause_event,
            },
            daemon=True,
        )
        self._worker_thread.start()

    def pause(self) -> None:
        '''
            Pauses worker transmission loop.

            :exceptions: None.
        '''
        self._pause_event.set()

    def resume(self) -> None:
        '''
            Resumes worker transmission loop.

            :exceptions: None.
        '''
        self._pause_event.clear()

    def stop(self) -> None:
        '''
            Stops worker immediately.

            :exceptions: None.
        '''
        self._is_running = False
        self._stop_event.set()
        self._pause_event.clear()
        self._barrier_coordinator.reset()

    def is_running(self) -> bool:
        '''
            Returns True if background thread is running.

            :return: True if running, False otherwise.
            :exceptions: None.
        '''
        return self._is_running and self._worker_thread.is_alive()

    def handle_incoming_bytes(self, data: bytes) -> None:
        '''
            Feeds incoming raw byte chunk into loop runner parser and handler.

            :param data: Raw byte chunk from transport stream.
            :exceptions: None.
        '''
        should_stop: bool = self._loop_runner.handle_incoming_bytes(
            data=data, session=self._session
        )

        if should_stop:
            self.stop()
