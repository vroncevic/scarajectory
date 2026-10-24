# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
    Translates mouse interaction and drag events into CAD vector canvas operations.
'''

from __future__ import annotations

from math import hypot
from tkinter import Event, Widget
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.canvas.handler.drag.ihandler import ICanvasDragHandler
from scarajectory.infrastructure.gui.canvas.handler.mouse.bundle import MouseHandlerBundle
from scarajectory.infrastructure.gui.canvas.handler.mouse.context import CanvasEventContext
from scarajectory.infrastructure.gui.canvas.handler.pan.ihandler import ICanvasViewportPanHandler
from scarajectory.infrastructure.gui.canvas.handler.selection.handler import CanvasSelectionMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.selection.ihandler import ICanvasSelectionMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.shape.ihandler import ICanvasShapeHandler
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasMouseHandler:
    '''
        Handles mouse press, drag, and release for CAD vector drawing.

        It defines:

            :attributes:
                | SELECT_HIT_RADIUS_PX - Hit detection pixel radius.
                | _vp - Viewport transformation matrix.
                | _state - Interactive mouse pan, drag, and selection state.
                | _pan_handler - Viewport pan translation collaborator.
                | _selection_handler - Waypoint selection collaborator.
                | _shape_handler - Shape discretization collaborator.
                | _drag_handler - Dragging motion collaborator.
            :methods:
                | __init__ - Initializes handler with injected collaborator bundle.
                | handle_mouse_down - Processes mouse down for tool or pan.
                | handle_mouse_drag - Processes motion for active tool or pan.
                | handle_mouse_up - Processes mouse release and commits shapes.
                | format_cursor_status - Computes coordinates for status.
    '''

    SELECT_HIT_RADIUS_PX: ClassVar[float] = (
        CanvasSelectionMouseHandler.SELECT_HIT_RADIUS_PX
    )

    _vp: ViewportTransform
    _state: CanvasInteractionState
    _pan_handler: ICanvasViewportPanHandler
    _selection_handler: ICanvasSelectionMouseHandler
    _shape_handler: ICanvasShapeHandler
    _drag_handler: ICanvasDragHandler

    def __init__(self, bundle: MouseHandlerBundle) -> None:
        '''
            Initializes handler with injected collaborator bundle.

            :param bundle: Required MouseHandlerBundle container.
            :exceptions: None.
        '''
        self._vp: Final[ViewportTransform] = bundle.vp
        self._state: Final[CanvasInteractionState] = bundle.state
        self._pan_handler: Final[ICanvasViewportPanHandler] = (
            bundle.pan_handler
        )
        self._selection_handler: Final[ICanvasSelectionMouseHandler] = (
            bundle.selection_handler
        )
        self._shape_handler: Final[ICanvasShapeHandler] = bundle.shape_handler
        self._drag_handler: Final[ICanvasDragHandler] = bundle.drag_handler

    def handle_mouse_down(
        self,
        event: Event[Widget],
        context: CanvasEventContext,
    ) -> None:
        '''
            Processes mouse button press for tool interaction or panning.

            :param event: Tkinter mouse Event.
            :param context: Active CanvasEventContext geometry and settings.
            :exceptions: None.
        '''
        if self._pan_handler.try_start_pan(event):
            return

        wx, wy = self._vp.screen_to_world(
            event.x, event.y, context.width, context.height
        )
        self._state.is_dragging = True
        self._state.drag_start_world = (wx, wy)
        self._state.drag_current_world = (wx, wy)
        self._state.dragged_node_idx = -1

        if context.tool_mode == CanvasToolMode.SELECT:
            self._selection_handler.handle_select_down(wx, wy)
        elif context.tool_mode == CanvasToolMode.FREEHAND:
            self._shape_handler.commit_point(wx, wy, context.settings)

    def handle_mouse_drag(
        self,
        event: Event[Widget],
        context: CanvasEventContext,
    ) -> bool:
        '''
            Processes mouse motion for active tool or viewport panning.

            :param event: Tkinter mouse Event.
            :param context: Active CanvasEventContext geometry and settings.
            :return: True if canvas redraw is needed, False otherwise.
            :exceptions: None.
        '''
        if self._pan_handler.pan_drag(event.x, event.y):
            return True

        wx, wy = self._vp.screen_to_world(
            event.x, event.y, context.width, context.height
        )
        self._state.drag_current_world = (wx, wy)

        if context.tool_mode == CanvasToolMode.SELECT:
            return self._selection_handler.handle_select_drag(wx, wy)

        if context.tool_mode == CanvasToolMode.FREEHAND:
            return self._drag_handler.handle_drag_freehand(
                wx, wy, context.settings
            )

        if context.tool_mode in (
            CanvasToolMode.CIRCLE,
            CanvasToolMode.RECTANGLE,
            CanvasToolMode.LINE,
        ):
            return True

        return False

    def handle_mouse_up(
        self,
        event: Event[Widget],
        context: CanvasEventContext,
    ) -> None:
        '''
            Processes mouse button release and commits shape insertions.

            :param event: Tkinter mouse Event.
            :param context: Active CanvasEventContext geometry and settings.
            :exceptions: None.
        '''
        if self._pan_handler.stop_pan():
            return

        wx, wy = self._vp.screen_to_world(
            event.x, event.y, context.width, context.height
        )

        if self._state.is_dragging:
            self._shape_handler.commit_shape(
                context.tool_mode,
                self._state.drag_start_world,
                (wx, wy),
                context.settings,
            )

        self._state.reset_drag()

    def format_cursor_status(
        self,
        event: Event[Widget],
        width: int,
        height: int,
    ) -> str:
        '''
            Computes world coordinates and zoom percentage for cursor status.

            :param event: Tkinter mouse Event.
            :param width: Current canvas pixel width.
            :param height: Current canvas pixel height.
            :return: Formatted status readout string.
            :exceptions: None.
        '''
        wx, wy = self._vp.screen_to_world(event.x, event.y, width, height)
        r: float = hypot(wx, wy)
        zoom_pct: int = int(
            (self._vp.scale / ViewportTransform.DEFAULT_ZOOM) * 100
        )

        return (
            f'Cursor: X={wx:6.1f} mm | Y={wy:6.1f} mm | '
            f'R={r:5.1f} mm | Zoom: {zoom_pct}%'
        )
