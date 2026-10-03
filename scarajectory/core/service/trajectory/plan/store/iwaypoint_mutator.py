# -*- coding: UTF-8 -*-

'''
Module
    iwaypoint_mutator.py
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
    Interface protocol for mutating individual trajectory waypoints.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWaypointMutator(Protocol):
    '''
        Structural protocol defining individual waypoint insertion, modification, and removal.

        It defines:

            :methods:
                | add - Appends a waypoint to storage.
                | insert - Inserts a waypoint at specific index.
                | update - Updates a waypoint at specific index.
                | remove - Removes a waypoint at specific index.
    '''

    def add(self, point: Waypoint) -> None:
        '''
            Appends a waypoint to storage.

            :param point: Waypoint entity to append.
        '''

    def insert(self, index: int, point: Waypoint) -> None:
        '''
            Inserts a waypoint at specific index.

            :param index: Target index.
            :param point: Waypoint entity to insert.
        '''

    def update(self, index: int, point: Waypoint) -> bool:
        '''
            Updates a waypoint at specific index.

            :param index: Target index.
            :param point: Replacement Waypoint entity.
            :return: True if updated, False otherwise.
        '''

    def remove(self, index: int) -> bool:
        '''
            Removes a waypoint at specific index.

            :param index: Target index.
            :return: True if removed, False otherwise.
        '''
