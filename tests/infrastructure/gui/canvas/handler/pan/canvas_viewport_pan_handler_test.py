# -*- coding: UTF-8 -*-

'''
Module
    canvas_viewport_pan_handler_test.py
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
    Unit tests for CanvasViewportPanHandler viewport panning component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.handler.pan.canvas_viewport_pan_handler import CanvasViewportPanHandler
from scarajectory.infrastructure.gui.canvas.handler.pan.canvas_viewport_pan_handler_factory import CanvasViewportPanHandlerFactory
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyEvent:
    '''
        Simulates Tkinter mouse events for unit testing.
    '''

    x: int
    y: int
    num: int
    delta: int

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        num: int = 1,
        delta: int = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.num = num
        self.delta = delta


class TestCanvasViewportPanHandler(TestCase):
    '''
        Test cases for CanvasViewportPanHandler viewport panning logic.

        It defines:

            :methods:
                | setUp - Initializes fixtures for viewport and pan handler.
                | test_try_start_pan_middle_click - Tests button 2 pan start.
                | test_try_start_pan_right_click - Tests button 3 pan start.
                | test_try_start_pan_left_click - Tests button 1 ignores pan.
                | test_pan_drag_active - Tests drag during active pan.
                | test_pan_drag_inactive - Tests drag when not panning.
                | test_stop_pan - Tests terminating active pan.
                | test_is_panning - Tests querying panning status.
    '''

    def setUp(self) -> None:
        '''
            Initializes fixtures for viewport and pan handler.

            :exceptions: None.
        '''
        self.vp = ViewportTransform()
        self.state = CanvasInteractionState()
        self.pan_handler: CanvasViewportPanHandler = (
            CanvasViewportPanHandlerFactory.create(self.vp, self.state)
        )

    def test_try_start_pan_middle_click(self) -> None:
        '''
            Tests pan start with button 2.

            :exceptions: None.
        '''
        event = DummyEvent(x=120, y=180, num=2)
        started: bool = self.pan_handler.try_start_pan(event)
        self.assertTrue(started)
        self.assertTrue(self.pan_handler.is_panning())
        self.assertEqual(self.state.pan_x, 120)
        self.assertEqual(self.state.pan_y, 180)

    def test_try_start_pan_right_click(self) -> None:
        '''
            Tests pan start with button 3.

            :exceptions: None.
        '''
        event = DummyEvent(x=200, y=250, num=3)
        started: bool = self.pan_handler.try_start_pan(event)
        self.assertTrue(started)
        self.assertTrue(self.pan_handler.is_panning())

    def test_try_start_pan_left_click(self) -> None:
        '''
            Tests left-click ignores panning.

            :exceptions: None.
        '''
        event = DummyEvent(x=200, y=250, num=1)
        started: bool = self.pan_handler.try_start_pan(event)
        self.assertFalse(started)
        self.assertFalse(self.pan_handler.is_panning())

    def test_pan_drag_active(self) -> None:
        '''
            Tests drag translation during active pan.

            :exceptions: None.
        '''
        self.state.is_panning = True
        self.state.pan_x = 100
        self.state.pan_y = 100

        panned: bool = self.pan_handler.pan_drag(130, 140)
        self.assertTrue(panned)
        self.assertEqual(self.vp.pan_x, 30.0)
        self.assertEqual(self.vp.pan_y, 40.0)
        self.assertEqual(self.state.pan_x, 130)
        self.assertEqual(self.state.pan_y, 140)

    def test_pan_drag_inactive(self) -> None:
        '''
            Tests drag ignored when not panning.

            :exceptions: None.
        '''
        self.state.is_panning = False
        panned: bool = self.pan_handler.pan_drag(130, 140)
        self.assertFalse(panned)
        self.assertEqual(self.vp.pan_x, 0.0)
        self.assertEqual(self.vp.pan_y, 0.0)

    def test_stop_pan(self) -> None:
        '''
            Tests terminating active pan.

            :exceptions: None.
        '''
        self.state.is_panning = True
        stopped: bool = self.pan_handler.stop_pan()
        self.assertTrue(stopped)
        self.assertFalse(self.pan_handler.is_panning())

        stopped_again: bool = self.pan_handler.stop_pan()
        self.assertFalse(stopped_again)

    def test_is_panning(self) -> None:
        '''
            Tests querying panning status.

            :exceptions: None.
        '''
        self.state.is_panning = False
        self.assertFalse(self.pan_handler.is_panning())
        self.state.is_panning = True
        self.assertTrue(self.pan_handler.is_panning())


if __name__ == '__main__':
    main()
