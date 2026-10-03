# -*- coding: UTF-8 -*-

'''
Module
    jog_tab_test.py
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
    Unit tests for JogTab and JogTabFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.jog.jog_axis import JogAxis
from scarajectory.infrastructure.gui.manipulator.jog.controllers_bundle import JogControllersBundle
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab import JogTab
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab_factory import JogTabFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogTab(TestCase):
    '''
        Test cases verifying JogTab layout mounting and sub-panel
        orchestration.
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
        self.mock_motion = MagicMock()
        self.mock_jog = MagicMock()
        self.mock_tool = MagicMock()
        self.mock_query = MagicMock()

        bundle: JogControllersBundle = JogControllersBundle(
            raw_channel=self.mock_channel,
            motion_controller=self.mock_motion,
            jog_controller=self.mock_jog,
            tool_controller=self.mock_tool,
            query_controller=self.mock_query,
        )
        self.tab: JogTab = JogTabFactory.create(
            self.root,
            bundle=bundle,
        )

    def tearDown(self) -> None:
        self.tab.destroy()

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(JogTabFactory.get_version(), '1.0.4')

    def test_layout_mounted_subpanels(self) -> None:
        '''
            Tests that all 4 specialized subpanels are instantiated and
            mounted.
        '''
        self.assertIsNotNone(self.tab.power_panel)
        self.assertIsNotNone(self.tab.axis_grid_panel)
        self.assertIsNotNone(self.tab.tool_panel)
        self.assertIsNotNone(self.tab.raw_panel)

    def test_jog_step_delegation(self) -> None:
        '''
            Tests that jog_step on JogTab delegates to axis grid panel.
        '''
        self.tab.jog_step(JogAxis.X, 1.0)
        self.mock_jog.jog.assert_called_once_with('X', 10.0)
        self.mock_query.query_status.assert_called_once()

    def test_send_raw_delegation(self) -> None:
        '''
            Tests that send_raw on JogTab delegates to raw command panel.
        '''
        self.tab.raw_panel.set_command('M115')
        self.tab.send_raw()
        self.mock_channel.send_raw_command.assert_called_once_with('M115')


if __name__ == '__main__':
    main()
