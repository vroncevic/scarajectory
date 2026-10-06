# -*- coding: UTF-8 -*-

'''
Module
    jog_command_formatter_test.py
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
    Unit testing for JogCommandFormatter component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.formatter.command.jog_command_formatter import JogCommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogCommandFormatterTestCase(TestCase):
    '''Unit tests for JogCommandFormatter formatting routines.'''

    def test_format_jog_positive(self) -> None:
        '''Verifies format_jog formats uppercase axis and positive step.'''
        cmd: str = JogCommandFormatter.format_jog('x', 10.0)
        self.assertEqual(cmd, '<CMD:JOG#X#10.0>')

    def test_format_jog_negative(self) -> None:
        '''Verifies format_jog formats uppercase axis and negative step.'''
        cmd: str = JogCommandFormatter.format_jog('z', -5.5)
        self.assertEqual(cmd, '<CMD:JOG#Z#-5.5>')

    def test_format_jog_rotational_axis(self) -> None:
        '''Verifies format_jog formats rotational axis with proper precision.'''
        cmd: str = JogCommandFormatter.format_jog('phi', 45.0)
        self.assertEqual(cmd, '<CMD:JOG#PHI#45.0>')


if __name__ == '__main__':
    main()
