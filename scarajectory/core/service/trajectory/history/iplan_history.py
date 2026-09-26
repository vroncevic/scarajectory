# -*- coding: UTF-8 -*-

'''
Module
    iplan_history.py
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
    Interface protocol for trajectory undo and redo history stack management.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPlanHistory(Protocol):
    '''
        Interface protocol for trajectory history stack management.

        It defines:

            :methods:
                | save_state - Pushes current snapshot onto undo stack.
                | undo - Pops last state from undo stack into redo stack.
                | redo - Pops last state from redo stack into undo stack.
                | clear - Clears all history.
    '''

    def save_state(self, current: list[Waypoint]) -> None:
        '''
            Pushes current snapshot onto undo stack.

            :param current: Current list of waypoints.
        '''

    def undo(self, current: list[Waypoint]) -> list[Waypoint] | None:
        '''
            Pops last state from undo stack into redo stack.

            :param current: Current list of waypoints.
            :return: Previous waypoints state or None if empty.
        '''

    def redo(self, current: list[Waypoint]) -> list[Waypoint] | None:
        '''
            Pops last state from redo stack into undo stack.

            :param current: Current list of waypoints.
            :return: Next waypoints state or None if empty.
        '''

    def clear(self) -> None:
        '''
            Clears all history.
        '''
