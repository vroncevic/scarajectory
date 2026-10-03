# -*- coding: UTF-8 -*-

'''
Module
    reach_boundary_renderer.py
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

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
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
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        center: tuple[float, float] = vp.world_to_screen(0.0, 0.0, w, h)
        bounds = getattr(validator, 'bounds', None)
        deadzone_r = getattr(bounds, 'deadzone_r_min', None)
        r_min_mm: float = validator.r_min

        if isinstance(deadzone_r, (int, float)):
            r_min_mm = max(r_min_mm, float(deadzone_r))

        r_max: float = validator.r_max
        rmax_px: float = r_max * vp.scale
        rmin_px: float = r_min_mm * vp.scale

        canvas.create_oval(
            center[0] - rmax_px,
            center[1] - rmax_px,
            center[0] + rmax_px,
            center[1] + rmax_px,
            outline='#61afef',
            width=2,
        )
        canvas.create_oval(
            center[0] - rmin_px,
            center[1] - rmin_px,
            center[0] + rmin_px,
            center[1] + rmin_px,
            fill='#e06c75',
            stipple='gray25',
            outline='#e06c75',
            width=1,
            dash=(4, 4),
        )
        canvas.create_text(
            center[0] + rmax_px - 40,
            center[1] + rmax_px + 12,
            text=f'R_MAX ({r_max:.0f}mm)',
            fill='#61afef',
            font=('DejaVu Sans', 7),
        )
        canvas.create_text(
            center[0] + rmin_px + 15,
            center[1] + 10,
            text=f'DEADZONE ({r_min_mm:.0f}mm)',
            fill='#e06c75',
            font=('DejaVu Sans', 7),
        )

    def get_layer_name(self) -> str:
        '''
            Returns unique identifier name of layer.

            :return: Layer name string.
        '''
        return 'reach_boundary'
