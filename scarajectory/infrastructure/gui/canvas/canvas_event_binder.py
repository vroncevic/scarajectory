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
    Dedicated Tk event binder for canvas mouse interactions, zoom, and pan.
'''

from __future__ import annotations

from tkinter import Event, Widget
from typing import Any, Final

from scarajectory.infrastructure.gui.canvas.handler.canvas_event_context import CanvasEventContext
from scarajectory.infrastructure.gui.canvas.handler.icanvas_mouse_handler import ICanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.status.icanvas_status_presenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator

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
        Binds low-level Tk canvas mouse events with high-level CAD operations.

        It defines:

            :attributes:
                | _canvas - Target Tkinter canvas widget.
                | _mouse_handler - Interactive CAD mouse action translator interface.
                | _navigator - Viewport zoom, pan, and framing coordinator interface.
                | _status_presenter - Cursor status presenter interface.
            :methods:
                | __init__ - Initializes binder with canvas and collaborators.
                | bind_events - Registers Tkinter event listeners on canvas.
                | on_mouse_down - Dispatches mouse click press event.
                | on_mouse_drag - Dispatches mouse drag motion event.
                | on_mouse_up - Dispatches mouse button release event.
                | on_mouse_wheel_or_move - Handles zoom and coordinate readout.
    '''

    _canvas: Widget
    _mouse_handler: ICanvasMouseHandler
    _navigator: ICanvasViewNavigator
    _status_presenter: ICanvasStatusPresenter

    def __init__(
        self,
        canvas: Widget,
        *,
        mouse_handler: ICanvasMouseHandler,
        navigator: ICanvasViewNavigator,
        status_presenter: ICanvasStatusPresenter,
    ) -> None:
        '''
            Initializes the binder with canvas and collaborators.

            :param canvas: Target canvas widget instance.
            :param mouse_handler: ICanvasMouseHandler interface.
            :param navigator: ICanvasViewNavigator interface.
            :param status_presenter: ICanvasStatusPresenter interface.
            :exceptions: None.
        '''
        self._canvas: Final[Widget] = canvas
        self._mouse_handler: Final[ICanvasMouseHandler] = mouse_handler
        self._navigator: Final[ICanvasViewNavigator] = navigator
        self._status_presenter: Final[ICanvasStatusPresenter] = (
            status_presenter
        )

    def bind_events(self) -> None:
        '''
            Registers all Tkinter event listeners on the canvas.

            :exceptions: None.
        '''
        self._canvas.bind('<Configure>', lambda _e: self._canvas.redraw())
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

    def on_mouse_down(self, event: Event[Any]) -> None:
        '''
            Dispatches mouse click press event.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        context = CanvasEventContext(
            width=self._canvas.winfo_width(),
            height=self._canvas.winfo_height(),
            tool_mode=self._canvas.tool_mode,
            settings=self._canvas.settings,
        )
        self._mouse_handler.handle_mouse_down(event, context)

    def on_mouse_drag(self, event: Event[Any]) -> None:
        '''
            Dispatches mouse drag motion event.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        context = CanvasEventContext(
            width=self._canvas.winfo_width(),
            height=self._canvas.winfo_height(),
            tool_mode=self._canvas.tool_mode,
            settings=self._canvas.settings,
        )
        if self._mouse_handler.handle_mouse_drag(event, context):
            self._canvas.redraw()

    def on_mouse_up(self, event: Event[Any]) -> None:
        '''
            Dispatches mouse button release event.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        context = CanvasEventContext(
            width=self._canvas.winfo_width(),
            height=self._canvas.winfo_height(),
            tool_mode=self._canvas.tool_mode,
            settings=self._canvas.settings,
        )
        self._mouse_handler.handle_mouse_up(event, context)
        self._canvas.redraw()

    def on_mouse_wheel_or_move(self, event: Event[Any]) -> None:
        '''
            Handles zooming and coordinate readout.

            :param event: Tkinter Event.
            :exceptions: None.
        '''
        if hasattr(event, 'delta') and event.delta != 0:
            if event.delta > 0:
                self._navigator.zoom_in()
            else:
                self._navigator.zoom_out()
            return

        w: int = self._canvas.winfo_width()
        h: int = self._canvas.winfo_height()
        status_text: str = self._mouse_handler.format_cursor_status(
            event, w, h
        )
        self._status_presenter.update_cursor_status(status_text)
