# -*- coding: UTF-8 -*-

'''
Module
    icoordinator.py
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
    Structural protocol for coordinating geometric shape discretization and
    plan commitment.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

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
class IShapePlanCoordinator(Protocol):
    '''
        Structural protocol defining shape commitment and avoidance coordination port.

        It defines:

            :methods:
                | commit_point - Commits a single waypoint bypassing dead zone.
                | commit_line - Discretizes and commits straight line segment bypassing dead zone.
                | commit_rectangle - Discretizes and commits rectangular perimeter with bypass routing.
                | commit_circle - Discretizes and commits circular trajectory with bypass routing.
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
        '''

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
        '''

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
        '''
