# -*- coding: UTF-8 -*-

'''
Module
    waypoint_bulk_mutator.py
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
    Concrete implementation of bulk waypoint clear and replace operations.
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


class WaypointBulkMutator:
    '''
        Concrete implementation of bulk waypoint clear and replace operations.

        It defines:

            :attributes:
                | _waypoints - Reference to internal list of motion waypoints.
            :methods:
                | __init__ - Initializes bulk mutator with waypoint list reference.
                | clear - Clears all stored waypoints.
                | replace - Replaces all stored waypoints with a new sequence.
    '''

    _waypoints: list[Waypoint]

    def __init__(self, waypoints: list[Waypoint]) -> None:
        '''
            Initializes bulk mutator with waypoint list reference.

            :param waypoints: Reference to waypoint list.
            :exceptions: None.
        '''
        self._waypoints: Final[list[Waypoint]] = waypoints

    def clear(self) -> None:
        '''
            Clears all stored waypoints.

            :exceptions: None.
        '''
        self._waypoints.clear()

    def replace(self, waypoints: Sequence[Waypoint]) -> None:
        '''
            Replaces all stored waypoints with a new sequence.

            :param waypoints: Sequence of Waypoint entities.
            :exceptions: None.
        '''
        self._waypoints.clear()
        self._waypoints.extend(waypoints)
