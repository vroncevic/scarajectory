# -*- coding: UTF-8 -*-

'''
Module
    canvas_reach_boundary_renderer_test.py
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
    Unit tests for CanvasReachBoundaryRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.infrastructure.gui.canvas.render.reach_boundary_renderer import CanvasReachBoundaryRenderer
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
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
        self.ovals: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.texts: list[tuple[tuple[float, ...], dict[str, object]]] = []

    def winfo_width(self) -> int:
        return self.width

    def winfo_height(self) -> int:
        return self.height

    def create_oval(self, *args: float, **kwargs: object) -> int:
        self.ovals.append((args, kwargs))
        return len(self.ovals)

    def create_text(self, *args: float, **kwargs: object) -> int:
        self.texts.append((args, kwargs))
        return len(self.texts)


class CanvasReachBoundaryRendererTestCase(TestCase):
    '''
        Test cases verifying CanvasReachBoundaryRenderer layer behavior.
    '''

    def setUp(self) -> None:
        self.canvas = MockCanvas()
        self.vp = ViewportTransform()
        self.bounds = ScaraBoundsLoaderFactory.create().load_bounds()
        self.kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        self.validator = TrajectoryValidatorFactory.create(
            kinematics=self.kinematics
        )
        self.renderer = CanvasReachBoundaryRenderer()

    def test_layer_name(self) -> None:
        '''
            Tests layer identifier string.
        '''
        self.assertEqual(
            self.renderer.get_layer_name(), 'reach_boundary'
        )

    def test_render_layer(self) -> None:
        '''
            Tests drawing of outer reach and inner deadzone circles.
        '''
        self.renderer.render_layer(self.canvas, self.vp, self.validator)
        self.assertEqual(len(self.canvas.ovals), 2)
        self.assertEqual(len(self.canvas.texts), 2)


if __name__ == '__main__':
    main()
