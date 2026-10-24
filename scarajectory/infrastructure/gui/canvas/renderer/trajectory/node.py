# -*- coding: UTF-8 -*-

'''
Module
    node.py
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
    Vector rendering component for waypoint circle markers and coordinate labels.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Canvas

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasWaypointNodeRenderer:
    '''
        Renders waypoint circle markers, validity colors, and coordinate labels on Tkinter canvas.

        It defines:

            :methods:
                | draw_nodes - Renders waypoint circle markers and point labels.
                | get_version - Returns component version string.
    '''

    @classmethod
    def draw_nodes(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        waypoints: Sequence[TrajectoryWaypoint],
        validator: ITrajectoryValidator
    ) -> None:
        '''
            Renders waypoint circle markers and point labels.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param waypoints: Sequence of TrajectoryWaypoints.
            :param validator: ITrajectoryValidator instance.
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()

        for idx, pt in enumerate(waypoints):
            sx, sy = vp.world_to_screen(pt.x, pt.y, w, h)
            is_valid: bool = validator.validate_point(pt).is_valid

            # Color node: green for reachable, orange/red for kinematic violation
            node_fill = '#38ef7d' if is_valid else '#f45c43'
            node_outline = '#11998e' if is_valid else '#eb3349'
            r: float = 4.5

            canvas.create_oval(
                sx - r, sy - r, sx + r, sy + r,
                fill=node_fill, outline=node_outline, width=1.5,
                tags=f'wp_{idx}'
            )

            # Waypoint sequence index label
            canvas.create_text(
                sx, sy - 10,
                text=f'P{idx}',
                fill='#e0e0e0', font=('Helvetica', 8, 'bold'),
                anchor='s', tags=f'wp_lbl_{idx}'
            )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
