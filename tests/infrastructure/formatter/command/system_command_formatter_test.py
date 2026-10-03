# -*- coding: UTF-8 -*-

'''
Module
    system_command_formatter_test.py
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
    Unit testing for SystemCommandFormatter component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.formatter.command.system_command_formatter import (
    SystemCommandFormatter,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SystemCommandFormatterTestCase(TestCase):
    '''Unit tests for SystemCommandFormatter formatting routines.'''

    def test_format_power_commands(self) -> None:
        '''Verifies format_enable and format_disable return correct packets.'''
        self.assertEqual(SystemCommandFormatter.format_enable(), '<CMD:ENABLE>')
        self.assertEqual(SystemCommandFormatter.format_disable(), '<CMD:DISABLE>')

    def test_format_safety_commands(self) -> None:
        '''Verifies format_estop and format_status return correct packets.'''
        self.assertEqual(SystemCommandFormatter.format_estop(), '<CMD:ESTOP>')
        self.assertEqual(SystemCommandFormatter.format_status(), '<CMD:STATUS>')

    def test_format_flow_commands(self) -> None:
        '''Verifies format_pause and format_resume return correct packets.'''
        self.assertEqual(SystemCommandFormatter.format_pause(), '<CMD:PAUSE>')
        self.assertEqual(SystemCommandFormatter.format_resume(), '<CMD:RESUME>')


if __name__ == '__main__':
    main()
