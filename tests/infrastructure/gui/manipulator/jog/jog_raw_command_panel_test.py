# -*- coding: UTF-8 -*-

'''
Module
    jog_raw_command_panel_test.py
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
    Unit tests for JogRawCommandPanel and JogRawCommandPanelFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.jog.raw_command_panel import JogRawCommandPanel
from scarajectory.infrastructure.gui.manipulator.jog.raw_command_panel_factory import JogRawCommandPanelFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogRawCommandPanel(TestCase):
    '''
        Test cases verifying JogRawCommandPanel command input, transmission, and clearing.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def setUp(self) -> None:
        self.mock_channel = MagicMock()
        self.panel: JogRawCommandPanel = JogRawCommandPanelFactory.create(
            self.root,
            raw_channel=self.mock_channel,
        )

    def tearDown(self) -> None:
        self.panel.destroy()

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(JogRawCommandPanelFactory.get_version(), '1.0.3')

    def test_send_raw_with_text(self) -> None:
        '''
            Tests that send_raw transmits command and clears input buffer.
        '''
        self.panel.set_command('M114')
        self.assertEqual(self.panel.get_command(), 'M114')

        self.panel.send_raw()

        self.mock_channel.send_raw_command.assert_called_once_with('M114')
        self.assertEqual(self.panel.get_command(), '')

    def test_send_raw_empty_does_nothing(self) -> None:
        '''
            Tests that send_raw does not transmit when input is empty or whitespace.
        '''
        self.panel.set_command('   ')
        self.panel.send_raw()

        self.mock_channel.send_raw_command.assert_not_called()

    def test_clear_command(self) -> None:
        '''
            Tests clear_command empties entry widget.
        '''
        self.panel.set_command('TEST_CMD')
        self.panel.clear_command()
        self.assertEqual(self.panel.get_command(), '')


if __name__ == '__main__':
    main()
