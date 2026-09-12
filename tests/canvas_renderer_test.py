# -*- coding: UTF-8 -*-

'''
Module
    canvas_renderer_test.py
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
    Unit tests for decomposed CanvasRenderer and its specialized sub-renderers.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir: str = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.kinematics.kinematics_service import KinematicsService
from scarajectory.core.service.trajectory.trajectory_validator import TrajectoryValidator
from scarajectory.infrastructure.gui.canvas.canvas_background_renderer import CanvasBackgroundRenderer
from scarajectory.infrastructure.gui.canvas.canvas_preview_renderer import CanvasPreviewRenderer
from scarajectory.infrastructure.gui.canvas.canvas_renderer import CanvasRenderer
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


class MockCanvas:
    '''
        Mock Tkinter canvas recording draw commands for headless testing.
    '''

    def __init__(self, width: int = 800, height: int = 600) -> None:
        self.width = width
        self.height = height
        self.lines: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.ovals: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.texts: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.polygons: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.rectangles: list[tuple[tuple[float, ...], dict[str, object]]] = []

    def winfo_width(self) -> int:
        return self.width

    def winfo_height(self) -> int:
        return self.height

    def create_line(self, *args: float, **kwargs: object) -> int:
        self.lines.append((args, kwargs))
        return len(self.lines)

    def create_oval(self, *args: float, **kwargs: object) -> int:
        self.ovals.append((args, kwargs))
        return len(self.ovals)

    def create_text(self, *args: float, **kwargs: object) -> int:
        self.texts.append((args, kwargs))
        return len(self.texts)

    def create_polygon(self, *args: float, **kwargs: object) -> int:
        self.polygons.append((args, kwargs))
        return len(self.polygons)

    def create_rectangle(self, *args: float, **kwargs: object) -> int:
        self.rectangles.append((args, kwargs))
        return len(self.rectangles)


class TestCanvasRenderer(TestCase):
    '''
        Test cases validating CanvasRenderer facade and sub-renderers.

        It defines:

            :methods:
                | setUp - Initializes fixtures for mock canvas, viewport, plan, and validator.
                | test_canvas_background_renderer - Tests background polar grid and workspace limits drawing.
                | test_canvas_trajectory_renderer - Tests trajectory lines, nodes, and selection ring drawing.
                | test_canvas_preview_renderer - Tests CAD tool preview geometries.
                | test_canvas_renderer_facade - Tests facade delegation to sub-renderers.
    '''

    def setUp(self) -> None:
        '''
            Initializes fixtures for mock canvas, viewport, plan, and validator.

            :exceptions: None.
        '''
        self.canvas = MockCanvas()
        self.vp = ViewportTransform()
        self.bounds = ScaraBounds()
        self.kinematics = KinematicsService(bounds=self.bounds)
        self.validator = TrajectoryValidator(bounds=self.bounds, kinematics=self.kinematics)
        self.plan = TrajectoryPlan()

    def test_canvas_background_renderer(self) -> None:
        '''
            Tests background polar grid and workspace limits drawing.

            :exceptions: None.
        '''
        CanvasBackgroundRenderer.draw_background(self.canvas, self.vp, self.validator)

        self.assertGreater(len(self.canvas.lines), 0)
        self.assertGreater(len(self.canvas.ovals), 0)
        self.assertGreater(len(self.canvas.texts), 0)
        self.assertEqual(len(self.canvas.polygons), 1)

    def test_canvas_trajectory_renderer(self) -> None:
        '''
            Tests trajectory lines, nodes, and selection ring drawing.

            :exceptions: None.
        '''
        self.plan.add_point(Waypoint(x=100.0, y=100.0, z=0.0, speed=50.0))
        self.plan.add_point(Waypoint(x=150.0, y=120.0, z=0.0, speed=50.0))
        self.plan.set_selected_index(0)

        CanvasTrajectoryRenderer.draw_trajectory(self.canvas, self.vp, self.plan, self.validator)

        self.assertEqual(len(self.canvas.lines), 1)
        self.assertEqual(len(self.canvas.ovals), 3)
        self.assertEqual(len(self.canvas.texts), 2)

    def test_canvas_preview_renderer(self) -> None:
        '''
            Tests CAD tool preview geometries for circle, rectangle, and line modes.

            :exceptions: None.
        '''
        drag_pts: tuple[tuple[float, float], tuple[float, float]] = ((50.0, 50.0), (100.0, 100.0))

        CanvasPreviewRenderer.draw_preview(self.canvas, self.vp, CanvasToolMode.CIRCLE, drag_pts)
        self.assertGreater(len(self.canvas.ovals), 0)

        CanvasPreviewRenderer.draw_preview(self.canvas, self.vp, CanvasToolMode.RECTANGLE, drag_pts)
        self.assertGreater(len(self.canvas.rectangles), 0)

        CanvasPreviewRenderer.draw_preview(self.canvas, self.vp, CanvasToolMode.LINE, drag_pts)
        self.assertGreater(len(self.canvas.lines), 0)

    def test_canvas_renderer_facade(self) -> None:
        '''
            Tests that CanvasRenderer facade delegates calls to all 3 sub-renderers.

            :exceptions: None.
        '''
        self.plan.add_point(Waypoint(x=120.0, y=80.0, z=0.0, speed=50.0))
        CanvasRenderer.draw_background(self.canvas, self.vp, self.validator)
        CanvasRenderer.draw_trajectory(self.canvas, self.vp, self.plan, self.validator)
        CanvasRenderer.draw_preview(
            self.canvas,
            self.vp,
            CanvasToolMode.CIRCLE,
            ((0.0, 0.0), (50.0, 50.0))
        )

        self.assertGreater(len(self.canvas.lines), 0)
        self.assertGreater(len(self.canvas.ovals), 0)
        self.assertGreater(len(self.canvas.texts), 0)
        self.assertGreater(len(self.canvas.polygons), 0)


if __name__ == '__main__':
    main()
