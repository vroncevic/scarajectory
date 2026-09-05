# -*- coding: UTF-8 -*-

'''
Module
    arc_interpolator.py
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
    Implementation of IArcInterpolator calculating smooth discrete arc segments.
'''

from __future__ import annotations

from math import atan2, ceil, cos, degrees, hypot, pi, radians, sin

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcInterpolator:
    '''
        Mathematical interpolator segmenting circular arcs into linear waypoints.

        It defines:

            :attributes:
                | None.
            :methods:
                | interpolate - Segments circular arc into discrete coordinates and tangent angles.
    '''

    def interpolate(
        self,
        *,
        start_x: float,
        start_y: float,
        target_x: float,
        target_y: float,
        offset_i: float,
        offset_j: float,
        is_clockwise: bool,
        step_angle_deg: float = 5.0,
    ) -> tuple[tuple[float, float, float], ...]:
        '''
            Segments circular arc into intermediate coordinates and tangent angles.

            :param start_x: Starting arc X coordinate.
            :param start_y: Starting arc Y coordinate.
            :param target_x: Destination arc X coordinate.
            :param target_y: Destination arc Y coordinate.
            :param offset_i: Center X offset from start.
            :param offset_j: Center Y offset from start.
            :param is_clockwise: True for ARC_CW, False for ARC_CCW.
            :param step_angle_deg: Angular discretization step size in degrees.
            :return: Tuple of (px, py, tangent_deg) tuples.
        '''
        center_x = start_x + offset_i
        center_y = start_y + offset_j
        radius = hypot(offset_i, offset_j)

        if radius < 1e-4:
            return ()

        angle_start = atan2(start_y - center_y, start_x - center_x)
        angle_end = atan2(target_y - center_y, target_x - center_x)

        if is_clockwise:
            if angle_end >= angle_start:
                angle_end -= 2.0 * pi
        else:
            if angle_end <= angle_start:
                angle_end += 2.0 * pi

        total_sweep = abs(angle_end - angle_start)
        step_rad = radians(max(0.5, step_angle_deg))
        num_segments = max(4, int(ceil(total_sweep / step_rad)))

        points: list[tuple[float, float, float]] = []
        for i in range(1, num_segments + 1):
            t = i / float(num_segments)
            cur_angle = angle_start + t * (angle_end - angle_start)
            px = center_x + radius * cos(cur_angle)
            py = center_y + radius * sin(cur_angle)

            tangent_rad = cur_angle - (
                pi / 2.0 if is_clockwise else -pi / 2.0
            )
            tangent_deg = (degrees(tangent_rad) + 180.0) % 360.0 - 180.0
            points.append((px, py, tangent_deg))

        return tuple(points)
