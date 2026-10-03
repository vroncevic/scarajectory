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
    Unit tests for ScaraDeadzoneCalculator and ScaraDeadzoneCalculatorFactory.
'''

from __future__ import annotations

from math import cos, pi, sqrt
from unittest import TestCase, main

from scarajectory.core.service.kinematics.iscara_deadzone_calculator import IScaraDeadzoneCalculator
from scarajectory.core.service.kinematics.scara_deadzone_calculator import ScaraDeadzoneCalculator
from scarajectory.core.service.kinematics.scara_deadzone_calculator_factory import ScaraDeadzoneCalculatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDeadzoneCalculator(TestCase):
    '''
        Test cases verifying ScaraDeadzoneCalculator mathematical operations and factory.
    '''

    def setUp(self) -> None:
        self.calculator: ScaraDeadzoneCalculator = (
            ScaraDeadzoneCalculatorFactory.create()
        )

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance against IScaraDeadzoneCalculator.
        '''
        self.assertIsInstance(self.calculator, IScaraDeadzoneCalculator)
        self.assertEqual(ScaraDeadzoneCalculatorFactory.get_version(), '1.0.4')

    def test_calculate_deadzone_radius_standard(self) -> None:
        '''
            Tests deadzone calculation with standard SCARA link lengths.
        '''
        l1: float = 150.0
        l2: float = 120.0
        j2_max: float = 2.530727
        expected_sq: float = l1 * l1 + l2 * l2 + 2.0 * l1 * l2 * cos(j2_max)
        expected_r: float = sqrt(expected_sq)

        sq: float = self.calculator.calculate_deadzone_radius_squared(l1, l2, j2_max)
        r: float = self.calculator.calculate_deadzone_radius(l1, l2, j2_max)

        self.assertAlmostEqual(sq, expected_sq, places=6)
        self.assertAlmostEqual(r, expected_r, places=6)

    def test_calculate_deadzone_fully_folded(self) -> None:
        '''
            Tests deadzone calculation when j2 is pi (fully folded back on itself).
        '''
        l1: float = 100.0
        l2: float = 60.0
        j2_max: float = pi
        # At pi, cos(pi) = -1, (l1 - l2)^2 = (100 - 60)^2 = 1600.0, r = 40.0
        sq: float = self.calculator.calculate_deadzone_radius_squared(l1, l2, j2_max)
        r: float = self.calculator.calculate_deadzone_radius(l1, l2, j2_max)

        self.assertAlmostEqual(sq, 1600.0, places=6)
        self.assertAlmostEqual(r, 40.0, places=6)

    def test_calculate_deadzone_clamps_negative_to_zero(self) -> None:
        '''
            Tests that calculation clamps negative values safely to zero.
        '''
        l1: float = 50.0
        l2: float = 50.0
        j2_max: float = pi
        # (50 - 50)^2 = 0
        sq: float = self.calculator.calculate_deadzone_radius_squared(l1, l2, j2_max)
        r: float = self.calculator.calculate_deadzone_radius(l1, l2, j2_max)

        self.assertEqual(sq, 0.0)
        self.assertEqual(r, 0.0)


if __name__ == '__main__':
    main()
