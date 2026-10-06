# -*- coding: UTF-8 -*-

'''
Module
    icanvas_mouse_handler.py
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
    Defines structural protocol ICanvasMouseHandler for interactive CAD mouse events.
'''

from __future__ import annotations

from tkinter import Event
from typing import Any, Protocol, runtime_checkable

from scarajectory.infrastructure.gui.canvas.handler.canvas_event_context import CanvasEventContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvasMouseHandler(Protocol):
    '''
        Structural protocol defining mouse interaction callbacks for CAD canvas.

        It defines:

            :methods:
                | handle_mouse_down - Processes mouse press for tool interaction or panning.
                | handle_mouse_drag - Processes mouse motion for active tool or pan operation.
                | handle_mouse_up - Processes mouse release to commit point or shape.
                | format_cursor_status - Generates status bar readout text for current cursor position.
    '''

    def handle_mouse_down(
        self,
        event: Event[Any],
        context: CanvasEventContext,
    ) -> None:
        '''
            Processes mouse button press for tool interaction or panning.

            :param event: Tkinter mouse Event.
            :param context: CanvasEventContext instance.
        '''

    def handle_mouse_drag(
        self,
        event: Event[Any],
        context: CanvasEventContext,
    ) -> bool:
        '''
            Processes mouse motion for active tool or pan operation.

            :param event: Tkinter mouse Event.
            :param context: CanvasEventContext instance.
            :return: True if redrawing is required, False otherwise.
        '''

    def handle_mouse_up(
        self,
        event: Event[Any],
        context: CanvasEventContext,
    ) -> None:
        '''
            Processes mouse button release to commit point or shape.

            :param event: Tkinter mouse Event.
            :param context: CanvasEventContext instance.
        '''

    def format_cursor_status(
        self,
        event: Event[Any],
        width: int,
        height: int,
    ) -> str:
        '''
            Generates status bar readout text for current cursor position.

            :param event: Tkinter mouse Event.
            :param width: Current canvas pixel width.
            :param height: Current canvas pixel height.
            :return: Formatted status string.
        '''
