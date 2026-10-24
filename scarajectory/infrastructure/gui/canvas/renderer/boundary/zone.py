# -*- coding: UTF-8 -*-

'''
Module
    zone.py
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

from math import degrees
from tkinter import Canvas
from typing import Final

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter

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

            :attributes:
                | _boundary_adapter - Injected workspace boundary calculation adapter.

            :methods:
                | __init__ - Initializes renderer with injected boundary adapter.
                | render_layer - Renders forbidden zone polygon and annotation.
                | get_layer_name - Returns unique identifier name of layer.
    '''

    _boundary_adapter: IWorkspaceBoundaryAdapter

    def __init__(
        self,
        boundary_adapter: IWorkspaceBoundaryAdapter
    ) -> None:
        '''
            Initializes renderer with injected boundary calculation adapter.

            :param boundary_adapter: Workspace boundary query adapter.
            :exceptions: None.
        '''
        self._boundary_adapter: Final[IWorkspaceBoundaryAdapter] = (
            boundary_adapter
        )

    def render_layer(
        self,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator
    ) -> None:
        '''
            Renders hatched forbidden zone wedge/polygon when joint 1 range is limited.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
            :exceptions: None.
        '''
        poly_pts = self._boundary_adapter.calculate_forbidden_zone_polygon(
            validator.bounds
        )
        if not poly_pts:
            return

        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()

        screen_pts: list[float] = []
        for pt in poly_pts:
            sx, sy = vp.world_to_screen(pt.x, pt.y, w, h)
            screen_pts.extend([sx, sy])

        if len(screen_pts) >= 6:
            canvas.create_polygon(
                screen_pts,
                fill='#201015',
                outline='#5a2028',
                width=1.5,
                tags='bg_grid'
            )

        lbl_x, lbl_y = vp.world_to_screen(-validator.r_max + 18.0, 0.0, w, h)
        j1_max: float = validator.bounds.joints.j1_max_rad
        j1_deg: float = degrees(j1_max)
        canvas.create_text(
            lbl_x,
            lbl_y,
            text=f'J1 LIMIT\n(±{j1_deg:.0f}°)',
            fill='#8a3040',
            font=('Helvetica', 7, 'italic'),
            justify='center',
            tags='bg_grid'
        )

    def get_layer_name(self) -> str:
        '''
            Returns unique identifier name of layer.

            :return: Layer name string.
            :exceptions: None.
        '''
        return 'forbidden_zone'
