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
    Interface protocol for shape-based contour and circle avoidance planning.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.circle import CircleGeometry

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
class IShapePlannerAdapter(Protocol):
    '''
        Structural protocol defining shape-based contour and circle avoidance planning.

        It defines:

            :methods:
                | plan_contour - Computes collision-free contour waypoints around dead zone.
                | plan_circle - Computes collision-free circular perimeter waypoints around dead zone.
                | get_version - Returns adapter component version string.
    '''

    def plan_contour(
        self,
        points: Sequence[Point2D],
        *,
        z: float,
        speed: float,
        closed: bool = True,
    ) -> list[TrajectoryWaypoint]:
        '''
            Plans safe contour waypoints bypassing central singularity dead zone.

            :param points: Sequence of Point2D contour vertices.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :param closed: True if last vertex connects to first vertex, False otherwise.
            :return: List of collision-free Waypoints including spliced detour arcs.
            :exceptions: None.
        '''

    def plan_circle(
        self,
        geometry: CircleGeometry,
    ) -> list[TrajectoryWaypoint]:
        '''
            Plans safe circular perimeter waypoints bypassing central dead zone.

            :param geometry: CircleGeometry parameter model containing coordinates, radius, steps, z, speed.
            :return: List of collision-free Waypoints along circle perimeter.
        '''

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Version string.
            :exceptions: None.
        '''
