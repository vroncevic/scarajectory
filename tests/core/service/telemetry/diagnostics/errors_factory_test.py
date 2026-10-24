# -*- coding: UTF-8 -*-

'''
Module
    errors_factory_test.py
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
    Unit tests for FollowingErrorsDiagnosticsFactory domain factory service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.errors import FollowingErrorsDiagnostics
from scarajectory.core.service.telemetry.diagnostics.errors_factory import FollowingErrorsDiagnosticsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FollowingErrorsDiagnosticsFactoryTestCase(TestCase):
    '''
        Tests for FollowingErrorsDiagnosticsFactory component.

        It defines:

            :methods:
                | test_create_following_errors - Verifies model creation.
                | test_get_version - Verifies factory version accessor string.
    '''

    def test_create_following_errors(self) -> None:
        '''
            Verifies following errors diagnostics model creation.

            :exceptions: None.
        '''
        model = FollowingErrorsDiagnosticsFactory.create(
            j1=3,
            j2=4,
            z=1,
            j4=0,
        )
        self.assertIsInstance(model, FollowingErrorsDiagnostics)
        self.assertEqual(model.j1, 3)
        self.assertEqual(model.j2, 4)
        self.assertEqual(model.z, 1)
        self.assertEqual(model.j4, 0)

    def test_get_version(self) -> None:
        '''
            Verifies factory version accessor string.

            :exceptions: None.
        '''
        self.assertEqual(FollowingErrorsDiagnosticsFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
