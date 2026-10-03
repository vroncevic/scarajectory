# -*- coding: UTF-8 -*-

'''
Module
    jog_tool_panel_test.py
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
    Unit tests for JogToolPanel and JogToolPanelFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.jog.tool_panel import JogToolPanel
from scarajectory.infrastructure.gui.manipulator.jog.tool_panel_factory import JogToolPanelFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogToolPanel(TestCase):
    '''
        Test cases verifying JogToolPanel pump and valve control dispatching.
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
        self.mock_tool = MagicMock()
        self.panel: JogToolPanel = JogToolPanelFactory.create(
            self.root,
            tool_controller=self.mock_tool,
        )

    def tearDown(self) -> None:
        self.panel.destroy()

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(JogToolPanelFactory.get_version(), '1.0.4')

    def test_set_pump(self) -> None:
        '''
            Tests vacuum pump activation and deactivation commands.
        '''
        self.panel.set_pump(True)
        self.mock_tool.set_vacuum_pump.assert_called_with(True)

        self.panel.set_pump(False)
        self.mock_tool.set_vacuum_pump.assert_called_with(False)

    def test_set_valve(self) -> None:
        '''
            Tests pneumatic valve open and close commands.
        '''
        self.panel.set_valve(True)
        self.mock_tool.set_valve.assert_called_with(True)

        self.panel.set_valve(False)
        self.mock_tool.set_valve.assert_called_with(False)


if __name__ == '__main__':
    main()
