# -*- coding: UTF-8 -*-

'''
Module
    scara_deadzone_calculator.py
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
    Domain service for computing SCARA robot workspace inner deadzone boundaries.
'''

from __future__ import annotations

from math import cos, sqrt

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDeadzoneCalculator:
    '''
        Domain service calculating SCARA workspace inner deadzone geometry from arm link parameters.

        It defines:

            :methods:
                | calculate_deadzone_radius - Calculates inner deadzone radius in millimeters.
                | calculate_deadzone_radius_squared - Calculates squared inner deadzone radius.
    '''

    def calculate_deadzone_radius(
        self,
        l1: float,
        l2: float,
        j2_max_rad: float,
    ) -> float:
        '''
            Calculates inner workspace deadzone radius boundary in millimeters.

            :param l1: Length of primary arm link in millimeters.
            :param l2: Length of secondary forearm link in millimeters.
            :param j2_max_rad: Maximum joint 2 angle limit in radians.
            :return: Minimum unreachable inner radius in millimeters.
            :exceptions: None.
        '''
        return sqrt(self.calculate_deadzone_radius_squared(l1, l2, j2_max_rad))

    def calculate_deadzone_radius_squared(
        self,
        l1: float,
        l2: float,
        j2_max_rad: float,
    ) -> float:
        '''
            Calculates squared inner workspace deadzone radius.

            :param l1: Length of primary arm link in millimeters.
            :param l2: Length of secondary forearm link in millimeters.
            :param j2_max_rad: Maximum joint 2 angle limit in radians.
            :return: Squared inner deadzone radius.
            :exceptions: None.
        '''
        r_dead_sq: float = l1 * l1 + l2 * l2 + 2.0 * l1 * l2 * cos(j2_max_rad)
        return max(0.0, r_dead_sq)
