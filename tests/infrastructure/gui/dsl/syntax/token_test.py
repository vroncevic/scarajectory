# -*- coding: UTF-8 -*-

'''
Module
    token_test.py
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
    Unit tests for SyntaxToken model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SyntaxTokenTestCase(TestCase):
    '''
        Unit test suite validating SyntaxToken model.

        It defines:

            :methods:
                | test_token_fields - Tests token attribute assignment.
                | test_token_immutability - Tests frozen immutability.
    '''

    def test_token_fields(self) -> None:
        '''
            Tests attribute values of SyntaxToken.

            :exceptions: None.
        '''
        token = SyntaxToken(
            tag='dsl_command',
            start_idx='1.0',
            end_idx='1.6',
        )
        self.assertEqual(token.tag, 'dsl_command')
        self.assertEqual(token.start_idx, '1.0')
        self.assertEqual(token.end_idx, '1.6')

    def test_token_immutability(self) -> None:
        '''
            Tests that SyntaxToken is frozen.

            :exceptions: None.
        '''
        token = SyntaxToken(
            tag='dsl_comment',
            start_idx='1.0',
            end_idx='1.10',
        )
        with self.assertRaises(AttributeError):
            token.tag = 'other'


if __name__ == '__main__':
    main()
