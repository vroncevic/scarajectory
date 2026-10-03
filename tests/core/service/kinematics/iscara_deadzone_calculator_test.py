# -*- coding: UTF-8 -*-

'''
Module
    iscara_deadzone_calculator_test.py
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
    Unit tests for IScaraDeadzoneCalculator protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.kinematics.iscara_deadzone_calculator import (
    IScaraDeadzoneCalculator,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingDeadzoneCalculatorStub:
    '''Conforming stub satisfying IScaraDeadzoneCalculator protocol.'''

    def calculate_deadzone_radius(
        self,
        l1: float,
        l2: float,
        j2_max_rad: float,
    ) -> float:
        '''Calculates deadzone radius.'''
        _ = (l1, l2, j2_max_rad)
        return 10.0

    def calculate_deadzone_radius_squared(
        self,
        l1: float,
        l2: float,
        j2_max_rad: float,
    ) -> float:
        '''Calculates squared deadzone radius.'''
        _ = (l1, l2, j2_max_rad)
        return 100.0


class IncompleteDeadzoneCalculatorStub:
    '''Non-conforming stub missing calculate_deadzone_radius_squared.'''

    def calculate_deadzone_radius(
        self,
        l1: float,
        l2: float,
        j2_max_rad: float,
    ) -> float:
        '''Calculates deadzone radius.'''
        _ = (l1, l2, j2_max_rad)
        return 10.0

    def dummy_method(self) -> None:
        '''Dummy placeholder to satisfy class method count.'''


class IScaraDeadzoneCalculatorTestCase(TestCase):
    '''
        Tests IScaraDeadzoneCalculator runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
                | test_protocol_methods - Verifies protocol defines required methods.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IScaraDeadzoneCalculator protocol.'''
        stub = ConformingDeadzoneCalculatorStub()
        self.assertIsInstance(stub, IScaraDeadzoneCalculator)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails protocol check.'''
        stub = IncompleteDeadzoneCalculatorStub()
        self.assertNotIsInstance(stub, IScaraDeadzoneCalculator)

    def test_protocol_methods(self) -> None:
        '''Verifies protocol defines expected method attributes.'''
        for method_name in (
            'calculate_deadzone_radius',
            'calculate_deadzone_radius_squared',
        ):
            self.assertTrue(hasattr(IScaraDeadzoneCalculator, method_name))


if __name__ == '__main__':
    main()
