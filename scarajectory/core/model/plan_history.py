# -*- coding: UTF-8 -*-

'''
Module
    plan_history.py
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
    History stack manager for undo and redo operations on waypoint collections.
'''

from __future__ import annotations

from scarajectory.core.model.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanHistory:
    '''
        History stack manager for undo and redo operations on waypoint collections.

        It defines:

            :attributes:
                | _undo_stack - History stack for undo states.
                | _redo_stack - History stack for redo states.
            :methods:
                | __init__ - Initializes empty undo and redo stacks.
                | save_state - Pushes current snapshot onto undo stack.
                | undo - Pops last state from undo stack into redo stack.
                | redo - Pops last state from redo stack into undo stack.
                | clear - Clears all history.
    '''

    _undo_stack: list[list[Waypoint]]
    _redo_stack: list[list[Waypoint]]

    def __init__(self) -> None:
        '''
            Initializes empty undo and redo stacks.

            :exceptions: None.
        '''
        self._undo_stack = []
        self._redo_stack = []

    def save_state(self, current: list[Waypoint]) -> None:
        '''
            Pushes current snapshot onto undo stack.

            :param current: Current list of waypoints.
            :exceptions: None.
        '''
        self._undo_stack.append(list(current))
        if len(self._undo_stack) > 50:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def undo(self, current: list[Waypoint]) -> list[Waypoint] | None:
        '''
            Pops last state from undo stack into redo stack.

            :param current: Current list of waypoints.
            :return: Previous waypoints state or None if empty.
            :exceptions: None.
        '''
        if not self._undo_stack:
            return None
        self._redo_stack.append(list(current))
        return self._undo_stack.pop()

    def redo(self, current: list[Waypoint]) -> list[Waypoint] | None:
        '''
            Pops last state from redo stack into undo stack.

            :param current: Current list of waypoints.
            :return: Next waypoints state or None if empty.
            :exceptions: None.
        '''
        if not self._redo_stack:
            return None
        self._undo_stack.append(list(current))
        return self._redo_stack.pop()

    def clear(self) -> None:
        '''
            Clears all history.

            :exceptions: None.
        '''
        self._undo_stack.clear()
        self._redo_stack.clear()
