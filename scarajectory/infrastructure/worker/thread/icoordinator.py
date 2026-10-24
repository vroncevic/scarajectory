# -*- coding: UTF-8 -*-

'''
Module
    icoordinator.py
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
    Defines structural protocol IWorkerThreadCoordinator for worker thread management.
'''

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWorkerThreadCoordinator(Protocol):
    '''
        Structural protocol defining worker background thread lifecycle management.

        It defines:

            :methods:
                | start_thread - Spawns and starts background worker thread with target function.
                | set_paused - Updates pause state for synchronization events.
                | stop - Aborts execution, sets termination event, and resets barrier.
                | is_running - Checks whether worker thread is actively executing.
    '''

    def start_thread(
        self,
        *,
        target: Callable[..., None],
        kwargs: Mapping[str, object],
    ) -> None:
        '''
            Spawns and starts background worker thread with target function and kwargs.

            :param target: Target callable to execute in worker thread.
            :param kwargs: Keyword arguments dictionary for target callable.
        '''

    def set_paused(self, *, paused: bool) -> None:
        '''
            Updates pause state for synchronization events.

            :param paused: True to pause transmission, False to resume.
        '''

    def stop(self) -> None:
        '''
            Aborts execution, sets termination event, and resets barrier.
        '''

    def is_running(self) -> bool:
        '''
            Checks whether worker thread is actively executing.

            :return: True if active and thread is alive, False otherwise.
        '''
