# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Infrastructure adapter delegating dead zone avoidance and detour planning to scaralang.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneAvoidanceAdapter:
    '''
        Adapter wrapping scaralang dead zone validator and bypass planner.

        It defines:

            :attributes:
                | _validator - Injected scaralang dead zone validator port.
                | _planner - Injected scaralang dead zone bypass planner port.
            :methods:
                | __init__ - Initializes adapter with validator and planner collaborators.
                | crosses_dead_zone - Determines if segment traverses dead zone.
                | is_point_in_dead_zone - Checks if waypoint coordinates reside in dead zone.
                | plan_detour - Plans intermediate detour waypoints bypassing dead zone.
                | get_version - Returns adapter component version string.
    '''

    _validator: IDeadZoneValidator
    _planner: IDeadZoneBypassPlanner

    def __init__(
        self,
        *,
        validator: IDeadZoneValidator,
        planner: IDeadZoneBypassPlanner,
    ) -> None:
        '''
            Initializes adapter with injected scaralang avoidance services.

            :param validator: Injected IDeadZoneValidator instance.
            :param planner: Injected IDeadZoneBypassPlanner instance.
            :exceptions: None.
        '''
        self._validator: Final[IDeadZoneValidator] = validator
        self._planner: Final[IDeadZoneBypassPlanner] = planner

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
        p1: Point2D = Point2D(x=start_point.x, y=start_point.y)
        p2: Point2D = Point2D(x=end_point.x, y=end_point.y)

        return self._validator.is_segment_crossing_dead_zone(p1, p2)

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
        return self._validator.is_point_in_dead_zone(point.x, point.y)

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
        p1: Point2D = Point2D(x=start_point.x, y=start_point.y)
        p2: Point2D = Point2D(x=end_point.x, y=end_point.y)
        raw_detour: list[Waypoint] = self._planner.plan_bypass(
            p1,
            p2,
            z=end_point.z,
            speed=end_point.speed,
        )

        return [
            TrajectoryWaypoint(
                x=pt.x,
                y=pt.y,
                z=pt.z,
                phi=end_point.phi,
                speed=pt.speed,
                name=pt.name,
                command=pt.command,
            )
            for pt in raw_detour
        ]

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
