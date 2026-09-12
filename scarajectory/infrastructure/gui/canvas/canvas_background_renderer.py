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


class CanvasBackgroundRenderer:
    '''
        Renders polar rays, concentric distance rings, axes, reach limits, and unreachable deadzones.

        It defines:

            :methods:
                | draw_background - Renders polar grid rays, concentric circles, Cartesian axes, and workspace limits.
    '''

    @classmethod
    def draw_background(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        r_min_or_validator: float | ITrajectoryValidator
    ) -> None:
        '''
            Renders polar rays, concentric distance rings, axes and reach limits.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param r_min_or_validator: Minimum deadzone radius float or ITrajectoryValidator instance.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        center: tuple[float, float] = vp.world_to_screen(0.0, 0.0, w, h)

        if hasattr(r_min_or_validator, 'r_min') and hasattr(r_min_or_validator, 'bounds'):
            r_min_mm: float = r_min_or_validator.r_min
            r_max: float = r_min_or_validator.r_max
            l1: float = r_min_or_validator.bounds.l1
            l2: float = r_min_or_validator.bounds.l2
            j1_max: float = r_min_or_validator.bounds.j1_max_rad
        else:
            r_min_mm = float(r_min_or_validator)
            r_max = ViewportTransform.R_MAX_MM
            l1 = 150.0
            l2 = 120.0
            j1_max = radians(150.0)

        rmax_px: float = r_max * vp.scale
        rmin_px: float = r_min_mm * vp.scale

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

        # Rear unreachable boundary crescent (Shoulder J1 angle limit +/- j1_max)
        poly_pts: list[float] = []

        # 1. Outer circle arc from j1_max to (2*pi - j1_max)
        steps_arc: int = 24
        start_ang: float = j1_max
        end_ang: float = 2.0 * pi - j1_max
        for i in range(steps_arc + 1):
            ang: float = start_ang + (end_ang - start_ang) * (i / steps_arc)
            wx: float = r_max * cos(ang)
            wy: float = r_max * sin(ang)
            sx, sy = vp.world_to_screen(wx, wy, w, h)
            poly_pts.extend((sx, sy))

        # 2. Lower boundary curve: theta1 = -j1_max, theta2 from 0 to theta2_cross
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

        # 3. Upper boundary curve: theta1 = +j1_max, theta2 from theta2_cross down to 0
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
