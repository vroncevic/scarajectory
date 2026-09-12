# -*- coding: UTF-8 -*-

'''
Module
    canvas_trajectory_renderer.py
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
    Vector CAD rendering engine for trajectory paths, waypoint markers, and selection highlights.
'''

from __future__ import annotations

from tkinter import Canvas
from typing import Sequence

from scarajectory.core.model.trajectory.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasTrajectoryRenderer:
    '''
        Renders trajectory polylines, waypoint markers, coordinate labels, and selection rings.

        It defines:

            :methods:
                | draw_trajectory - Renders trajectory path lines, waypoint node markers and selection rings.
                | _draw_nodes - Renders waypoint circle markers and point labels.
    '''

    @classmethod
    def _draw_nodes(
        cls,
        canvas: Canvas,
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
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        for index, pt in enumerate(waypoints):
            sx, sy = vp.world_to_screen(pt.x, pt.y, w, h)
            is_valid: bool = validator.validate_point(pt).is_valid
            node_color: str = '#98c379' if is_valid else '#e06c75'
            canvas.create_oval(sx - 4, sy - 4, sx + 4, sy + 4, fill=node_color, outline='#ffffff', width=1)
            canvas.create_text(
                sx + 8, sy - 8,
                text=f'P{index + 1} ({pt.x:.0f}, {pt.y:.0f})',
                fill='#abb2bf',
                font=('DejaVu Sans', 8),
                anchor='w'
            )

    @classmethod
    def draw_trajectory(
        cls,
        canvas: Canvas,
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
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        waypoints: Sequence[Waypoint] = plan.waypoints

        if len(waypoints) > 1:
            coords: list[float] = [coord for pt in waypoints for coord in vp.world_to_screen(pt.x, pt.y, w, h)]
            canvas.create_line(*coords, fill='#98c379', width=2)

        cls._draw_nodes(canvas, vp, waypoints, validator)

        sel_idx: int = plan.selected_index
        if 0 <= sel_idx < len(waypoints):
            s_pt: Waypoint = waypoints[sel_idx]
            sel_x, sel_y = vp.world_to_screen(s_pt.x, s_pt.y, w, h)
            canvas.create_oval(sel_x - 9, sel_y - 9, sel_x + 9, sel_y + 9, outline='#e5c07b', width=2, dash=(2, 2))
