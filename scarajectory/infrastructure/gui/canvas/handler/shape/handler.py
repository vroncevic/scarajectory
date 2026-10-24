# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
    Handles discretization and commitment of geometric CAD shapes to trajectory
    plan.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.canvas.handler.coordinator.icoordinator import IShapePlanCoordinator
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasShapeHandler:
    '''
        Discretizes geometric shapes and commits generated waypoints to trajectory plan.

        It defines:

            :attributes:
                | _coordinator - Injected shape plan and avoidance coordinator.
            :methods:
                | __init__ - Initializes handler with injected shape plan coordinator.
                | create_waypoint_at - Builds a TrajectoryWaypoint at given world coordinates.
                | create_relocated_waypoint - Builds updated TrajectoryWaypoint with relocated coordinates.
                | commit_point - Commits a single waypoint to the trajectory plan.
                | commit_shape - Dispatches shape commitment based on active tool mode.
    '''

    _coordinator: IShapePlanCoordinator

    def __init__(
        self,
        *,
        coordinator: IShapePlanCoordinator,
    ) -> None:
        '''
            Initializes shape handler with injected shape plan coordinator.

            :param coordinator: Injected IShapePlanCoordinator instance.
            :exceptions: None.
        '''
        self._coordinator: Final[IShapePlanCoordinator] = coordinator

    def create_waypoint_at(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> TrajectoryWaypoint:
        '''
            Builds a TrajectoryWaypoint at given world coordinates.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :return: New TrajectoryWaypoint instance.
            :exceptions: None.
        '''
        return TrajectoryWaypoint(
            x=wx,
            y=wy,
            z=settings.default_z,
            phi=0.0,
            speed=settings.default_speed,
            name='',
            command='',
        )

    def create_relocated_waypoint(
        self,
        current: TrajectoryWaypoint,
        wx: float,
        wy: float,
    ) -> TrajectoryWaypoint:
        '''
            Builds updated TrajectoryWaypoint retaining non-coordinate properties.

            :param current: Reference TrajectoryWaypoint.
            :param wx: New world X coordinate.
            :param wy: New world Y coordinate.
            :return: Relocated TrajectoryWaypoint instance.
            :exceptions: None.
        '''
        return TrajectoryWaypoint(
            x=wx,
            y=wy,
            z=current.z,
            phi=current.phi,
            speed=current.speed,
            name=current.name,
            command=current.command,
        )

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
        self._coordinator.commit_point(wx, wy, settings)

    def commit_shape(
        self,
        tool_mode: CanvasToolMode,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Dispatches shape commitment based on active tool mode.

            :param tool_mode: Active CanvasToolMode.
            :param p1: Start world coordinate tuple (x, y).
            :param p2: End world coordinate tuple (x, y).
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        match tool_mode:
            case CanvasToolMode.POINT:
                self._coordinator.commit_point(p2[0], p2[1], settings)
            case CanvasToolMode.LINE:
                self._coordinator.commit_line(p1, p2, settings)
            case CanvasToolMode.CIRCLE:
                self._coordinator.commit_circle(p1, p2, settings)
            case CanvasToolMode.RECTANGLE:
                self._coordinator.commit_rectangle(p1, p2, settings)
            case _:
                pass
