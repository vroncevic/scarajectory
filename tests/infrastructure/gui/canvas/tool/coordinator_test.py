# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for CanvasToolModeCoordinator component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.tool.coordinator import CanvasToolModeCoordinator
from scarajectory.infrastructure.gui.canvas.tool.icoordinator import ICanvasToolModeCoordinator
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasToolModeCoordinatorTestCase(TestCase):
    '''
        Tests CanvasToolModeCoordinator component behavior and protocol conformance.

        It defines:

            :methods:
                | setUp - Sets up mock collaborators and coordinator component.
                | test_satisfies_protocol - Verifies component satisfies ICanvasToolModeCoordinator.
                | test_set_tool_mode - Verifies mode changes, drag reset and redraw trigger.
                | test_reset - Verifies reset restores default POINT mode.
    '''

    def setUp(self) -> None:
        '''
            Sets up mock collaborators and coordinator component.

            :exceptions: None.
        '''
        self.state = CanvasInteractionState()
        self.state.is_dragging = True
        self.mock_redraw_delegate = MagicMock()

        self.coordinator = CanvasToolModeCoordinator(
            state=self.state,
            redraw_delegate=self.mock_redraw_delegate,
        )

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies CanvasToolModeCoordinator satisfies ICanvasToolModeCoordinator.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, ICanvasToolModeCoordinator)

    def test_set_tool_mode(self) -> None:
        '''
            Verifies set_tool_mode updates mode, resets drag and triggers redraw.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.tool_mode, CanvasToolMode.POINT)
        self.coordinator.set_tool_mode(CanvasToolMode.LINE)
        self.assertEqual(self.coordinator.tool_mode, CanvasToolMode.LINE)
        self.assertFalse(self.state.is_dragging)
        self.mock_redraw_delegate.redraw.assert_called_once()

    def test_reset(self) -> None:
        '''
            Verifies reset restores default POINT mode and triggers redraw.

            :exceptions: None.
        '''
        self.coordinator.set_tool_mode(CanvasToolMode.FREEHAND)
        self.assertEqual(self.coordinator.tool_mode, CanvasToolMode.FREEHAND)
        self.mock_redraw_delegate.reset_mock()

        self.coordinator.reset()
        self.assertEqual(self.coordinator.tool_mode, CanvasToolMode.POINT)
        self.mock_redraw_delegate.redraw.assert_called_once()


if __name__ == '__main__':
    main()
