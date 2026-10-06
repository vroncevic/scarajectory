# -*- coding: UTF-8 -*-

'''
Module
    connection_preference_test.py
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
    Unit tests for ConnectionPreference and ConnectionPreferenceFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.preferences.connection_preference import ConnectionPreference
from scarajectory.core.service.preferences.connection_preference_factory import ConnectionPreferenceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestConnectionPreference(TestCase):
    '''
        Test cases verifying ConnectionPreference model and factory.

        It defines:

            :methods:
                | test_create_explicit - Verifies creating preference with explicit values.
                | test_create_default - Verifies creating preference with sensible defaults.
                | test_factory_version - Verifies factory version string.
    '''

    def test_create_explicit(self) -> None:
        '''
            Verifies creating preference with explicit port and baud.
        '''
        pref: ConnectionPreference = ConnectionPreferenceFactory.create(
            port='/dev/ttyUSB0',
            baud=115200
        )
        self.assertEqual(pref.port, '/dev/ttyUSB0')
        self.assertEqual(pref.baud, 115200)

    def test_create_default(self) -> None:
        '''
            Verifies default preference values.
        '''
        pref: ConnectionPreference = ConnectionPreferenceFactory.create_default()
        self.assertEqual(pref.port, ConnectionPreferenceFactory.DEFAULT_PORT)
        self.assertEqual(pref.baud, ConnectionPreferenceFactory.DEFAULT_BAUD)

    def test_factory_version(self) -> None:
        '''
            Verifies factory version returns current semantic version.
        '''
        self.assertEqual(ConnectionPreferenceFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
