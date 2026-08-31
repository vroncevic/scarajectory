# -*- coding: UTF-8 -*-

'''
Module
    canvas_renderer.py
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
    Dedicated CAD vector graphics and trajectory path rendering engine for Tkinter canvas.
'''

from __future__ import annotations

import math
import tkinter as tk
from typing import Sequence

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.canvas_tool_mode import CanvasToolMode
from scarajectory.core.model.viewport_transform import ViewportTransform
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasRenderer:
    '''
        Vector CAD rendering engine drawing polar grids, workspace limits, trajectory paths and nodes.

        It defines:

            :methods:
                | draw_background - Renders polar rays, concentric distance rings, axes and reach limits.
                | draw_trajectory - Renders trajectory path lines, waypoint node markers and selection rings.
                | draw_preview - Renders interactive drag preview geometry for active CAD tool.
    '''

    @classmethod
    def draw_background(
        cls,
        canvas: tk.Canvas,
        vp: ViewportTransform,
        r_min_mm: float
    ) -> None:
        '''
            Renders polar rays, concentric distance rings, axes and reach limits.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param r_min_mm: Minimum deadzone radius in mm.
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        center: tuple[float, float] = vp.world_to_screen(0.0, 0.0, w, h)
        rmax_px: float = ViewportTransform.R_MAX_MM * vp.scale
        rmin_px: float = r_min_mm * vp.scale

        for deg in (30, 60, 120, 150, 210, 240, 300, 330):
            canvas.create_line(
                center[0], center[1],
                center[0] + rmax_px * math.cos(math.radians(deg)),
                center[1] - rmax_px * math.sin(math.radians(deg)),
                fill='#232830', dash=(2, 6)
            )

        for r_mm in (50.0, 100.0, 150.0, 200.0, 250.0):
            r_px: float = r_mm * vp.scale
            canvas.create_oval(
                center[0] - r_px, center[1] - r_px,
                center[0] + r_px, center[1] + r_px,
                outline='#282c34', dash=(2, 4)
            )

        canvas.create_line(0, center[1], w, center[1], fill='#3e4451', width=1)
        canvas.create_line(center[0], 0, center[0], h, fill='#3e4451', width=1)
        canvas.create_text(w - 15, center[1] - 10, text='+X', fill='#61afef', font=('DejaVu Sans', 8, 'bold'))
        canvas.create_text(center[0] + 15, 12, text='+Y', fill='#61afef', font=('DejaVu Sans', 8, 'bold'))

        canvas.create_oval(
            center[0] - rmax_px, center[1] - rmax_px,
            center[0] + rmax_px, center[1] + rmax_px,
            outline='#61afef', width=2
        )
        canvas.create_oval(
            center[0] - rmin_px, center[1] - rmin_px,
            center[0] + rmin_px, center[1] + rmin_px,
            outline='#e06c75', width=1, dash=(4, 4)
        )
        canvas.create_text(
            center[0] + rmax_px - 40, center[1] + rmax_px + 12,
            text='R_MAX (270mm)', fill='#61afef', font=('DejaVu Sans', 7)
        )
        canvas.create_text(
            center[0] + rmin_px + 15, center[1] + 10,
            text='DEADZONE', fill='#e06c75', font=('DejaVu Sans', 7)
        )

        canvas.create_oval(center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5, fill='#61afef', outline='#ffffff')
        canvas.create_text(center[0] + 8, center[1] - 8, text='(0,0) BASE', fill='#61afef', font=('DejaVu Sans', 8, 'bold'), anchor='w')

    @classmethod
    def _draw_nodes(
        cls,
        canvas: tk.Canvas,
        vp: ViewportTransform,
        waypoints: Sequence[Waypoint],
        validator: ITrajectoryValidator
    ) -> None:
        '''
            Renders waypoint circle markers and point labels.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param waypoints: Sequence of Waypoint entities.
            :param validator: ITrajectoryValidator instance.
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        for index, pt in enumerate(waypoints):
            sx, sy = vp.world_to_screen(pt.x, pt.y, w, h)
            is_valid: bool = validator.validate_point_dto(pt.to_dto()).is_valid
            node_color: str = '#98c379' if is_valid else '#e06c75'
            canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4, fill=node_color, outline='#ffffff')
            canvas.create_text(
                sx + 8, sy - 6,
                text=f'P{index + 1}',
                fill='#abb2bf',
                font=('DejaVu Sans', 8),
                anchor='w'
            )

    @classmethod
    def draw_trajectory(
        cls,
        canvas: tk.Canvas,
        vp: ViewportTransform,
        plan: TrajectoryPlan,
        validator: ITrajectoryValidator
    ) -> None:
        '''
            Renders trajectory path lines, waypoint node markers and selection rings.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param plan: Active TrajectoryPlan instance.
            :param validator: ITrajectoryValidator instance.
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        waypoints = plan.waypoints

        if len(waypoints) > 1:
            coords = [coord for pt in waypoints for coord in vp.world_to_screen(pt.x, pt.y, w, h)]
            canvas.create_line(*coords, fill='#98c379', width=2)

        cls._draw_nodes(canvas, vp, waypoints, validator)

        sel_idx: int = plan.selected_index
        if 0 <= sel_idx < len(waypoints):
            s_pt = waypoints[sel_idx]
            sel_x, sel_y = vp.world_to_screen(s_pt.x, s_pt.y, w, h)
            canvas.create_oval(sel_x - 9, sel_y - 9, sel_x + 9, sel_y + 9, outline='#e5c07b', width=2, dash=(2, 2))

    @classmethod
    def draw_preview(
        cls,
        canvas: tk.Canvas,
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
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        drag_start, current_pos = drag_points
        x1, y1 = vp.world_to_screen(drag_start[0], drag_start[1], w, h)
        x2, y2 = vp.world_to_screen(current_pos[0], current_pos[1], w, h)

        if tool_mode == CanvasToolMode.CIRCLE:
            radius: float = math.hypot(current_pos[0] - drag_start[0], current_pos[1] - drag_start[1]) * vp.scale
            canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius, outline='#e5c07b', width=1, dash=(3, 3))
            canvas.create_line(x1, y1, x2, y2, fill='#e5c07b', dash=(2, 2))
        elif tool_mode == CanvasToolMode.RECTANGLE:
            canvas.create_rectangle(x1, y1, x2, y2, outline='#e5c07b', width=1, dash=(3, 3))
        elif tool_mode in (CanvasToolMode.POINT, CanvasToolMode.SELECT, CanvasToolMode.LINE):
            canvas.create_line(x1, y1, x2, y2, fill='#e5c07b', dash=(2, 2))
