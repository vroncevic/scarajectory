# -*- coding: UTF-8 -*-

'''
Module
    canvas_event_binder_test.py
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
    Unit testing for CanvasEventBinder and CanvasEventBinderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.canvas_event_binder import (
    CanvasEventBinder,
)
from scarajectory.infrastructure.gui.canvas.canvas_event_binder_factory import (
    CanvasEventBinderFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasEventBinderTestCase(TestCase):
    '''
        Unit tests for CanvasEventBinder and its factory.

        It defines:

            :methods:
                | setUp - Initializes mock canvas and collaborators.
                | test_bind_events - Verifies binding of canvas mouse events.
                | test_mouse_press_drag_and_release - Verifies press, drag, release handling.
                | test_mouse_wheel_and_move - Verifies wheel zoom and cursor move handling.
    '''

    def setUp(self) -> None:
        '''Initializes mock canvas and binder collaborators before each test.'''
        self.mock_canvas = MagicMock()
        self.mock_canvas.winfo_width.return_value = 800
        self.mock_canvas.winfo_height.return_value = 600
        self.mock_canvas.tool_mode = 'SELECT'
        self.mock_canvas.settings = MagicMock()

        self.mock_handler = MagicMock()
        self.mock_navigator = MagicMock()
        self.mock_presenter = MagicMock()

        self.binder: CanvasEventBinder = CanvasEventBinderFactory.create(
            self.mock_canvas,
            mouse_handler=self.mock_handler,
            navigator=self.mock_navigator,
            status_presenter=self.mock_presenter,
        )

    def test_bind_events(self) -> None:
        '''Verifies all required Tkinter event sequences are registered on canvas.'''
        self.binder.bind_events()
        bound_events = [
            call.args[0] for call in self.mock_canvas.bind.call_args_list
        ]
        expected_events = [
            '<Configure>',
            '<ButtonPress-1>',
            '<ButtonPress-2>',
            '<ButtonPress-3>',
            '<B1-Motion>',
            '<B2-Motion>',
            '<B3-Motion>',
            '<ButtonRelease-1>',
            '<ButtonRelease-2>',
            '<ButtonRelease-3>',
            '<MouseWheel>',
            '<Motion>',
        ]
        for event_name in expected_events:
            self.assertIn(event_name, bound_events)

    def test_mouse_press_drag_and_release(self) -> None:
        '''Verifies down, drag, and up events dispatch to handler and trigger redraw.'''
        mock_event = MagicMock()

        self.binder.on_mouse_down(mock_event)
        self.mock_handler.handle_mouse_down.assert_called_once()

        self.mock_handler.handle_mouse_drag.return_value = False
        self.binder.on_mouse_drag(mock_event)
        self.mock_canvas.redraw.assert_not_called()

        self.mock_handler.handle_mouse_drag.return_value = True
        self.binder.on_mouse_drag(mock_event)
        self.mock_canvas.redraw.assert_called_once()

        self.mock_canvas.redraw.reset_mock()
        self.binder.on_mouse_up(mock_event)
        self.mock_handler.handle_mouse_up.assert_called_once()
        self.mock_canvas.redraw.assert_called_once()

    def test_mouse_wheel_and_move(self) -> None:
        '''Verifies zoom-in, zoom-out, and coordinate status updating.'''
        zoom_in_event = MagicMock()
        zoom_in_event.delta = 120
        self.binder.on_mouse_wheel_or_move(zoom_in_event)
        self.mock_navigator.zoom_in.assert_called_once()

        zoom_out_event = MagicMock()
        zoom_out_event.delta = -120
        self.binder.on_mouse_wheel_or_move(zoom_out_event)
        self.mock_navigator.zoom_out.assert_called_once()

        move_event = MagicMock()
        move_event.delta = 0
        self.mock_handler.format_cursor_status.return_value = 'X: 10.0, Y: 20.0'
        self.binder.on_mouse_wheel_or_move(move_event)
        self.mock_presenter.update_cursor_status.assert_called_once_with(
            'X: 10.0, Y: 20.0'
        )

        self.assertEqual(CanvasEventBinderFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
