# -*- coding: UTF-8 -*-

'''
Module
    driver_factory_test.py
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
    Unit tests for DriverFaultDiagnosticsFactory domain factory service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.driver import DriverFaultDiagnostics
from scarajectory.core.service.telemetry.diagnostics.driver_factory import DriverFaultDiagnosticsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DriverFaultDiagnosticsFactoryTestCase(TestCase):
    '''
        Tests for DriverFaultDiagnosticsFactory component.

        It defines:

            :methods:
                | test_create_driver_fault_diagnostics - Verifies model creation.
                | test_get_version - Verifies factory version accessor string.
    '''

    def test_create_driver_fault_diagnostics(self) -> None:
        '''
            Verifies driver fault diagnostics model creation.

            :exceptions: None.
        '''
        model = DriverFaultDiagnosticsFactory.create(
            stall_guard_flags=1,
            driver_fault_flags=2,
        )
        self.assertIsInstance(model, DriverFaultDiagnostics)
        self.assertEqual(model.stall_guard_flags, 1)
        self.assertEqual(model.driver_fault_flags, 2)

    def test_get_version(self) -> None:
        '''
            Verifies factory version accessor string.

            :exceptions: None.
        '''
        self.assertEqual(DriverFaultDiagnosticsFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
