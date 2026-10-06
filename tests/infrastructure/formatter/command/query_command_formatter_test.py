# -*- coding: UTF-8 -*-

'''
Module
    query_command_formatter_test.py
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
    Unit testing for QueryCommandFormatter component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.formatter.command.query_command_formatter import QueryCommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueryCommandFormatterTestCase(TestCase):
    '''Unit tests for QueryCommandFormatter formatting routines.'''

    def test_format_getpos(self) -> None:
        '''Verifies format_getpos outputs expected position query packet.'''
        self.assertEqual(QueryCommandFormatter.format_getpos(), '<CMD:GETPOS>')

    def test_format_get_elbow(self) -> None:
        '''Verifies format_get_elbow outputs expected elbow query packet.'''
        self.assertEqual(QueryCommandFormatter.format_get_elbow(), '<CMD:GET_ELBOW>')

    def test_format_set_elbow_left(self) -> None:
        '''Verifies format_set_elbow formats LEFT when elbow_left is True.'''
        cmd: str = QueryCommandFormatter.format_set_elbow(elbow_left=True)
        self.assertEqual(cmd, '<CMD:SET_ELBOW#LEFT>')

    def test_format_set_elbow_right(self) -> None:
        '''Verifies format_set_elbow formats RIGHT when elbow_left is False.'''
        cmd: str = QueryCommandFormatter.format_set_elbow(elbow_left=False)
        self.assertEqual(cmd, '<CMD:SET_ELBOW#RIGHT>')


if __name__ == '__main__':
    main()
