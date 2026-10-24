# -*- coding: UTF-8 -*-

'''
Module
    renderer.py
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

from collections.abc import Sequence
from tkinter import Canvas

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.bundle import TrajectoryRenderBundle
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.node import CanvasWaypointNodeRenderer
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

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
                | get_version - Returns component version string.
    '''

    @classmethod
    def draw_trajectory(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        bundle: TrajectoryRenderBundle
    ) -> None:
        '''
            Renders trajectory path lines, waypoint node markers and selection rings.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param bundle: Injected TrajectoryRenderBundle instance.
            :exceptions: None.
        '''
        w: int = canvas.winfo_width()
        h: int = canvas.winfo_height()
        waypoints: Sequence[TrajectoryWaypoint] = bundle.store.waypoints

        if len(waypoints) > 1:
            coords: list[float] = [
                coord for pt in waypoints
                for coord in vp.world_to_screen(pt.x, pt.y, w, h)
            ]
            canvas.create_line(*coords, fill='#98c379', width=2)

        CanvasWaypointNodeRenderer.draw_nodes(
            canvas, vp, waypoints, bundle.validator
        )

        sel_idx: int = bundle.selection.selected_index
        if 0 <= sel_idx < len(waypoints):
            s_pt: TrajectoryWaypoint = waypoints[sel_idx]
            sel_x, sel_y = vp.world_to_screen(s_pt.x, s_pt.y, w, h)
            canvas.create_oval(
                sel_x - 9, sel_y - 9, sel_x + 9, sel_y + 9,
                outline='#e5c07b', width=2, dash=(2, 2)
            )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
