# -*- coding: UTF-8 -*-

'''
Module
    icanvas_waypoint_builder.py
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
    Defines structural protocol ICanvasWaypointBuilder for interactive waypoint instantiation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvasWaypointBuilder(Protocol):
    '''
        Structural protocol for constructing and relocating waypoints on canvas.

        It defines:

            :methods:
                | create_waypoint_at - Builds a new Waypoint at world coordinates.
                | create_relocated_waypoint - Builds updated Waypoint retaining existing properties.
    '''

    def create_waypoint_at(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> Waypoint:
        '''
            Builds a new Waypoint at given world coordinates.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :return: Instantiated Waypoint object.
            :exceptions: None.
        '''

    def create_relocated_waypoint(
        self,
        current: Waypoint,
        wx: float,
        wy: float,
    ) -> Waypoint:
        '''
            Builds updated Waypoint with relocated coordinates and preserved properties.

            :param current: Current Waypoint instance.
            :param wx: New world X coordinate.
            :param wy: New world Y coordinate.
            :return: Updated Waypoint object.
            :exceptions: None.
        '''
