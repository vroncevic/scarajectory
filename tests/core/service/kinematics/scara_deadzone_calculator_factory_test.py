# -*- coding: UTF-8 -*-

'''
Module
    scara_deadzone_calculator_factory_test.py
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
    Unit tests for ScaraDeadzoneCalculatorFactory factory service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.kinematics.scara_deadzone_calculator import (
    ScaraDeadzoneCalculator,
)
from scarajectory.core.service.kinematics.scara_deadzone_calculator_factory import (
    ScaraDeadzoneCalculatorFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDeadzoneCalculatorFactoryTestCase(TestCase):
    '''
        Tests ScaraDeadzoneCalculatorFactory component instantiation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create - Verifies instantiation of ScaraDeadzoneCalculator.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies factory version string and create callable.'''
        self.assertEqual(ScaraDeadzoneCalculatorFactory.get_version(), '1.0.4')
        self.assertTrue(hasattr(ScaraDeadzoneCalculatorFactory, 'create'))
        self.assertTrue(callable(ScaraDeadzoneCalculatorFactory.create))

    def test_factory_create(self) -> None:
        '''Verifies create returns an instance of ScaraDeadzoneCalculator.'''
        calculator = ScaraDeadzoneCalculatorFactory.create()
        self.assertIsInstance(calculator, ScaraDeadzoneCalculator)


if __name__ == '__main__':
    main()
