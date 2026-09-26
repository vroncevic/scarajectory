# -*- coding: UTF-8 -*-

'''
Module
    canvas_background_renderer.py
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
    Vector CAD rendering engine for canvas background, polar grid, and kinematic limits.
'''

from __future__ import annotations

from math import asin, cos, degrees, pi, radians, sin
from tkinter import Canvas

from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasBackgroundRenderer:
    '''
        Renders polar rays, concentric distance rings, axes, reach limits, and unreachable deadzones.

        It defines:

            :methods:
                | draw_background - Renders polar grid rays, concentric circles, Cartesian axes, and workspace limits.
                | draw_polar_grid - Draws polar rays, concentric distance rings, and Cartesian axis lines.
                | draw_boundary_circles - Renders outer reach and inner deadzone boundary rings.
                | draw_j1_limit_crescent - Draws unreachable rear boundary polygon caused by joint 1 limits.
                | draw_annotations - Renders coordinate markers, center base indicator, and text labels.
    '''

    @classmethod
    def draw_background(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator,
    ) -> None:
        '''
            Renders polar rays, concentric distance rings, axes and reach limits.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        center: tuple[float, float] = vp.world_to_screen(0.0, 0.0, w, h)

        r_min_mm: float = validator.r_min
        r_max: float = validator.r_max
        l1: float = validator.bounds.l1
        l2: float = validator.bounds.l2
        j1_max: float = validator.bounds.j1_max_rad

        cls.draw_polar_grid(canvas, vp, center, r_max, w, h)
        cls.draw_boundary_circles(canvas, vp, center, r_min_mm, r_max)
        cls.draw_j1_limit_crescent(canvas, vp, w, h, r_max, l1, l2, j1_max)
        cls.draw_annotations(canvas, vp, center, r_min_mm, r_max, j1_max, w, h)

    @classmethod
    def draw_polar_grid(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        center: tuple[float, float],
        r_max: float,
        w: int,
        h: int,
    ) -> None:
        '''
            Draws polar rays, concentric distance rings, and Cartesian axis lines.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param center: Screen coordinates of workspace center.
            :param r_max: Maximum reach radius in mm.
            :param w: Canvas pixel width.
            :param h: Canvas pixel height.
            :exceptions: None.
        '''
        rmax_px: float = r_max * vp.scale
        for deg in (30, 60, 120, 150, 210, 240, 300, 330):
            canvas.create_line(
                center[0], center[1],
                center[0] + rmax_px * cos(radians(deg)),
                center[1] - rmax_px * sin(radians(deg)),
                fill='#232830', dash=(2, 6)
            )

        step_mm: float = 50.0
        current_r: float = step_mm
        while current_r < r_max:
            r_px: float = current_r * vp.scale
            canvas.create_oval(
                center[0] - r_px, center[1] - r_px,
                center[0] + r_px, center[1] + r_px,
                outline='#282c34', dash=(2, 4)
            )
            current_r += step_mm

        canvas.create_line(0, center[1], w, center[1], fill='#3e4451', width=1)
        canvas.create_line(center[0], 0, center[0], h, fill='#3e4451', width=1)
        canvas.create_text(w - 15, center[1] - 10, text='+X', fill='#61afef', font=('DejaVu Sans', 8, 'bold'))
        canvas.create_text(center[0] + 15, 12, text='+Y', fill='#61afef', font=('DejaVu Sans', 8, 'bold'))

    @classmethod
    def draw_boundary_circles(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        center: tuple[float, float],
        r_min_mm: float,
        r_max: float,
    ) -> None:
        '''
            Renders outer reach and inner deadzone boundary rings.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param center: Screen coordinates of workspace center.
            :param r_min_mm: Minimum deadzone radius in mm.
            :param r_max: Maximum reach radius in mm.
            :exceptions: None.
        '''
        rmax_px: float = r_max * vp.scale
        rmin_px: float = r_min_mm * vp.scale
        canvas.create_oval(
            center[0] - rmax_px, center[1] - rmax_px,
            center[0] + rmax_px, center[1] + rmax_px,
            outline='#61afef', width=2
        )
        canvas.create_oval(
            center[0] - rmin_px, center[1] - rmin_px,
            center[0] + rmin_px, center[1] + rmin_px,
            fill='#e06c75', stipple='gray25',
            outline='#e06c75', width=1, dash=(4, 4)
        )

    @classmethod
    def draw_j1_limit_crescent(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        w: int,
        h: int,
        r_max: float,
        l1: float,
        l2: float,
        j1_max: float,
    ) -> None:
        '''
            Draws unreachable rear boundary polygon caused by joint 1 limits.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param w: Canvas pixel width.
            :param h: Canvas pixel height.
            :param r_max: Maximum reach radius in mm.
            :param l1: First link length in mm.
            :param l2: Second link length in mm.
            :param j1_max: Maximum J1 angle in radians.
            :exceptions: None.
        '''
        poly_pts: list[float] = []
        steps_arc: int = 24
        start_ang: float = j1_max
        end_ang: float = 2.0 * pi - j1_max
        for i in range(steps_arc + 1):
            ang: float = start_ang + (end_ang - start_ang) * (i / steps_arc)
            sx, sy = vp.world_to_screen(r_max * cos(ang), r_max * sin(ang), w, h)
            poly_pts.extend((sx, sy))

        sin_target: float = min(1.0, (l1 * sin(j1_max)) / l2)
        theta2_cross: float = pi - asin(sin_target) - j1_max
        elbow_neg_x: float = l1 * cos(-j1_max)
        elbow_neg_y: float = l1 * sin(-j1_max)
        steps_curve: int = 16
        for i in range(steps_curve + 1):
            q2: float = theta2_cross * (i / steps_curve)
            arm2_ang: float = -j1_max - q2
            wx = elbow_neg_x + l2 * cos(arm2_ang)
            wy = elbow_neg_y + l2 * sin(arm2_ang)
            sx, sy = vp.world_to_screen(wx, wy, w, h)
            poly_pts.extend((sx, sy))

        elbow_pos_x: float = l1 * cos(j1_max)
        elbow_pos_y: float = l1 * sin(j1_max)
        for i in range(steps_curve, -1, -1):
            q2 = theta2_cross * (i / steps_curve)
            arm2_ang = j1_max + q2
            wx = elbow_pos_x + l2 * cos(arm2_ang)
            wy = elbow_pos_y + l2 * sin(arm2_ang)
            sx, sy = vp.world_to_screen(wx, wy, w, h)
            poly_pts.extend((sx, sy))

        canvas.create_polygon(
            *poly_pts,
            fill='#e06c75', stipple='gray25',
            outline='#e06c75', width=1, dash=(4, 4)
        )

    @classmethod
    def draw_annotations(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        center: tuple[float, float],
        r_min_mm: float,
        r_max: float,
        j1_max: float,
        w: int,
        h: int,
    ) -> None:
        '''
            Renders coordinate markers, center base indicator, and text labels.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param center: Screen coordinates of workspace center.
            :param r_min_mm: Minimum deadzone radius in mm.
            :param r_max: Maximum reach radius in mm.
            :param j1_max: Maximum J1 angle in radians.
            :param w: Canvas pixel width.
            :param h: Canvas pixel height.
            :exceptions: None.
        '''
        rmax_px: float = r_max * vp.scale
        rmin_px: float = r_min_mm * vp.scale
        canvas.create_text(
            center[0] + rmax_px - 40, center[1] + rmax_px + 12,
            text=f'R_MAX ({r_max:.0f}mm)', fill='#61afef', font=('DejaVu Sans', 7)
        )
        canvas.create_text(
            center[0] + rmin_px + 15, center[1] + 10,
            text='DEADZONE', fill='#e06c75', font=('DejaVu Sans', 7)
        )
        lbl_x, lbl_y = vp.world_to_screen(-r_max + 18.0, 0.0, w, h)
        j1_deg: float = degrees(j1_max)
        canvas.create_text(
            lbl_x, lbl_y,
            text=f'J1 LIMIT\n(±{j1_deg:.0f}°)', fill='#e06c75', font=('DejaVu Sans', 7), justify='center'
        )
        canvas.create_oval(center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5, fill='#61afef', outline='#ffffff')
        canvas.create_text(center[0] + 8, center[1] - 8, text='(0,0) BASE', fill='#61afef', font=('DejaVu Sans', 8, 'bold'), anchor='w')
