# -*- coding: UTF-8 -*-

'''
Module
    driver_test.py
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
    Unit tests for DriverFaultDiagnostics immutable telemetry model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.driver import DriverFaultDiagnostics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DriverFaultDiagnosticsTestCase(TestCase):
    '''
        Tests for DriverFaultDiagnostics telemetry model.

        It defines:

            :methods:
                | test_driver_creation - Verifies attribute assignment during initialization.
                | test_driver_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_driver_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        driver = DriverFaultDiagnostics(
            stall_guard_flags=1,
            driver_fault_flags=2,
        )
        self.assertEqual(driver.stall_guard_flags, 1)
        self.assertEqual(driver.driver_fault_flags, 2)

    def test_driver_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen DriverFaultDiagnostics raises FrozenInstanceError.

            :exceptions: None.
        '''
        driver = DriverFaultDiagnostics(
            stall_guard_flags=0,
            driver_fault_flags=0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(driver, 'stall_guard_flags', 10)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical DriverFaultDiagnostics instances.

            :exceptions: None.
        '''
        d1 = DriverFaultDiagnostics(
            stall_guard_flags=1,
            driver_fault_flags=2,
        )
        d2 = DriverFaultDiagnostics(
            stall_guard_flags=1,
            driver_fault_flags=2,
        )
        self.assertEqual(d1, d2)


if __name__ == '__main__':
    main()
