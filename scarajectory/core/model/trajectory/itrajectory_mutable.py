# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_mutable.py
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
    Interface protocol for mutating trajectory plan waypoints.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable
from collections.abc import Sequence

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.model.trajectory.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryMutable(ITrajectoryReadOnly, Protocol):
    '''
        Interface protocol for mutating trajectory waypoints.

        It defines:

            :methods:
                | add_point - Appends waypoint to plan.
                | insert_point - Inserts waypoint at index.
                | remove_point - Removes waypoint at index.
                | clear - Clears all waypoints.
                | set_waypoints - Replaces all waypoints with a new sequence.
                | update_point - Modifies waypoint at index.
    '''

    def add_point(self, point: Waypoint) -> None:
        '''
            Appends waypoint to plan.

            :param point: Waypoint entity.
        '''

    def insert_point(self, index: int, point: Waypoint) -> None:
        '''
            Inserts waypoint at specified index.

            :param index: Insertion index.
            :param point: Waypoint entity.
        '''

    def remove_point(self, index: int) -> bool:
        '''
            Removes waypoint at index.

            :param index: Target waypoint index.
            :return: True if removed, False otherwise.
        '''

    def clear(self) -> None:
        '''
            Clears all waypoints.
        '''

    def set_waypoints(self, waypoints: Sequence[Waypoint]) -> None:
        '''
            Replaces all waypoints with a new sequence.

            :param waypoints: Sequence of Waypoint instances.
        '''

    def update_point(self, index: int, new_point: Waypoint) -> bool:
        '''
            Modifies waypoint at index.

            :param index: Target waypoint index.
            :param new_point: Replacement Waypoint entity.
            :return: True if updated, False otherwise.
        '''
