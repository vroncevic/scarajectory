# -*- coding: UTF-8 -*-

'''
Module
    canvas_event_binder.py
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
    Dedicated Tk event binder for canvas mouse interactions, zooming, and panning.
'''

from __future__ import annotations

from tkinter import Event
from typing import Any, Final

from scarajectory.infrastructure.gui.canvas.canvas_mouse_handler import CanvasMouseHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasEventBinder:
    '''
        Binds and coordinates low-level Tk canvas mouse events with high-level CAD operations.

        It defines:

            :attributes:
                | _canvas - Target Tkinter canvas widget.
                | _mouse_handler - Interactive CAD mouse action translator.
            :methods:
                | __init__ - Initializes the binder with canvas and mouse handler.
                | bind_events - Registers all Tkinter event listeners on the canvas.
                | on_mouse_down - Dispatches mouse click press event.
                | on_mouse_drag - Dispatches mouse drag motion event.
                | on_mouse_up - Dispatches mouse button release event.
                | on_mouse_wheel_or_move - Handles zooming and coordinate readout.
    '''

    _canvas: Final[Any]
    _mouse_handler: Final[CanvasMouseHandler]

    def __init__(self, canvas: Any, mouse_handler: CanvasMouseHandler) -> None:
        '''
            Initializes the binder with canvas and mouse handler.

            :param canvas: Target canvas instance.
            :param mouse_handler: CanvasMouseHandler instance.
            :exceptions: None.
        '''
        self._canvas = canvas
        self._mouse_handler = mouse_handler

    def bind_events(self) -> None:
        '''
            Registers all Tkinter event listeners on the canvas.

            :exceptions: None.
        '''
        self._canvas.bind('<Configure>', lambda e: self._canvas.redraw())
        self._canvas.bind('<ButtonPress-1>', self.on_mouse_down)
        self._canvas.bind('<ButtonPress-2>', self.on_mouse_down)
        self._canvas.bind('<ButtonPress-3>', self.on_mouse_down)
        self._canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self._canvas.bind('<B2-Motion>', self.on_mouse_drag)
        self._canvas.bind('<B3-Motion>', self.on_mouse_drag)
        self._canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        self._canvas.bind('<ButtonRelease-2>', self.on_mouse_up)
        self._canvas.bind('<ButtonRelease-3>', self.on_mouse_up)
        self._canvas.bind('<MouseWheel>', self.on_mouse_wheel_or_move)
        self._canvas.bind('<Motion>', self.on_mouse_wheel_or_move)

    def on_mouse_down(self, event: Event) -> None:
        '''
            Dispatches mouse click press event.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        self._mouse_handler.handle_mouse_down(
            event,
            self._canvas.winfo_width(),
            self._canvas.winfo_height(),
            self._canvas._tool_mode,
            self._canvas._settings,
        )

    def on_mouse_drag(self, event: Event) -> None:
        '''
            Dispatches mouse drag motion event.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        if self._mouse_handler.handle_mouse_drag(
            event,
            self._canvas.winfo_width(),
            self._canvas.winfo_height(),
            self._canvas._tool_mode,
            self._canvas._settings,
        ):
            self._canvas.redraw()

    def on_mouse_up(self, event: Event) -> None:
        '''
            Dispatches mouse button release event.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        self._mouse_handler.handle_mouse_up(
            event,
            self._canvas.winfo_width(),
            self._canvas.winfo_height(),
            self._canvas._tool_mode,
            self._canvas._settings,
        )
        self._canvas.redraw()

    def on_mouse_wheel_or_move(self, event: Event) -> None:
        '''
            Handles zooming and coordinate readout.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        if hasattr(event, 'delta') and event.delta != 0:
            if event.delta > 0:
                self._canvas.zoom_in()
            else:
                self._canvas.zoom_out()
            return

        if self._canvas._hover_label:
            w: int = self._canvas.winfo_width()
            h: int = self._canvas.winfo_height()
            self._canvas._hover_label['text'] = (
                self._mouse_handler.format_cursor_status(event, w, h)
            )
