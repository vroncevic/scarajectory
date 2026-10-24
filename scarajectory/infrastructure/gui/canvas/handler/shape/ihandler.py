# -*- coding: UTF-8 -*-

'''
Module
    ihandler.py
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
    Structural protocol for handling canvas geometric shape creation and
    plan commitment.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
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


@runtime_checkable
class ICanvasShapeHandler(Protocol):
    '''
        Structural protocol defining canvas waypoint generation and shape commitment port.

        It defines:

            :methods:
                | create_waypoint_at - Builds a TrajectoryWaypoint at given world coordinates.
                | create_relocated_waypoint - Builds updated TrajectoryWaypoint with relocated coordinates.
                | commit_point - Commits a single waypoint to the trajectory plan.
                | commit_shape - Dispatches shape commitment based on active tool mode.
    '''

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
        '''

    def create_relocated_waypoint(
        self,
        current: TrajectoryWaypoint,
        wx: float,
        wy: float,
    ) -> TrajectoryWaypoint:
        '''
            Builds updated TrajectoryWaypoint with relocated coordinates and preserved properties.

            :param current: Current TrajectoryWaypoint instance.
            :param wx: New world X coordinate.
            :param wy: New world Y coordinate.
            :return: Updated TrajectoryWaypoint object.
        '''

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
        '''

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
        '''
