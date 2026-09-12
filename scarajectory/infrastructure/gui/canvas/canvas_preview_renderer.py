# -*- coding: UTF-8 -*-

'''
Module
    canvas_preview_renderer.py
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
    Vector CAD rendering engine for interactive mouse drag geometry previews.
'''

from __future__ import annotations

from math import hypot
from tkinter import Canvas

from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasPreviewRenderer:
    '''
        Renders interactive drag preview geometry for active CAD tools.

        It defines:

            :methods:
                | draw_preview - Renders interactive drag preview geometry for active CAD tool.
    '''

    @classmethod
    def draw_preview(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        tool_mode: CanvasToolMode,
        drag_points: tuple[tuple[float, float], tuple[float, float]]
    ) -> None:
        '''
            Renders interactive drag preview geometry for active CAD tool.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param tool_mode: Active CanvasToolMode.
            :param drag_points: Tuple of (drag_start, current_pos) coordinates in mm.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        drag_start, current_pos = drag_points
        x1, y1 = vp.world_to_screen(drag_start[0], drag_start[1], w, h)
        x2, y2 = vp.world_to_screen(current_pos[0], current_pos[1], w, h)

        if tool_mode == CanvasToolMode.CIRCLE:
            radius: float = hypot(current_pos[0] - drag_start[0], current_pos[1] - drag_start[1]) * vp.scale
            canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius, outline='#e5c07b', width=1, dash=(3, 3))
            canvas.create_line(x1, y1, x2, y2, fill='#e5c07b', dash=(2, 2))
        elif tool_mode == CanvasToolMode.RECTANGLE:
            canvas.create_rectangle(x1, y1, x2, y2, outline='#e5c07b', width=1, dash=(3, 3))
        elif tool_mode in (CanvasToolMode.POINT, CanvasToolMode.SELECT, CanvasToolMode.LINE):
            canvas.create_line(x1, y1, x2, y2, fill='#e5c07b', dash=(2, 2))
