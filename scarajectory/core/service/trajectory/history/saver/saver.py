# -*- coding: UTF-8 -*-

'''
Module
    saver.py
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
    State saver implementation for trajectory plan undo snapshots.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar, Final

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


class PlanHistorySaver:
    '''
        State saver recording snapshots to undo stack and clearing redo history.

        It defines:

            :constants:
                | MAX_STACK_SIZE - Maximum number of snapshots preserved in undo stack.
            :attributes:
                | _stack - Injected IPlanHistoryStack storage instance.
            :methods:
                | __init__ - Initializes saver with injected stack storage.
                | save_state - Pushes current snapshot onto undo stack and clears redo stack.
                | clear - Clears all states from stack storage.
    '''

    MAX_STACK_SIZE: ClassVar[int] = 50

    _stack: IPlanHistoryStack

    def __init__(self, stack: IPlanHistoryStack) -> None:
        '''
            Initializes saver with injected stack storage.

            :param stack: Injected IPlanHistoryStack instance.
            :exceptions: None.
        '''
        self._stack: Final[IPlanHistoryStack] = stack

    def save_state(self, current: Sequence[TrajectoryWaypoint]) -> None:
        '''
            Pushes current snapshot onto undo stack and clears redo stack.

            :param current: Current sequence of waypoints.
            :exceptions: None.
        '''
        undo = self._stack.undo_stack
        undo.append(list(current))

        if len(undo) > self.MAX_STACK_SIZE:
            undo.pop(0)

        self._stack.redo_stack.clear()

    def clear(self) -> None:
        '''
            Clears all states from stack storage.

            :exceptions: None.
        '''
        self._stack.clear()
