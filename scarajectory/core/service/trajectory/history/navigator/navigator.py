# -*- coding: UTF-8 -*-

'''
Module
    navigator.py
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
    History navigation manager for undo and redo operations on waypoint collections.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.stack.istack import IPlanHistoryStack

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanHistoryNavigator:
    '''
        History navigation manager for undo and redo operations on waypoint collections.

        It defines:

            :attributes:
                | _stack - Injected IPlanHistoryStack storage instance.
            :methods:
                | __init__ - Initializes history navigator with injected stack storage.
                | can_undo - Checks whether undo history is available.
                | can_redo - Checks whether redo history is available.
                | undo - Pops last state from undo stack into redo stack.
                | redo - Pops last state from redo stack into undo stack.
    '''

    _stack: IPlanHistoryStack

    def __init__(self, stack: IPlanHistoryStack) -> None:
        '''
            Initializes history navigator with injected stack storage.

            :param stack: Injected IPlanHistoryStack instance.
            :exceptions: None.
        '''
        self._stack: Final[IPlanHistoryStack] = stack

    def can_undo(self) -> bool:
        '''
            Checks whether undo history is available.

            :return: True if undo history exists, False otherwise.
            :exceptions: None.
        '''
        return len(self._stack.undo_stack) > 0

    def can_redo(self) -> bool:
        '''
            Checks whether redo history is available.

            :return: True if redo history exists, False otherwise.
            :exceptions: None.
        '''
        return len(self._stack.redo_stack) > 0

    def undo(
        self, current: Sequence[TrajectoryWaypoint]
    ) -> list[TrajectoryWaypoint]:
        '''
            Pops last state from undo stack into redo stack.

            :param current: Current sequence of waypoints.
            :return: Previous waypoints state, or current state if empty.
            :exceptions: None.
        '''
        undo = self._stack.undo_stack

        if not undo:
            return list(current)

        self._stack.redo_stack.append(list(current))

        return undo.pop()

    def redo(
        self, current: Sequence[TrajectoryWaypoint]
    ) -> list[TrajectoryWaypoint]:
        '''
            Pops last state from redo stack into undo stack.

            :param current: Current sequence of waypoints.
            :return: Next waypoints state, or current state if empty.
            :exceptions: None.
        '''
        redo = self._stack.redo_stack

        if not redo:
            return list(current)

        self._stack.undo_stack.append(list(current))

        return redo.pop()
