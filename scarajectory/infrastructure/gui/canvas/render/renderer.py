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
    Unified CAD vector graphics and trajectory path rendering coordinator.
'''

from __future__ import annotations

from tkinter import Canvas
from typing import Final

from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.canvas.render.forbidden_zone_renderer import CanvasForbiddenZoneRenderer
from scarajectory.infrastructure.gui.canvas.render.polar_grid_renderer import CanvasPolarGridRenderer
from scarajectory.infrastructure.gui.canvas.render.preview_renderer import CanvasPreviewRenderer
from scarajectory.infrastructure.gui.canvas.render.reach_boundary_renderer import CanvasReachBoundaryRenderer
from scarajectory.infrastructure.gui.canvas.render.trajectory_renderer import CanvasTrajectoryRenderer
from scarajectory.infrastructure.gui.canvas.render.ilayer_renderer import ILayerRenderer
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
        Unified CAD rendering coordinator managing background, trajectory and tool preview.

        It defines:

            :methods:
                | draw_background - Renders visual CAD background layers.
                | draw_trajectory - Delegates to CanvasTrajectoryRenderer.
                | draw_preview - Delegates to CanvasPreviewRenderer.
    '''

    _BACKGROUND_LAYERS: Final[tuple[ILayerRenderer, ...]] = (
        CanvasPolarGridRenderer(),
        CanvasReachBoundaryRenderer(),
        CanvasForbiddenZoneRenderer(),
    )

    @classmethod
    def draw_background(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator,
    ) -> None:
        '''
            Renders polar rays, concentric distance rings, axes and limits.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
        '''
        for layer in cls._BACKGROUND_LAYERS:
            layer.render_layer(canvas, vp, validator)

    @classmethod
    def draw_trajectory(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        store: IWaypointStore,
        selection: IPlanSelectionCoordinator,
        validator: ITrajectoryValidator
    ) -> None:
        '''
            Renders trajectory path lines, waypoint node markers and
            selection rings.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param store: Injected IWaypointStore instance.
            :param selection: Injected IPlanSelectionCoordinator instance.
            :param validator: ITrajectoryValidator instance.
        '''
        CanvasTrajectoryRenderer.draw_trajectory(
            canvas, vp, store, selection, validator
        )

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
            :param drag_points: (drag_start, current_pos) coordinates in mm.
        '''
        CanvasPreviewRenderer.draw_preview(canvas, vp, tool_mode, drag_points)
