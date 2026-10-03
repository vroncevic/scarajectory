# -*- coding: UTF-8 -*-

'''
Module
    tool_command_formatter_test.py
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
    Unit testing for ToolCommandFormatter component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.formatter.command.tool_command_formatter import (
    ToolCommandFormatter,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolCommandFormatterTestCase(TestCase):
    '''Unit tests for ToolCommandFormatter formatting routines.'''

    def test_format_pump(self) -> None:
        '''Verifies format_pump returns on and off command packets.'''
        self.assertEqual(ToolCommandFormatter.format_pump(enable=True), '<CMD:PUMP#1>')
        self.assertEqual(ToolCommandFormatter.format_pump(enable=False), '<CMD:PUMP#0>')

    def test_format_valve(self) -> None:
        '''Verifies format_valve returns open and closed command packets.'''
        self.assertEqual(ToolCommandFormatter.format_valve(enable=True), '<CMD:VALVE#1>')
        self.assertEqual(ToolCommandFormatter.format_valve(enable=False), '<CMD:VALVE#0>')

    def test_format_wait(self) -> None:
        '''Verifies format_wait clamps negative delays to zero and formats correctly.'''
        self.assertEqual(ToolCommandFormatter.format_wait(500), '<CMD:WAIT#500>')
        self.assertEqual(ToolCommandFormatter.format_wait(-20), '<CMD:WAIT#0>')

    def test_format_override(self) -> None:
        '''Verifies format_override clamps values to 1-200 range and formats correctly.'''
        self.assertEqual(ToolCommandFormatter.format_override(100), '<CMD:OVERRIDE#100>')
        self.assertEqual(ToolCommandFormatter.format_override(0), '<CMD:OVERRIDE#1>')
        self.assertEqual(ToolCommandFormatter.format_override(250), '<CMD:OVERRIDE#200>')


if __name__ == '__main__':
    main()
