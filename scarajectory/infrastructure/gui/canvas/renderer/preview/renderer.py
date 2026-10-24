# -*- coding: UTF-8 -*-

'''
Module
    renderer.py
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
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

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
                | get_version - Returns component version string.
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
            :param drag_points: (drag_start, current_pos) coordinates in mm.
            :exceptions: None.
        '''
        drag_start, current_pos = drag_points
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        sx0, sy0 = vp.world_to_screen(drag_start[0], drag_start[1], w, h)
        sx, sy = vp.world_to_screen(current_pos[0], current_pos[1], w, h)

        match tool_mode:
            case CanvasToolMode.LINE:
                canvas.create_line(
                    sx0, sy0, sx, sy,
                    fill='#00d2ff', width=1, dash=(4, 4), tags='preview'
                )
            case CanvasToolMode.RECTANGLE:
                canvas.create_rectangle(
                    sx0, sy0, sx, sy,
                    outline='#00d2ff', width=1, dash=(4, 4), tags='preview'
                )
            case CanvasToolMode.CIRCLE:
                radius: float = hypot(
                    current_pos[0] - drag_start[0],
                    current_pos[1] - drag_start[1]
                ) * vp.scale
                canvas.create_oval(
                    sx0 - radius, sy0 - radius, sx0 + radius, sy0 + radius,
                    outline='#00d2ff', width=1, dash=(4, 4), tags='preview'
                )
                canvas.create_line(
                    sx0, sy0, sx, sy,
                    fill='#3a6ea5', width=1, dash=(2, 2), tags='preview'
                )
            case _:
                pass

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
