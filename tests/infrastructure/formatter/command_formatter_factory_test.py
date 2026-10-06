# -*- coding: UTF-8 -*-

'''
Module
    command_formatter_factory_test.py
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
    Unit tests for CommandFormatterFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.formatter.command_formatter import CommandFormatter
from scarajectory.infrastructure.formatter.command_formatter_factory import CommandFormatterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandFormatterFactory(TestCase):
    '''
        Test cases for CommandFormatterFactory.

        It defines:

            :methods:
                | test_create - Tests instantiation of CommandFormatter via factory.
                | test_get_version - Tests factory version query.
    '''

    def test_create(self) -> None:
        '''
            Tests factory instantiation of CommandFormatter.

            :exceptions: None.
        '''
        formatter = CommandFormatterFactory.create()
        self.assertIsInstance(formatter, CommandFormatter)

    def test_get_version(self) -> None:
        '''
            Tests factory version string.

            :exceptions: None.
        '''
        version = CommandFormatterFactory.get_version()
        self.assertTrue(isinstance(version, str) and len(version) > 0)


if __name__ == '__main__':
    main()
