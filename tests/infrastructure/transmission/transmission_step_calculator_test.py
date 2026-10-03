# -*- coding: UTF-8 -*-

'''
Module
    transmission_step_calculator_test.py
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
    Unit tests for TransmissionStepCalculator and TransmissionStepCalculatorFactory.
'''

from __future__ import annotations

from math import pi
from unittest import TestCase, main

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.infrastructure.transmission.transmission_step_calculator import TransmissionStepCalculator
from scarajectory.infrastructure.transmission.transmission_step_calculator_factory import TransmissionStepCalculatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransmissionStepCalculator(TestCase):
    '''
        Test suite verifying step calculation logic and factory construction.

        It defines:

            :methods:
                | setUp - Prepares transmission parameters fixture.
                | test_revolute_steps - Verifies revolute step conversions.
                | test_linear_z_steps - Verifies linear displacement step conversions.
                | test_calculate_duration_us - Verifies segment timing calculations.
                | test_factory_creation - Verifies factory instantiation.
    '''

    def setUp(self) -> None:
        '''
            Prepares transmission parameters fixture.
        '''
        self._transmission = TransmissionParameters(
            steps_per_rev=200,
            microstepping=16,
            gear_ratio_j1=4.0,
            gear_ratio_j2=4.0,
            gear_ratio_j4=2.0,
            leadscrew_pitch_z=8.0,
        )
        self._calc = TransmissionStepCalculator(transmission=self._transmission)

    def test_revolute_steps(self) -> None:
        '''
            Verifies revolute step calculations for given angles.
        '''
        # steps_per_rad = (200 * 16 * 4.0) / (2 * pi) = 12800 / (2 * pi) ~ 2037.18
        # For pi radians: round(pi * (12800 / (2*pi))) = 6400
        steps = self._calc.revolute_steps(angle_rad=pi, gear_ratio=4.0)
        self.assertEqual(steps, 6400)

        zero_steps = self._calc.revolute_steps(angle_rad=0.0, gear_ratio=4.0)
        self.assertEqual(zero_steps, 0)

    def test_linear_z_steps(self) -> None:
        '''
            Verifies linear Z step calculations for given displacements.
        '''
        # steps_per_mm = (200 * 16) / 8.0 = 400 steps/mm
        # 10 mm -> 4000 steps
        steps = self._calc.linear_z_steps(z_mm=10.0)
        self.assertEqual(steps, 4000)

    def test_calculate_duration_us(self) -> None:
        '''
            Verifies microsecond duration calculation from speed.
        '''
        duration = self._calc.calculate_duration_us(speed=100.0)
        self.assertEqual(duration, 10000)

        min_duration = self._calc.calculate_duration_us(speed=10000.0)
        self.assertEqual(min_duration, 1000)

    def test_factory_creation(self) -> None:
        '''
            Verifies TransmissionStepCalculatorFactory instantiates calculator correctly.
        '''
        calc = TransmissionStepCalculatorFactory.create(transmission=self._transmission)
        self.assertIsInstance(calc, TransmissionStepCalculator)


if __name__ == '__main__':
    main()
