# -*- coding: UTF-8 -*-

'''
Module
    tool_test.py
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
    Unit tests for ToolSection component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.toolbar.section.tool import ToolSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolSectionTestCase(TestCase):
    '''
        Test cases verifying CAD tool mode selection subcomponent.

        It defines:

            :methods:
                | setUpClass - Sets up root Tk fixture.
                | tearDownClass - Tears down root Tk fixture.
                | setUp - Sets up mock canvas and tool section component.
                | tearDown - Tears down tool section widget.
                | test_default_mode - Tests default tool mode is POINT.
                | test_set_tool_mode - Tests programmatic tool mode setting.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up root Tk fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down root Tk fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up mock canvas and tool section component.

            :exceptions: None.
        '''
        self.mock_canvas = MagicMock(spec=ICanvas)
        self.section = ToolSection(self.root, self.mock_canvas)

    def tearDown(self) -> None:
        '''
            Tears down tool section widget.

            :exceptions: None.
        '''
        self.section.destroy()

    def test_default_mode(self) -> None:
        '''
            Tests default tool mode is POINT.

            :exceptions: None.
        '''
        self.assertEqual(self.section.get_tool_mode(), 'POINT')

    def test_set_tool_mode(self) -> None:
        '''
            Tests programmatic tool mode setting.

            :exceptions: None.
        '''
        self.section.set_tool_mode(CanvasToolMode.LINE)
        self.assertEqual(self.section.get_tool_mode(), 'LINE')
        self.mock_canvas.set_tool_mode.assert_called_with(CanvasToolMode.LINE)

        self.section.set_tool_mode(CanvasToolMode.CIRCLE)
        self.assertEqual(self.section.get_tool_mode(), 'CIRCLE')
        self.mock_canvas.set_tool_mode.assert_called_with(CanvasToolMode.CIRCLE)


if __name__ == '__main__':
    main()
