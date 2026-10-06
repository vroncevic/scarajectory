# -*- coding: UTF-8 -*-

'''
Module
    protocol_mode_test.py
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
    Unit tests for ProtocolMode communication protocol mode enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolModeTestCase(TestCase):
    '''
        Tests for ProtocolMode enumeration values and membership.

        It defines:

            :methods:
                | test_enumeration_values - Verifies string representation of protocol modes.
                | test_enumeration_members - Verifies all expected members are defined.
    '''

    def test_enumeration_values(self) -> None:
        '''
            Verifies string representation of protocol modes.

            :exceptions: None.
        '''
        self.assertEqual(ProtocolMode.ASCII.value, 'ascii')
        self.assertEqual(ProtocolMode.BINARY.value, 'binary')
        self.assertEqual(str(ProtocolMode.ASCII), 'ascii')
        self.assertEqual(str(ProtocolMode.BINARY), 'binary')

    def test_enumeration_members(self) -> None:
        '''
            Verifies all expected members are defined.

            :exceptions: None.
        '''
        members = list(ProtocolMode)
        self.assertIn(ProtocolMode.ASCII, members)
        self.assertIn(ProtocolMode.BINARY, members)
        self.assertEqual(len(members), 2)


if __name__ == '__main__':
    main()
