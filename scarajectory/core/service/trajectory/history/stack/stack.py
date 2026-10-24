# -*- coding: UTF-8 -*-

'''
Module
    stack.py
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
    Underlying stack storage for trajectory plan undo and redo snapshots.
'''

from __future__ import annotations

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanHistoryStack:
    '''
        Storage container managing raw undo and redo waypoint snapshot stacks.

        It defines:

            :attributes:
                | _undo_stack - Internal stack holding undo states.
                | _redo_stack - Internal stack holding redo states.
            :methods:
                | __init__ - Initializes empty undo and redo stacks.
                | undo_stack - Returns reference to internal undo stack.
                | redo_stack - Returns reference to internal redo stack.
                | clear - Clears all states from both undo and redo stacks.
    '''

    _undo_stack: list[list[TrajectoryWaypoint]]
    _redo_stack: list[list[TrajectoryWaypoint]]

    def __init__(self) -> None:
        '''
            Initializes empty undo and redo stacks.

            :exceptions: None.
        '''
        self._undo_stack = []
        self._redo_stack = []

    @property
    def undo_stack(self) -> list[list[TrajectoryWaypoint]]:
        '''
            Returns internal undo stack.

            :return: List of waypoint snapshot lists.
            :exceptions: None.
        '''
        return self._undo_stack

    @property
    def redo_stack(self) -> list[list[TrajectoryWaypoint]]:
        '''
            Returns internal redo stack.

            :return: List of waypoint snapshot lists.
            :exceptions: None.
        '''
        return self._redo_stack

    def clear(self) -> None:
        '''
            Clears all states from both undo and redo stacks.

            :exceptions: None.
        '''
        self._undo_stack.clear()
        self._redo_stack.clear()
