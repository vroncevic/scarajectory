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

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.renderer.boundary.reach import CanvasReachBoundaryRenderer
from scarajectory.infrastructure.gui.canvas.renderer.boundary.zone_factory import CanvasForbiddenZoneRendererFactory
from scarajectory.infrastructure.gui.canvas.renderer.grid.renderer import CanvasPolarGridRenderer
from scarajectory.infrastructure.gui.canvas.renderer.layer.ilayer import ILayerRenderer
from scarajectory.infrastructure.gui.canvas.renderer.preview.renderer import CanvasPreviewRenderer
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.bundle import TrajectoryRenderBundle
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.renderer import CanvasTrajectoryRenderer
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter

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
                | get_version - Returns component version string.
    '''

    _STATIC_LAYERS: Final[tuple[ILayerRenderer, ...]] = (
        CanvasPolarGridRenderer(),
        CanvasReachBoundaryRenderer(),
    )

    @classmethod
    def draw_background(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator,
        boundary_adapter: IWorkspaceBoundaryAdapter,
    ) -> None:
        '''
            Renders polar rays, concentric distance rings, axes and limits.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
            :param boundary_adapter: Injected IWorkspaceBoundaryAdapter instance.
            :exceptions: None.
        '''
        for layer in cls._STATIC_LAYERS:
            layer.render_layer(canvas, vp, validator)
        zone_renderer = CanvasForbiddenZoneRendererFactory.create(boundary_adapter)
        zone_renderer.render_layer(canvas, vp, validator)



    @classmethod
    def draw_trajectory(
        cls,
        canvas: Canvas,
        vp: ViewportTransform,
        bundle: TrajectoryRenderBundle
    ) -> None:
        '''
            Renders trajectory path lines, waypoint node markers and
            selection rings.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param bundle: Injected TrajectoryRenderBundle instance.
            :exceptions: None.
        '''
        CanvasTrajectoryRenderer.draw_trajectory(canvas, vp, bundle)

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
            :exceptions: None.
        '''
        CanvasPreviewRenderer.draw_preview(canvas, vp, tool_mode, drag_points)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
