# -*- coding: UTF-8 -*-

'''
Module
    waypoint_mutator.py
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
    Concrete implementation of individual waypoint mutation operations.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointMutator:
    '''
        Concrete implementation of individual waypoint mutation operations.

        It defines:

            :attributes:
                | _waypoints - Reference to internal list of motion waypoints.
            :methods:
                | __init__ - Initializes mutator with waypoint list reference.
                | add - Appends a waypoint to storage.
                | insert - Inserts a waypoint at specific index.
                | update - Updates a waypoint at specific index.
                | remove - Removes a waypoint at specific index.
    '''

    _waypoints: list[Waypoint]

    def __init__(self, waypoints: list[Waypoint]) -> None:
        '''
            Initializes mutator with waypoint list reference.

            :param waypoints: Reference to waypoint list.
            :exceptions: None.
        '''
        self._waypoints: Final[list[Waypoint]] = waypoints

    def add(self, point: Waypoint) -> None:
        '''
            Appends a waypoint to storage.

            :param point: Waypoint entity to append.
            :exceptions: None.
        '''
        self._waypoints.append(point)

    def insert(self, index: int, point: Waypoint) -> None:
        '''
            Inserts a waypoint at specific index.

            :param index: Target index.
            :param point: Waypoint entity to insert.
            :exceptions: None.
        '''
        self._waypoints.insert(index, point)

    def update(self, index: int, point: Waypoint) -> bool:
        '''
            Updates a waypoint at specific index.

            :param index: Target index.
            :param point: Replacement Waypoint entity.
            :return: True if updated, False otherwise.
            :exceptions: None.
        '''
        if 0 <= index < len(self._waypoints):
            self._waypoints[index] = point

            return True

        return False

    def remove(self, index: int) -> bool:
        '''
            Removes a waypoint at specific index.

            :param index: Target index.
            :return: True if removed, False otherwise.
            :exceptions: None.
        '''
        if 0 <= index < len(self._waypoints):
            self._waypoints.pop(index)

            return True

        return False
