# -*- coding: UTF-8 -*-

'''
Module
    trajectory_metrics.py
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
    Defines TrajectoryMetrics computing motion distance, timing, and waypoint geometric metrics.
'''

from __future__ import annotations

from collections.abc import Sequence
from math import hypot, sqrt

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryMetrics:
    '''
        Computes motion distance, planar radial offsets, and duration metrics for trajectory plans.

        It defines:

            :methods:
                | distance_between - Computes 3D Euclidean distance between two waypoints.
                | radial_distance - Calculates planar radial distance from robot base for a waypoint.
                | calculate_distance - Computes total 3D Cartesian distance along the path.
                | calculate_duration - Computes estimated execution duration based on speeds.
    '''

    @classmethod
    def distance_between(cls, p1: Waypoint, p2: Waypoint) -> float:
        '''
            Computes 3D Euclidean distance between two waypoints.

            :param p1: Source waypoint.
            :param p2: Destination waypoint.
            :return: 3D distance in mm.
        '''
        dx: float = p2.x - p1.x
        dy: float = p2.y - p1.y
        dz: float = p2.z - p1.z

        return sqrt(dx * dx + dy * dy + dz * dz)

    @classmethod
    def radial_distance(cls, point: Waypoint) -> float:
        '''
            Calculates planar radial distance from robot base r = sqrt(x^2 + y^2).

            :param point: Target waypoint.
            :return: Radial distance in mm.
        '''
        return hypot(point.x, point.y)

    @classmethod
    def calculate_distance(cls, waypoints: Sequence[Waypoint]) -> float:
        '''
            Computes total 3D Cartesian distance along the path in mm.

            :param waypoints: Sequence of waypoints.
            :return: Cumulative distance in mm.
        '''
        if len(waypoints) < 2:
            return 0.0

        total: float = 0.0

        for i in range(len(waypoints) - 1):
            total += cls.distance_between(waypoints[i], waypoints[i + 1])

        return total

    @classmethod
    def calculate_duration(cls, waypoints: Sequence[Waypoint]) -> float:
        '''
            Computes estimated execution duration based on waypoint speeds in seconds.

            :param waypoints: Sequence of waypoints.
            :return: Estimated duration in seconds.
        '''
        if len(waypoints) < 2:
            return 0.0

        total_sec: float = 0.0

        for i in range(len(waypoints) - 1):
            dist: float = cls.distance_between(waypoints[i], waypoints[i + 1])
            spd: float = max(1.0, waypoints[i + 1].speed)
            total_sec += dist / spd

        return total_sec
