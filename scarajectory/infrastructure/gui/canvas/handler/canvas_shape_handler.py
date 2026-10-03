# -*- coding: UTF-8 -*-

'''
Module
    canvas_shape_handler.py
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
    Handles discretization and commitment of geometric CAD shapes to trajectory plan.
'''

from __future__ import annotations

from math import hypot
from typing import ClassVar, Final

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.circle_geometry import CircleGeometry
from scaralang.core.service.trajectory.discretization.ishape_discretizer import IShapeDiscretizer
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.itrajectory_mutable import ITrajectoryMutable
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasShapeHandler:
    '''
        Discretizes geometric shapes and commits generated waypoints to trajectory plan.

        It defines:

            :attributes:
                | CIRCLE_MIN_RADIUS_MM - Minimum radius threshold in mm for inserting circle shapes.
                | CIRCLE_DEFAULT_STEPS - Number of waypoint segments used for circle discretization.
                | _plan - Active trajectory plan interface.
                | _discretizer - Geometric discretization service.
            :methods:
                | __init__ - Initializes handler with injected plan and discretizer.
                | create_waypoint_at - Builds a Waypoint at given world coordinates.
                | commit_point - Commits a single waypoint to the trajectory plan.
                | commit_line - Discretizes and commits straight line segment to plan.
                | commit_circle - Discretizes and commits circular trajectory to plan.
                | commit_rectangle - Discretizes and commits rectangular perimeter to plan.
                | commit_shape - Dispatches shape commitment based on active tool mode.
    '''

    CIRCLE_MIN_RADIUS_MM: ClassVar[float] = 5.0
    CIRCLE_DEFAULT_STEPS: ClassVar[int] = 16

    _plan: ITrajectoryMutable
    _discretizer: IShapeDiscretizer

    def __init__(
        self,
        plan: ITrajectoryMutable,
        discretizer: IShapeDiscretizer,
    ) -> None:
        '''
            Initializes shape handler with injected plan and discretizer.

            :param plan: Active ITrajectoryMutable instance.
            :param discretizer: IShapeDiscretizer instance.
            :exceptions: None.
        '''
        self._plan: Final[ITrajectoryMutable] = plan
        self._discretizer: Final[IShapeDiscretizer] = discretizer

    def create_waypoint_at(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> Waypoint:
        '''
            Builds a Waypoint at given world coordinates.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :return: New Waypoint instance.
            :exceptions: None.
        '''
        return Waypoint(
            x=wx,
            y=wy,
            z=settings.default_z,
            phi=0.0,
            speed=settings.default_speed,
            name='',
            command='',
        )

    def commit_point(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Commits single point to the trajectory plan.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        self._plan.add_point(self.create_waypoint_at(wx, wy, settings))

    def commit_line(
        self,
        x0: float,
        y0: float,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits straight line segment to plan.

            :param x0: Starting world X coordinate.
            :param y0: Starting world Y coordinate.
            :param wx: Ending world X coordinate.
            :param wy: Ending world Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        if hypot(wx - x0, wy - y0) > 1.0:
            line_pts = self._discretizer.discretize_line(
                Point2D(x=x0, y=y0),
                Point2D(x=wx, y=wy),
                z=settings.default_z,
                speed=settings.default_speed,
            )
            self._plan.set_waypoints(list(self._plan.waypoints) + line_pts)

    def commit_circle(
        self,
        x0: float,
        y0: float,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits circular trajectory to plan.

            :param x0: Center world X coordinate.
            :param y0: Center world Y coordinate.
            :param wx: Boundary world X coordinate.
            :param wy: Boundary world Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        radius: float = hypot(wx - x0, wy - y0)

        if radius >= self.CIRCLE_MIN_RADIUS_MM:
            geom = CircleGeometry(
                center=Point2D(x=x0, y=y0),
                radius=radius,
                steps=self.CIRCLE_DEFAULT_STEPS,
                z=settings.default_z,
                speed=settings.default_speed,
            )
            circle_pts = self._discretizer.discretize_circle(geometry=geom)
            self._plan.set_waypoints(list(self._plan.waypoints) + circle_pts)

    def commit_rectangle(
        self,
        x0: float,
        y0: float,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits rectangular perimeter to plan.

            :param x0: Starting corner world X coordinate.
            :param y0: Starting corner world Y coordinate.
            :param wx: Opposite corner world X coordinate.
            :param wy: Opposite corner world Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        if abs(wx - x0) > 2.0 and abs(wy - y0) > 2.0:
            rect_pts = self._discretizer.discretize_rectangle(
                Point2D(x=x0, y=y0),
                Point2D(x=wx, y=wy),
                z=settings.default_z,
                speed=settings.default_speed,
            )
            self._plan.set_waypoints(list(self._plan.waypoints) + rect_pts)

    def commit_shape(
        self,
        tool_mode: CanvasToolMode,
        x0: float,
        y0: float,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Dispatches shape commitment based on active tool mode.

            :param tool_mode: Active CanvasToolMode.
            :param x0: Start world X coordinate.
            :param y0: Start world Y coordinate.
            :param wx: Current world X coordinate.
            :param wy: Current world Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        match tool_mode:
            case CanvasToolMode.POINT:
                self.commit_point(wx, wy, settings)
            case CanvasToolMode.LINE:
                self.commit_line(x0, y0, wx, wy, settings)
            case CanvasToolMode.CIRCLE:
                self.commit_circle(x0, y0, wx, wy, settings)
            case CanvasToolMode.RECTANGLE:
                self.commit_rectangle(x0, y0, wx, wy, settings)
            case _:
                pass
