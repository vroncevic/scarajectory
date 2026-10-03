# -*- coding: UTF-8 -*-

'''
Module
    toolbar_tool_selector_test.py
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
    Unit tests for ToolbarToolSelector and ToolbarToolSelectorFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.toolbar.tool_selector import ToolbarToolSelector
from scarajectory.infrastructure.gui.toolbar.tool_selector_factory import ToolbarToolSelectorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolbarToolSelector(TestCase):
    '''
        Test cases verifying CAD tool mode selection subcomponent.
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
        self.mock_canvas = MagicMock()
        self.selector: ToolbarToolSelector = (
            ToolbarToolSelectorFactory.create(self.root, self.mock_canvas)
        )

    def tearDown(self) -> None:
        self.selector.destroy()

    def test_default_mode(self) -> None:
        '''
            Tests default tool mode is POINT.
        '''
        self.assertEqual(self.selector.get_tool_mode(), 'POINT')

    def test_set_tool_mode(self) -> None:
        '''
            Tests programmatic tool mode setting.
        '''
        self.selector.set_tool_mode(CanvasToolMode.LINE)
        self.assertEqual(self.selector.get_tool_mode(), 'LINE')
        self.mock_canvas.set_tool_mode.assert_called_with(CanvasToolMode.LINE)

        self.selector.set_tool_mode(CanvasToolMode.CIRCLE)
        self.assertEqual(self.selector.get_tool_mode(), 'CIRCLE')
        self.mock_canvas.set_tool_mode.assert_called_with(
            CanvasToolMode.CIRCLE
        )

    def test_factory_version(self) -> None:
        '''
            Tests factory version retrieval.
        '''
        self.assertEqual(ToolbarToolSelectorFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
