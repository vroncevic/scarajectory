# -*- coding: UTF-8 -*-

'''
Module
    reach.py
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
    Visual CAD layer renderer for reach limits and inner deadzone circles.
'''

from __future__ import annotations

from tkinter import Canvas

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasReachBoundaryRenderer:
    '''
        Visual CAD layer renderer for reach limits and inner deadzone.

        It defines:

            :methods:
                | render_layer - Renders outer reach and deadzone boundaries.
                | get_layer_name - Returns unique identifier name of layer.
    '''

    def render_layer(
        self,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator,
    ) -> None:
        '''
            Renders outer reach and inner deadzone circles and text.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        r_max: float = validator.r_max
        r_min: float = validator.r_min
        cx, cy = vp.world_to_screen(0.0, 0.0, w, h)

        # 1. Outer workspace reach circle (maximum physical extension)
        r_max_px: float = r_max * vp.scale
        canvas.create_oval(
            cx - r_max_px, cy - r_max_px, cx + r_max_px, cy + r_max_px,
            outline='#3a6ea5', width=2, dash=(6, 3), tags='bg_grid'
        )
        lx, ly = vp.world_to_screen(0.0, r_max, w, h)
        canvas.create_text(
            lx + 4, ly - 8, text=f'R_MAX {int(r_max)} mm',
            fill='#3a6ea5', font=('Helvetica', 8, 'bold'),
            anchor='w', tags='bg_grid'
        )

        # 2. Inner deadzone circle (singularity at origin / minimum extension)
        if r_min > 0.0:
            r_min_px: float = r_min * vp.scale
            canvas.create_oval(
                cx - r_min_px, cy - r_min_px, cx + r_min_px, cy + r_min_px,
                outline='#7a3030', fill='#1a1418', width=1.5, tags='bg_grid'
            )
            lx, ly = vp.world_to_screen(0.0, r_min, w, h)
            canvas.create_text(
                lx + 4, ly + 8, text=f'R_MIN {int(r_min)} mm',
                fill='#aa5050', font=('Helvetica', 8),
                anchor='w', tags='bg_grid'
            )

    def get_layer_name(self) -> str:
        '''
            Returns unique identifier name of layer.

            :return: Layer name string.
            :exceptions: None.
        '''
        return 'reach_boundary'
