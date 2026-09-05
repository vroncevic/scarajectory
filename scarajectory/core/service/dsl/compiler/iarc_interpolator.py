# -*- coding: UTF-8 -*-

'''
Module
    iarc_interpolator.py
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
    Defines structural runtime-checkable protocol IArcInterpolator for circular arc segmentation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IArcInterpolator(Protocol):
    '''
        Structural protocol defining contract for circular arc Cartesian segmentation.

        It defines:

            :attributes:
                | None.
            :methods:
                | interpolate - Generates discrete points and tangent angles along circular arc.
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
