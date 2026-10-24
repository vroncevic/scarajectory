# -*- coding: UTF-8 -*-

'''
Module
    worker.py
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
    Worker managing streaming concurrency lifecycle.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.infrastructure.worker.holder import StreamSessionHolder
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner
from scarajectory.infrastructure.worker.thread.icoordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamExecutionWorker:
    '''
        Worker managing streaming concurrency lifecycle.

        It defines:

            :attributes:
                | _loop_runner - IStreamLoopRunner managing step execution loops.
                | _coordinator - IWorkerThreadCoordinator managing background thread execution.
                | _session_holder - StreamSessionHolder tracking active stream session.
            :methods:
                | __init__ - Initializes worker with loop runner, coordinator, and session holder.
                | start_waypoints - Spawns background worker thread for waypoint sequence.
                | start_program - Spawns background worker thread for binary program.
                | set_paused - Updates stream transmission pause state.
                | stop - Aborts transmission loop and cleans up.
                | is_running - Checks if background thread is active.
    '''

    _loop_runner: IStreamLoopRunner
    _coordinator: IWorkerThreadCoordinator
    _session_holder: StreamSessionHolder

    def __init__(
        self,
        *,
        loop_runner: IStreamLoopRunner,
        coordinator: IWorkerThreadCoordinator,
        session_holder: StreamSessionHolder,
    ) -> None:
        '''
            Initializes stream worker with loop runner, coordinator, and session holder.

            :param loop_runner: Injected IStreamLoopRunner instance.
            :param coordinator: Injected IWorkerThreadCoordinator instance.
            :param session_holder: Injected StreamSessionHolder instance.
            :exceptions: None.
        '''
        self._loop_runner: Final[IStreamLoopRunner] = loop_runner
        self._coordinator: Final[IWorkerThreadCoordinator] = coordinator
        self._session_holder: Final[StreamSessionHolder] = session_holder

    def start_waypoints(self, *, session: StreamSession) -> None:
        '''
            Launches background worker for active waypoint session.

            :param session: Active StreamSession tracking metrics.
            :exceptions: None.
        '''
        self._session_holder.session = session
        self._coordinator.start_thread(
            target=self._loop_runner.run_waypoints_loop,
            kwargs={'session': session},
        )

    def start_program(
        self,
        *,
        session: StreamSession,
        program: BinaryProgram,
    ) -> None:
        '''
            Launches background worker for pre-compiled binary program.

            :param session: Active StreamSession tracking metrics.
            :param program: BinaryProgram containing compiled binary steps.
            :exceptions: None.
        '''
        self._session_holder.session = session
        self._coordinator.start_thread(
            target=self._loop_runner.run_program_loop,
            kwargs={'program': program, 'session': session},
        )

    def set_paused(self, paused: bool) -> None:
        '''
            Updates stream transmission pause state.

            :param paused: True to pause, False to resume.
            :exceptions: None.
        '''
        self._coordinator.set_paused(paused=paused)

    def stop(self) -> None:
        '''
            Stops worker immediately.

            :exceptions: None.
        '''
        self._coordinator.stop()

    def is_running(self) -> bool:
        '''
            Returns True if background thread is running.

            :return: True if running, False otherwise.
            :exceptions: None.
        '''
        return self._coordinator.is_running()
