# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Coordinates shape discretization and dead zone avoidance planning for
    canvas shapes.
'''

from __future__ import annotations

from math import hypot
from typing import ClassVar, Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.circle import CircleGeometry

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.handler.coordinator.bundle import ShapePlanCoordinatorBundle
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ShapePlanCoordinator:
    '''
        Coordinates shape discretization and dead zone avoidance planning for canvas shapes.

        It defines:

            :attributes:
                | CIRCLE_MIN_RADIUS_MM - Minimum radius threshold in mm for circle insertion.
                | CIRCLE_DEFAULT_STEPS - Number of perimeter segments for circle discretization.
                | _store - Injected waypoint query and storage service.
                | _point_mutator - Active trajectory plan point mutator.
                | _bulk_mutator - Active trajectory plan bulk mutator.
                | _avoidance_adapter - Dead zone validation and query adapter.
                | _planner_adapter - Shape contour avoidance planner adapter.
                | _validator - Kinematic reachability validator.
            :methods:
                | __init__ - Initializes coordinator with injected bundle.
                | commit_point - Commits a single waypoint bypassing dead zone.
                | commit_line - Discretizes and commits straight line segment bypassing dead zone.
                | commit_rectangle - Discretizes and commits rectangular perimeter with bypass routing.
                | commit_circle - Discretizes and commits circular trajectory with bypass routing.
    '''

    CIRCLE_MIN_RADIUS_MM: ClassVar[float] = 5.0
    CIRCLE_DEFAULT_STEPS: ClassVar[int] = 16

    _store: IWaypointStore
    _point_mutator: IPlanPointMutator
    _bulk_mutator: IPlanBulkMutator
    _avoidance_adapter: IDeadZoneAvoidanceAdapter
    _planner_adapter: IShapePlannerAdapter
    _validator: ITrajectoryValidator

    def __init__(self, bundle: ShapePlanCoordinatorBundle) -> None:
        '''
            Initializes coordinator with injected collaborators bundle.

            :param bundle: Injected ShapePlanCoordinatorBundle instance.
            :exceptions: None.
        '''
        self._store: Final[IWaypointStore] = bundle.store
        self._point_mutator: Final[IPlanPointMutator] = bundle.point_mutator
        self._bulk_mutator: Final[IPlanBulkMutator] = bundle.bulk_mutator
        self._avoidance_adapter: Final[IDeadZoneAvoidanceAdapter] = (
            bundle.avoidance_adapter
        )
        self._planner_adapter: Final[IShapePlannerAdapter] = (
            bundle.planner_adapter
        )
        self._validator: Final[ITrajectoryValidator] = bundle.validator

    def commit_point(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Commits single point to the trajectory plan, bypassing dead zone if needed.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        new_pt: TrajectoryWaypoint = TrajectoryWaypoint(
            x=wx,
            y=wy,
            z=settings.default_z,
            phi=0.0,
            speed=settings.default_speed,
            name='',
            command='',
        )

        if (
            settings.enforce_deadzone
            and not self._validator.validate_point(new_pt).is_valid
        ):
            return

        if self._avoidance_adapter.is_point_in_dead_zone(new_pt):
            return

        if self._store.count > 0:
            last: TrajectoryWaypoint = self._store.waypoints[-1]

            if not self._avoidance_adapter.crosses_dead_zone(last, new_pt):
                self._point_mutator.add_point(new_pt)

                return

            detour_wps: list[TrajectoryWaypoint] = (
                self._avoidance_adapter.plan_detour(last, new_pt)
            )

            for pt in detour_wps[1:]:
                if (
                    settings.enforce_deadzone
                    and not self._validator.validate_point(pt).is_valid
                ):
                    return
                self._point_mutator.add_point(pt)

            return

        self._point_mutator.add_point(new_pt)

    def commit_line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits straight line segment to plan with dead zone detour routing.

            :param p1: Starting world coordinate tuple (x, y).
            :param p2: Ending world coordinate tuple (x, y).
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        x0, y0 = p1
        wx, wy = p2

        if hypot(wx - x0, wy - y0) > 1.0:
            p2_wp: TrajectoryWaypoint = TrajectoryWaypoint(
                x=wx,
                y=wy,
                z=settings.default_z,
                phi=0.0,
                speed=settings.default_speed,
                name='',
                command='',
            )

            if (
                settings.enforce_deadzone
                and not self._validator.validate_point(p2_wp).is_valid
            ):
                return

            if self._avoidance_adapter.is_point_in_dead_zone(p2_wp):
                return

            pt1: Point2D = Point2D(x=x0, y=y0)
            pt2: Point2D = Point2D(x=wx, y=wy)
            line_wps: list[TrajectoryWaypoint] = (
                self._planner_adapter.plan_contour(
                    [pt1, pt2],
                    z=settings.default_z,
                    speed=settings.default_speed,
                    closed=False,
                )
            )
            if settings.enforce_deadzone:
                for pt in line_wps:
                    if not self._validator.validate_point(pt).is_valid:
                        return

            self._bulk_mutator.set_waypoints(
                list(self._store.waypoints) + line_wps
            )

    def commit_rectangle(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits rectangular perimeter to plan with dead zone detour routing.

            :param p1: Starting corner world coordinate tuple (x, y).
            :param p2: Opposite corner world coordinate tuple (x, y).
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        x0, y0 = p1
        wx, wy = p2

        if abs(wx - x0) > 2.0 and abs(wy - y0) > 2.0:
            c1: Point2D = Point2D(x=x0, y=y0)
            c2: Point2D = Point2D(x=wx, y=y0)
            c3: Point2D = Point2D(x=wx, y=wy)
            c4: Point2D = Point2D(x=x0, y=wy)
            rect_wps: list[TrajectoryWaypoint] = (
                self._planner_adapter.plan_contour(
                    [c1, c2, c3, c4],
                    z=settings.default_z,
                    speed=settings.default_speed,
                    closed=True,
                )
            )
            if settings.enforce_deadzone:
                for pt in rect_wps:
                    if not self._validator.validate_point(pt).is_valid:
                        return

            self._bulk_mutator.set_waypoints(
                list(self._store.waypoints) + rect_wps
            )

    def commit_circle(
        self,
        center: tuple[float, float],
        boundary: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits circular trajectory to plan with dead zone detour routing.

            :param center: Center world coordinate tuple (x, y).
            :param boundary: Boundary world coordinate tuple (x, y).
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        x0, y0 = center
        wx, wy = boundary
        radius: float = hypot(wx - x0, wy - y0)

        if radius >= self.CIRCLE_MIN_RADIUS_MM:
            geom: CircleGeometry = CircleGeometry(
                center=Point2D(x=x0, y=y0),
                radius=radius,
                steps=self.CIRCLE_DEFAULT_STEPS,
                z=settings.default_z,
                speed=settings.default_speed,
            )
            circle_wps: list[TrajectoryWaypoint] = (
                self._planner_adapter.plan_circle(geom)
            )
            if settings.enforce_deadzone:
                for pt in circle_wps:
                    if not self._validator.validate_point(pt).is_valid:
                        return

            self._bulk_mutator.set_waypoints(
                list(self._store.waypoints) + circle_wps
            )
