# -*- coding: UTF-8 -*-

'''
Module
    iadapter.py
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
    Interface protocol for dead zone avoidance and bypass path planning.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDeadZoneAvoidanceAdapter(Protocol):
    '''
        Structural protocol defining dead zone intersection checks and detour planning.

        It defines:

            :methods:
                | crosses_dead_zone - Determines if segment traverses dead zone.
                | is_point_in_dead_zone - Checks if waypoint coordinates reside in dead zone.
                | plan_detour - Plans intermediate detour waypoints bypassing dead zone.
                | get_version - Returns adapter component version string.
    '''

    def crosses_dead_zone(
        self,
        start_point: TrajectoryWaypoint,
        end_point: TrajectoryWaypoint,
    ) -> bool:
        '''
            Determines if direct straight-line segment crosses inner dead zone.

            :param start_point: Starting TrajectoryWaypoint.
            :param end_point: Target destination TrajectoryWaypoint.
            :return: True if segment crosses dead zone, False otherwise.
            :exceptions: None.
        '''

    def is_point_in_dead_zone(
        self,
        point: TrajectoryWaypoint,
    ) -> bool:
        '''
            Determines whether the given waypoint resides inside the dead zone.

            :param point: TrajectoryWaypoint to check.
            :return: True if coordinates reside inside dead zone, False otherwise.
            :exceptions: None.
        '''

    def plan_detour(
        self,
        start_point: TrajectoryWaypoint,
        end_point: TrajectoryWaypoint,
    ) -> list[TrajectoryWaypoint]:
        '''
            Plans safe tangential bypass detour around central dead zone.

            :param start_point: Starting TrajectoryWaypoint.
            :param end_point: Target destination TrajectoryWaypoint.
            :return: List of collision-free intermediate detour Waypoints to destination.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Version string.
            :exceptions: None.
        '''
