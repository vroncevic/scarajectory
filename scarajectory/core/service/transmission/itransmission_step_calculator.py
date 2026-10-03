# -*- coding: UTF-8 -*-

'''
Module
    itransmission_step_calculator.py
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
    Defines structural protocol ITransmissionStepCalculator for transmission step calculations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITransmissionStepCalculator(Protocol):
    '''
        Structural protocol defining motor step calculations from transmission parameters.

        It defines:

            :methods:
                | revolute_steps - Computes step counts for a revolute joint.
                | linear_z_steps - Computes step counts for the linear Z axis.
                | calculate_duration_us - Computes segment duration in microseconds.
    '''

    def revolute_steps(self, *, angle_rad: float, gear_ratio: float) -> int:
        '''
            Computes step counts for a revolute joint given angle and gear ratio.

            :param angle_rad: Joint angle in radians.
            :param gear_ratio: Joint gear ratio.
            :return: Computed integer step count.
        '''

    def linear_z_steps(self, *, z_mm: float) -> int:
        '''
            Computes step counts for the linear Z axis given displacement in millimeters.

            :param z_mm: Linear displacement in millimeters.
            :return: Computed integer step count.
        '''

    def calculate_duration_us(self, *, speed: float) -> int:
        '''
            Computes segment duration in microseconds based on target speed.

            :param speed: Target speed scalar.
            :return: Duration in microseconds.
        '''
