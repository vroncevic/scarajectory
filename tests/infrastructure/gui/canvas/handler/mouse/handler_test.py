# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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
    Unit tests for CanvasMouseHandler CAD mouse interaction component.
'''

from __future__ import annotations

from tkinter import Event, Widget
from typing import ClassVar, cast
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.mouse.bundle import MouseHandlerBundle
from scarajectory.infrastructure.gui.canvas.handler.mouse.context import CanvasEventContext
from scarajectory.infrastructure.gui.canvas.handler.mouse.handler import CanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

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
        Dummy event object mimicking Tkinter mouse event attributes.
    '''

    x: int
    y: int
    num: int
    delta: int

    def __init__(
        self,
        x: int,
        y: int,
        num: int = 1,
        delta: int = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.num = num
        self.delta = delta

    def get_coords(self) -> tuple[int, int]:
        '''Returns event coordinates.'''
        return (self.x, self.y)

    def get_delta(self) -> int:
        '''Returns event scroll delta.'''
        return self.delta


class TestCanvasMouseHandler(TestCase):
    '''
        Test cases for CanvasMouseHandler mouse interaction logic.

        It defines:

            :attributes:
                | DEFAULT_SETTINGS - Default settings instance for canvas events.
            :methods:
                | setUp - Initializes fixtures with mocked collaborators.
                | test_mouse_down_panning - Tests pan start handling.
                | test_mouse_down_select - Tests select down dispatch.
                | test_mouse_down_freehand - Tests freehand point commit dispatch.
                | test_mouse_drag_modes - Tests mouse drag for various canvas modes.
                | test_mouse_up_and_stop_pan - Tests mouse up committing shapes and releasing pan.
                | test_format_cursor_status - Tests formatting status readout string.
    '''

    DEFAULT_SETTINGS: ClassVar[CanvasSettings] = CanvasSettings(
        default_z=15.0, default_speed=35.0
    )

    def setUp(self) -> None:
        '''
            Initializes fixtures for plan, viewport, and mouse handler.

            :exceptions: None.
        '''
        self.vp = ViewportTransform()
        self.state = CanvasInteractionState()
        self.pan_handler = MagicMock()
        self.selection_handler = MagicMock()
        self.shape_handler = MagicMock()
        self.drag_handler = MagicMock()

        bundle = MouseHandlerBundle(
            vp=self.vp,
            state=self.state,
            pan_handler=self.pan_handler,
            selection_handler=self.selection_handler,
            shape_handler=self.shape_handler,
            drag_handler=self.drag_handler,
        )
        self.handler = CanvasMouseHandler(bundle)

    def test_mouse_down_panning(self) -> None:
        '''
            Tests mouse down when panning is triggered.

            :exceptions: None.
        '''
        pan_evt: Event[Widget] = cast(
            'Event[Widget]', DummyEvent(x=100, y=150, num=2)
        )
        ctx_point = CanvasEventContext(
            800, 600, CanvasToolMode.POINT, self.DEFAULT_SETTINGS
        )
        self.pan_handler.try_start_pan.return_value = True
        self.handler.handle_mouse_down(pan_evt, ctx_point)
        self.pan_handler.try_start_pan.assert_called_once_with(pan_evt)
        self.assertFalse(self.state.is_dragging)

    def test_mouse_down_select(self) -> None:
        '''
            Tests mouse down dispatch for select mode.

            :exceptions: None.
        '''
        self.pan_handler.try_start_pan.return_value = False
        select_evt: Event[Widget] = cast(
            'Event[Widget]', DummyEvent(x=400, y=300, num=1)
        )
        ctx_select = CanvasEventContext(
            800, 600, CanvasToolMode.SELECT, self.DEFAULT_SETTINGS
        )
        self.handler.handle_mouse_down(select_evt, ctx_select)
        self.assertTrue(self.state.is_dragging)
        self.selection_handler.handle_select_down.assert_called_once()

    def test_mouse_down_freehand(self) -> None:
        '''
            Tests mouse down dispatch for freehand mode.

            :exceptions: None.
        '''
        self.pan_handler.try_start_pan.return_value = False
        freehand_evt: Event[Widget] = cast(
            'Event[Widget]', DummyEvent(x=410, y=310, num=1)
        )
        ctx_freehand = CanvasEventContext(
            800, 600, CanvasToolMode.FREEHAND, self.DEFAULT_SETTINGS
        )
        self.handler.handle_mouse_down(freehand_evt, ctx_freehand)
        self.assertTrue(self.state.is_dragging)
        self.shape_handler.commit_point.assert_called_once()

    def test_mouse_drag_modes(self) -> None:
        '''
            Tests mouse drag for pan, select, freehand, and shape tools.

            :exceptions: None.
        '''
        pan_evt: Event[Widget] = cast(
            'Event[Widget]', DummyEvent(x=120, y=115, num=1)
        )
        ctx_point = CanvasEventContext(
            800, 600, CanvasToolMode.POINT, self.DEFAULT_SETTINGS
        )
        self.pan_handler.pan_drag.return_value = True
        self.assertTrue(self.handler.handle_mouse_drag(pan_evt, ctx_point))

        self.pan_handler.pan_drag.return_value = False
        ctx_select = CanvasEventContext(
            800, 600, CanvasToolMode.SELECT, self.DEFAULT_SETTINGS
        )
        self.selection_handler.handle_select_drag.return_value = True
        self.assertTrue(self.handler.handle_mouse_drag(pan_evt, ctx_select))

        ctx_freehand = CanvasEventContext(
            800, 600, CanvasToolMode.FREEHAND, self.DEFAULT_SETTINGS
        )
        self.drag_handler.handle_drag_freehand.return_value = True
        self.assertTrue(self.handler.handle_mouse_drag(pan_evt, ctx_freehand))

        ctx_circle = CanvasEventContext(
            800, 600, CanvasToolMode.CIRCLE, self.DEFAULT_SETTINGS
        )
        self.assertTrue(self.handler.handle_mouse_drag(pan_evt, ctx_circle))

        self.assertFalse(self.handler.handle_mouse_drag(pan_evt, ctx_point))

    def test_mouse_up_and_stop_pan(self) -> None:
        '''
            Tests committing point on mouse up and releasing active pan.

            :exceptions: None.
        '''
        ctx_point = CanvasEventContext(
            800, 600, CanvasToolMode.POINT, self.DEFAULT_SETTINGS
        )
        up_evt: Event[Widget] = cast(
            'Event[Widget]', DummyEvent(x=450, y=250, num=1)
        )
        self.pan_handler.stop_pan.return_value = True
        self.handler.handle_mouse_up(up_evt, ctx_point)
        self.pan_handler.stop_pan.assert_called_once()

        self.pan_handler.stop_pan.return_value = False
        self.state.is_dragging = True
        self.state.drag_start_world = (10.0, 20.0)
        self.handler.handle_mouse_up(up_evt, ctx_point)
        self.shape_handler.commit_shape.assert_called_once()
        self.assertFalse(self.state.is_dragging)

    def test_format_cursor_status(self) -> None:
        '''
            Tests status bar readout text formatting.

            :exceptions: None.
        '''
        event: Event[Widget] = cast(
            'Event[Widget]', DummyEvent(x=400, y=300)
        )
        status_text = self.handler.format_cursor_status(event, 800, 600)
        self.assertIn('Cursor: X=', status_text)
        self.assertIn('Zoom:', status_text)


if __name__ == '__main__':
    main()
