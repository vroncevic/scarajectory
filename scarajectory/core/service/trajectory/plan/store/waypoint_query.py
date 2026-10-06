# -*- coding: UTF-8 -*-

'''
Module
    waypoint_query.py
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
    Concrete implementation of read-only waypoint storage queries.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointQuery:
    '''
        Concrete implementation of read-only waypoint storage queries.

        It defines:

            :attributes:
                | _waypoints - Reference to internal list of motion waypoints.
            :methods:
                | __init__ - Initializes query provider with waypoint list reference.
                | waypoints - Returns read-only view of waypoints.
                | count - Returns total number of waypoints.
    '''

    _waypoints: list[Waypoint]

    def __init__(self, waypoints: list[Waypoint]) -> None:
        '''
            Initializes query provider with waypoint list reference.

            :param waypoints: Reference to waypoint list.
            :exceptions: None.
        '''
        self._waypoints: Final[list[Waypoint]] = waypoints

    @property
    def waypoints(self) -> Sequence[Waypoint]:
        '''
            Returns read-only view of waypoints.

            :return: Tuple of Waypoint instances.
            :exceptions: None.
        '''
        return tuple(self._waypoints)

    @property
    def count(self) -> int:
        '''
            Returns total number of waypoints.

            :return: Number of waypoints.
            :exceptions: None.
        '''
        return len(self._waypoints)
