# -*- coding: UTF-8 -*-

'''
Module
    forbidden_zone_renderer.py
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
    Visual CAD layer renderer for joint 1 limit forbidden crescent zone.
'''

from __future__ import annotations

from math import asin, cos, degrees, pi, sin
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


class CanvasForbiddenZoneRenderer:
    '''
        Visual CAD layer renderer for joint 1 limit forbidden crescent zone.

        It defines:

            :methods:
                | render_layer - Renders forbidden zone polygon and annotation.
                | get_layer_name - Returns unique identifier name of layer.
    '''

    def render_layer(
        self,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator,
    ) -> None:
        '''
            Renders unreachable rear boundary polygon and J1 limit label.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        r_max: float = validator.r_max
        l1: float = validator.bounds.links.l1
        l2: float = validator.bounds.links.l2
        j1_max: float = validator.bounds.joints.j1_max_rad

        poly_pts: list[float] = []
        steps_arc: int = 24
        start_ang: float = j1_max
        end_ang: float = 2.0 * pi - j1_max

        for i in range(steps_arc + 1):
            ang: float = start_ang + (end_ang - start_ang) * (i / steps_arc)
            sx, sy = vp.world_to_screen(
                r_max * cos(ang), r_max * sin(ang), w, h
            )
            poly_pts.extend((sx, sy))

        sin_target: float = min(1.0, (l1 * sin(j1_max)) / l2)
        theta2_cross: float = pi - asin(sin_target) - j1_max
        elbow_neg_x: float = l1 * cos(-j1_max)
        elbow_neg_y: float = l1 * sin(-j1_max)
        steps_curve: int = 16

        for i in range(steps_curve + 1):
            q2: float = theta2_cross * (i / steps_curve)
            arm2_ang: float = -j1_max - q2
            wx: float = elbow_neg_x + l2 * cos(arm2_ang)
            wy: float = elbow_neg_y + l2 * sin(arm2_ang)
            sx, sy = vp.world_to_screen(wx, wy, w, h)
            poly_pts.extend((sx, sy))

        elbow_pos_x: float = l1 * cos(j1_max)
        elbow_pos_y: float = l1 * sin(j1_max)

        for i in range(steps_curve, -1, -1):
            q2: float = theta2_cross * (i / steps_curve)
            arm2_ang: float = j1_max + q2
            wx: float = elbow_pos_x + l2 * cos(arm2_ang)
            wy: float = elbow_pos_y + l2 * sin(arm2_ang)
            sx, sy = vp.world_to_screen(wx, wy, w, h)
            poly_pts.extend((sx, sy))

        canvas.create_polygon(
            *poly_pts,
            fill='#e06c75',
            stipple='gray25',
            outline='#e06c75',
            width=1,
            dash=(4, 4),
        )
        lbl_x, lbl_y = vp.world_to_screen(-r_max + 18.0, 0.0, w, h)
        j1_deg: float = degrees(j1_max)
        canvas.create_text(
            lbl_x,
            lbl_y,
            text=f'J1 LIMIT\n(±{j1_deg:.0f}°)',
            fill='#e06c75',
            font=('DejaVu Sans', 7),
            justify='center',
        )

    def get_layer_name(self) -> str:
        '''
            Returns unique identifier name of layer.

            :return: Layer name string.
        '''
        return 'forbidden_zone'
