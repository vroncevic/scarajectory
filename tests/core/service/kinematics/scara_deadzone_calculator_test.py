# -*- coding: UTF-8 -*-

'''
Module
    scara_deadzone_calculator_test.py
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
    Unit tests for ScaraDeadzoneCalculator domain service.
'''

from __future__ import annotations

from math import isclose, pi
from unittest import TestCase, main

from scarajectory.core.service.kinematics.scara_deadzone_calculator import (
    ScaraDeadzoneCalculator,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDeadzoneCalculatorTestCase(TestCase):
    '''
        Tests ScaraDeadzoneCalculator geometric calculations.

        It defines:

            :methods:
                | test_calculate_deadzone_radius_positive - Verifies radius at maximum fold angle.
                | test_calculate_deadzone_radius_zero_boundary - Verifies zero boundary fold.
                | test_calculate_deadzone_radius_acute_angle - Verifies radius at zero angle extension.
    '''

    def test_calculate_deadzone_radius_positive(self) -> None:
        '''Verifies standard arm link lengths inner deadzone calculation.'''
        calculator = ScaraDeadzoneCalculator()
        sq = calculator.calculate_deadzone_radius_squared(150.0, 120.0, pi)
        rad = calculator.calculate_deadzone_radius(150.0, 120.0, pi)
        self.assertTrue(isclose(sq, 900.0, rel_tol=1e-5))
        self.assertTrue(isclose(rad, 30.0, rel_tol=1e-5))

    def test_calculate_deadzone_radius_zero_boundary(self) -> None:
        '''Verifies symmetric arm link lengths fold completely to origin.'''
        calculator = ScaraDeadzoneCalculator()
        sq = calculator.calculate_deadzone_radius_squared(100.0, 100.0, pi)
        rad = calculator.calculate_deadzone_radius(100.0, 100.0, pi)
        self.assertTrue(isclose(sq, 0.0, abs_tol=1e-5))
        self.assertTrue(isclose(rad, 0.0, abs_tol=1e-5))

    def test_calculate_deadzone_radius_acute_angle(self) -> None:
        '''Verifies fully extended arm link lengths computation.'''
        calculator = ScaraDeadzoneCalculator()
        sq = calculator.calculate_deadzone_radius_squared(150.0, 120.0, 0.0)
        rad = calculator.calculate_deadzone_radius(150.0, 120.0, 0.0)
        self.assertTrue(isclose(sq, 72900.0, rel_tol=1e-5))
        self.assertTrue(isclose(rad, 270.0, rel_tol=1e-5))


if __name__ == '__main__':
    main()
