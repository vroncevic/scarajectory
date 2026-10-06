# -*- coding: UTF-8 -*-

'''
Module
    serial_console_builder_test.py
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
    Unit tests for SerialConsoleBuilder component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.console.serial_console_builder import SerialConsoleBuilder
from scarajectory.infrastructure.gui.console.serial_console_builder_factory import SerialConsoleBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSerialConsoleBuilder(TestCase):
    '''
        Test cases for SerialConsoleBuilder.
    '''

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies factory creates SerialConsoleBuilder.
        '''
        builder = SerialConsoleBuilderFactory.create()
        self.assertIsInstance(builder, SerialConsoleBuilder)
        self.assertIsInstance(SerialConsoleBuilderFactory.get_version(), str)

    @patch('scarajectory.infrastructure.gui.console.serial_console_builder.Text')
    @patch('scarajectory.infrastructure.gui.console.serial_console_builder.Button')
    @patch('scarajectory.infrastructure.gui.console.serial_console_builder.Frame')
    def test_build_widgets(self, mock_frame: MagicMock, mock_btn: MagicMock, mock_text: MagicMock) -> None:
        '''
            Verifies build_widgets sets up UI elements.
        '''
        mock_console = MagicMock()
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        builder = SerialConsoleBuilder()
        result = builder.build_widgets(mock_console)

        self.assertEqual(result, mock_text_inst)
        self.assertEqual(mock_btn.call_count, 3)
        self.assertTrue(mock_text_inst.pack.called)
