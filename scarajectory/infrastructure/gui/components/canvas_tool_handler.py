# -*- coding: UTF-8 -*-

'''
Module
    canvas_tool_handler.py
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
    CAD tool shape discretization, point sampling and hit-testing operations.
'''

from __future__ import annotations

import math
from typing import Sequence

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasToolHandler:
    '''
        Geometric discretization and spatial calculation engine for interactive CAD tools.

        It defines:

            :methods:
                | discretize_line - Generates linear segment start and end waypoints.
                | discretize_circle - Generates circle perimeter waypoints.
                | discretize_rectangle - Generates 4 corner waypoints of rectangle boundary.
                | find_hit_index - Finds nearest waypoint index matching cursor hit-radius.
                | is_freehand_distance_met - Checks if cursor has moved beyond minimum freehand threshold.
    '''

    @classmethod
    def discretize_line(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings
    ) -> list[Waypoint]:
        '''
            Generates start and end waypoints of straight linear segment.

            :param p1: Start point (x, y) coordinate tuple in mm.
            :param p2: End point (x, y) coordinate tuple in mm.
            :param settings: Active CanvasSettings.
            :return: List of Waypoint instances.
            :exceptions: None.
        '''
        return [
            Waypoint(x=p1[0], y=p1[1], z=settings.default_z, phi=0.0, speed=settings.default_speed),
            Waypoint(x=p2[0], y=p2[1], z=settings.default_z, phi=0.0, speed=settings.default_speed)
        ]

    @classmethod
    def discretize_circle(
        cls,
        center: tuple[float, float],
        radius: float,
        steps: int,
        settings: CanvasSettings
    ) -> list[Waypoint]:
        '''
            Generates circle perimeter waypoints.

            :param center: Center (x, y) coordinate tuple in mm.
            :param radius: Circle radius in mm.
            :param steps: Discretization step count.
            :param settings: Active CanvasSettings.
            :return: List of Waypoint instances.
            :exceptions: None.
        '''
        pts: list[Waypoint] = []

        for i in range(steps + 1):
            angle: float = 2.0 * math.pi * (i / steps)
            px: float = center[0] + radius * math.cos(angle)
            py: float = center[1] + radius * math.sin(angle)
            pts.append(Waypoint(x=px, y=py, z=settings.default_z, phi=0.0, speed=settings.default_speed))

        return pts

    @classmethod
    def discretize_rectangle(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings
    ) -> list[Waypoint]:
        '''
            Generates 4 corner waypoints of rectangle boundary with closing start waypoint.

            :param p1: Initial corner (x, y) tuple in mm.
            :param p2: Opposite corner (x, y) tuple in mm.
            :param settings: Active CanvasSettings.
            :return: List of Waypoint instances.
            :exceptions: None.
        '''
        return [
            Waypoint(x=p1[0], y=p1[1], z=settings.default_z, phi=0.0, speed=settings.default_speed),
            Waypoint(x=p2[0], y=p1[1], z=settings.default_z, phi=0.0, speed=settings.default_speed),
            Waypoint(x=p2[0], y=p2[1], z=settings.default_z, phi=0.0, speed=settings.default_speed),
            Waypoint(x=p1[0], y=p2[1], z=settings.default_z, phi=0.0, speed=settings.default_speed),
            Waypoint(x=p1[0], y=p1[1], z=settings.default_z, phi=0.0, speed=settings.default_speed)
        ]

    @classmethod
    def find_hit_index(
        cls,
        waypoints: Sequence[Waypoint],
        wx: float,
        wy: float,
        max_radius: float
    ) -> int:
        '''
            Finds nearest waypoint index matching cursor hit-radius.

            :param waypoints: Sequence of Waypoints.
            :param wx: Cursor world X coordinate.
            :param wy: Cursor world Y coordinate.
            :param max_radius: Maximum hit-test radius in mm.
            :return: Waypoint index or -1 if no hit.
            :exceptions: None.
        '''
        best_idx: int = -1
        best_dist: float = max_radius

        for idx, pt in enumerate(waypoints):
            dist: float = math.hypot(pt.x - wx, pt.y - wy)

            if dist < best_dist:
                best_dist = dist
                best_idx = idx

        return best_idx

    @classmethod
    def is_freehand_distance_met(
        cls,
        last_pt: Waypoint,
        wx: float,
        wy: float,
        min_dist: float
    ) -> bool:
        '''
            Checks if cursor has moved beyond minimum freehand threshold.

            :param last_pt: Last sampled Waypoint.
            :param wx: Current world X.
            :param wy: Current world Y.
            :param min_dist: Minimum distance threshold in mm.
            :return: True if distance met, False otherwise.
            :exceptions: None.
        '''
        return math.hypot(wx - last_pt.x, wy - last_pt.y) >= min_dist
