# -*- coding: UTF-8 -*-

'''
Module
    jog_direction_test.py
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
    Unit tests for JogDirection enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.jog.jog_direction import JogDirection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogDirectionTestCase(TestCase):
    '''
        Tests for JogDirection enumeration values and behavior.

        It defines:

            :methods:
                | test_direction_values - Verifies string representation of displacement symbols.
                | test_membership - Verifies enumeration members.
    '''

    def test_direction_values(self) -> None:
        '''
            Verifies string value symbols for positive and negative directions.

            :exceptions: None.
        '''
        self.assertEqual(JogDirection.POSITIVE.value, '+')
        self.assertEqual(JogDirection.NEGATIVE.value, '-')

    def test_membership(self) -> None:
        '''
            Verifies enumeration membership and count.

            :exceptions: None.
        '''
        self.assertEqual(str(JogDirection.POSITIVE), '+')
        self.assertEqual(str(JogDirection.NEGATIVE), '-')
        self.assertEqual(len(JogDirection), 2)


if __name__ == '__main__':
    main()
