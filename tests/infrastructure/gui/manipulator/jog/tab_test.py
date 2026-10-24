# -*- coding: UTF-8 -*-

'''
Module
    tab_test.py
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
    Unit tests for JogTab.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.jog.axis import JogAxis
from scarajectory.infrastructure.gui.manipulator.jog.panel.bundle import JogPanelBundle
from scarajectory.infrastructure.gui.manipulator.jog.tab import JogTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogTab(TestCase):
    '''
        Test cases verifying JogTab layout mounting and sub-panel orchestration.
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
        self.mock_power = MagicMock()
        self.mock_grid = MagicMock()
        self.mock_tool = MagicMock()
        self.mock_raw = MagicMock()

        self.bundle = JogPanelBundle(
            power_panel=self.mock_power,
            axis_grid_panel=self.mock_grid,
            tool_panel=self.mock_tool,
            raw_panel=self.mock_raw,
        )
        self.tab = JogTab(self.root)
        self.tab.mount_panels(self.bundle)

    def tearDown(self) -> None:
        self.tab.destroy()

    def test_mounted_subpanels(self) -> None:
        '''
            Tests that all specialized subpanels are mounted and accessible.

            :exceptions: None.
        '''
        self.assertIs(self.tab.panels, self.bundle)
        self.mock_power.pack.assert_called_once()
        self.mock_grid.pack.assert_called_once()
        self.mock_tool.pack.assert_called_once()
        self.mock_raw.pack.assert_called_once()

    def test_jog_step_delegation(self) -> None:
        '''
            Tests that jog_step delegates to axis grid panel.

            :exceptions: None.
        '''
        self.tab.jog_step(JogAxis.X, 1.0)
        self.mock_grid.jog_step.assert_called_once_with(JogAxis.X, 1.0)

    def test_send_raw_delegation(self) -> None:
        '''
            Tests that send_raw delegates to raw command panel.

            :exceptions: None.
        '''
        self.tab.send_raw()
        self.mock_raw.send_raw.assert_called_once()


if __name__ == '__main__':
    main()
