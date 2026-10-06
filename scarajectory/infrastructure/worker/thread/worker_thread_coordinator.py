# -*- coding: UTF-8 -*-

'''
Module
    worker_thread_coordinator.py
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
    Coordinator managing background worker thread execution and lifecycle synchronization.
'''

from __future__ import annotations

from threading import Event, Thread
from typing import Any, Callable, Final

from scarajectory.infrastructure.pacing.iflow_barrier_coordinator import IFlowBarrierCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerThreadCoordinator:
    '''
        Coordinator managing background worker thread execution and lifecycle synchronization.

        It defines:

            :attributes:
                | _barrier_coordinator - IFlowBarrierCoordinator managing synchronization barriers.
                | _worker_thread - Active background worker thread.
                | _stop_event - Event signaling streaming loop termination.
                | _pause_event - Event signaling transmission pause.
                | _is_running - Flag indicating whether worker thread is actively executing.
            :methods:
                | __init__ - Initializes coordinator with barrier coordinator.
                | start_thread - Spawns and starts background worker thread with target function.
                | set_paused - Updates pause state for synchronization events.
                | stop - Aborts execution, sets termination event, and resets barrier.
                | is_running - Checks whether worker thread is actively executing.
    '''

    _barrier_coordinator: IFlowBarrierCoordinator
    _worker_thread: Thread
    _stop_event: Event
    _pause_event: Event
    _is_running: bool

    def __init__(
        self,
        *,
        barrier_coordinator: IFlowBarrierCoordinator,
    ) -> None:
        '''
            Initializes coordinator with barrier coordinator.

            :param barrier_coordinator: IFlowBarrierCoordinator managing synchronization barriers.
            :exceptions: None.
        '''
        self._barrier_coordinator: Final[IFlowBarrierCoordinator] = (
            barrier_coordinator
        )
        self._worker_thread: Thread = Thread(target=tuple)
        self._stop_event: Final[Event] = Event()
        self._pause_event: Final[Event] = Event()
        self._is_running: bool = False

    def start_thread(
        self,
        *,
        target: Callable[..., None],
        kwargs: dict[str, Any],
    ) -> None:
        '''
            Spawns and starts background worker thread with target function and kwargs.

            :param target: Target callable to execute in worker thread.
            :param kwargs: Keyword arguments dictionary for target callable.
            :exceptions: None.
        '''
        self._is_running = True
        self._stop_event.clear()
        self._pause_event.clear()
        thread_kwargs: dict[str, Any] = dict(kwargs)
        thread_kwargs['stop_event'] = self._stop_event
        thread_kwargs['pause_event'] = self._pause_event
        self._worker_thread = Thread(
            target=target,
            kwargs=thread_kwargs,
            daemon=True,
        )
        self._worker_thread.start()

    def set_paused(self, *, paused: bool) -> None:
        '''
            Updates pause state for synchronization events.

            :param paused: True to pause transmission, False to resume.
            :exceptions: None.
        '''
        if paused:
            self._pause_event.set()
        else:
            self._pause_event.clear()

    def stop(self) -> None:
        '''
            Aborts execution, sets termination event, and resets barrier coordinator.

            :exceptions: None.
        '''
        self._is_running = False
        self._stop_event.set()
        self._pause_event.clear()
        self._barrier_coordinator.reset()

    def is_running(self) -> bool:
        '''
            Checks whether worker thread is actively executing.

            :return: True if active and thread is alive, False otherwise.
            :exceptions: None.
        '''
        return self._is_running and self._worker_thread.is_alive()
