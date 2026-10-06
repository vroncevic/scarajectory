# -*- coding: UTF-8 -*-

'''
Module
    polar_grid_renderer.py
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
    Visual CAD layer renderer for polar rays, concentric rings, and axes.
'''

from __future__ import annotations

from math import cos, radians, sin
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


class CanvasPolarGridRenderer:
    '''
        Visual CAD layer renderer for polar rays, concentric rings, and axes.

        It defines:

            :methods:
                | render_layer - Renders polar rays, concentric rings, axes.
                | get_layer_name - Returns unique identifier name of layer.
    '''

    def render_layer(
        self,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator,
    ) -> None:
        '''
            Renders polar rays, concentric rings, axes, and base marker.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        center: tuple[float, float] = vp.world_to_screen(0.0, 0.0, w, h)
        r_max: float = validator.r_max
        rmax_px: float = r_max * vp.scale

        for deg in (30, 60, 120, 150, 210, 240, 300, 330):
            canvas.create_line(
                center[0],
                center[1],
                center[0] + rmax_px * cos(radians(deg)),
                center[1] - rmax_px * sin(radians(deg)),
                fill='#232830',
                dash=(2, 6),
            )

        step_mm: float = 50.0
        current_r: float = step_mm

        while current_r < r_max:
            r_px: float = current_r * vp.scale
            canvas.create_oval(
                center[0] - r_px,
                center[1] - r_px,
                center[0] + r_px,
                center[1] + r_px,
                outline='#282c34',
                dash=(2, 4),
            )
            current_r += step_mm

        canvas.create_line(
            0, center[1], w, center[1], fill='#3e4451', width=1
        )
        canvas.create_line(
            center[0], 0, center[0], h, fill='#3e4451', width=1
        )
        canvas.create_text(
            w - 15,
            center[1] - 10,
            text='+X',
            fill='#61afef',
            font=('DejaVu Sans', 8, 'bold'),
        )
        canvas.create_text(
            center[0] + 15,
            12,
            text='+Y',
            fill='#61afef',
            font=('DejaVu Sans', 8, 'bold'),
        )
        canvas.create_oval(
            center[0] - 5,
            center[1] - 5,
            center[0] + 5,
            center[1] + 5,
            fill='#61afef',
            outline='#ffffff',
        )
        canvas.create_text(
            center[0] + 8,
            center[1] - 8,
            text='(0,0) BASE',
            fill='#61afef',
            font=('DejaVu Sans', 8, 'bold'),
            anchor='w',
        )

    def get_layer_name(self) -> str:
        '''
            Returns unique identifier name of layer.

            :return: Layer name string.
        '''
        return 'polar_grid'
