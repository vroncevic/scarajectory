# -*- coding: UTF-8 -*-

'''
Module
    canvas_renderer.py
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
    Unified CAD vector graphics and trajectory path rendering facade for Tkinter canvas.
'''

from __future__ import annotations

from tkinter import Canvas

from scarajectory.core.model.trajectory.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.canvas_background_renderer import CanvasBackgroundRenderer
from scarajectory.infrastructure.gui.canvas.canvas_preview_renderer import CanvasPreviewRenderer
from scarajectory.infrastructure.gui.canvas.canvas_trajectory_renderer import CanvasTrajectoryRenderer
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasRenderer:
    '''
        Unified CAD rendering facade coordinating background, trajectory, and tool preview sub-renderers.

        It defines:

            :methods:
                | draw_background - Delegates to CanvasBackgroundRenderer for polar grids and workspace limits.
                | draw_trajectory - Delegates to CanvasTrajectoryRenderer for trajectory paths, waypoints and nodes.
                | draw_preview - Delegates to CanvasPreviewRenderer for interactive CAD tool geometry preview.
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
        CanvasBackgroundRenderer.draw_background(canvas, vp, r_min_or_validator)

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
        CanvasTrajectoryRenderer.draw_trajectory(canvas, vp, plan, validator)

    @classmethod
    def draw_preview(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        tool_mode: CanvasToolMode,
        drag_points: tuple[tuple[float, float], tuple[float, float]]
    ) -> None:
        '''
            Renders interactive drag preview geometry for active CAD tool.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param tool_mode: Active CanvasToolMode.
            :param drag_points: Tuple of (drag_start, current_pos) coordinates in mm.
        '''
        CanvasPreviewRenderer.draw_preview(canvas, vp, tool_mode, drag_points)
