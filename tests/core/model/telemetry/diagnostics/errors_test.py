# -*- coding: UTF-8 -*-

'''
Module
    errors_test.py
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
    Unit tests for FollowingErrorsDiagnostics immutable telemetry model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.errors import FollowingErrorsDiagnostics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FollowingErrorsDiagnosticsTestCase(TestCase):
    '''
        Tests for FollowingErrorsDiagnostics telemetry model.

        It defines:

            :methods:
                | test_errors_creation - Verifies attribute assignment during initialization.
                | test_errors_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_errors_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        errors = FollowingErrorsDiagnostics(
            j1=3,
            j2=1,
            z=0,
            j4=0,
        )
        self.assertEqual(errors.j1, 3)
        self.assertEqual(errors.j2, 1)
        self.assertEqual(errors.z, 0)
        self.assertEqual(errors.j4, 0)

    def test_errors_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen FollowingErrorsDiagnostics raises FrozenInstanceError.

            :exceptions: None.
        '''
        errors = FollowingErrorsDiagnostics(
            j1=0,
            j2=0,
            z=0,
            j4=0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(errors, 'j1', 10)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical FollowingErrorsDiagnostics instances.

            :exceptions: None.
        '''
        e1 = FollowingErrorsDiagnostics(
            j1=0,
            j2=0,
            z=0,
            j4=0,
        )
        e2 = FollowingErrorsDiagnostics(
            j1=0,
            j2=0,
            z=0,
            j4=0,
        )
        self.assertEqual(e1, e2)


if __name__ == '__main__':
    main()
