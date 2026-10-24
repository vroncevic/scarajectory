# -*- coding: UTF-8 -*-

'''
Module
    reach_test.py
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
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.renderer.boundary.reach import CanvasReachBoundaryRenderer
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

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

        It defines:

            :attributes:
                | width - Canvas width.
                | height - Canvas height.
                | ovals - Recorded ovals.
                | texts - Recorded texts.
            :methods:
                | __init__ - Initializes mock canvas.
                | winfo_width - Returns canvas width.
                | winfo_height - Returns canvas height.
                | create_oval - Records create_oval call.
                | create_text - Records create_text call.
    '''

    def __init__(self, width: int = 800, height: int = 600) -> None:
        '''
            Initializes mock canvas.

            :param width: Canvas pixel width.
            :param height: Canvas pixel height.
            :exceptions: None.
        '''
        self.width = width
        self.height = height
        self.ovals: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.texts: list[tuple[tuple[float, ...], dict[str, object]]] = []

    def winfo_width(self) -> int:
        '''
            Returns mock canvas width.

            :return: Canvas width integer.
            :exceptions: None.
        '''
        return self.width

    def winfo_height(self) -> int:
        '''
            Returns mock canvas height.

            :return: Canvas height integer.
            :exceptions: None.
        '''
        return self.height

    def create_oval(self, *args: float, **kwargs: object) -> int:
        '''
            Records oval creation arguments.

            :param args: Coordinates.
            :param kwargs: Style attributes.
            :return: Unique item identifier.
            :exceptions: None.
        '''
        self.ovals.append((args, kwargs))
        return len(self.ovals)

    def create_text(self, *args: float, **kwargs: object) -> int:
        '''
            Records text creation arguments.

            :param args: Coordinates.
            :param kwargs: Style attributes.
            :return: Unique item identifier.
            :exceptions: None.
        '''
        self.texts.append((args, kwargs))
        return len(self.texts)


class CanvasReachBoundaryRendererTestCase(TestCase):
    '''
        Test cases verifying CanvasReachBoundaryRenderer layer behavior.

        It defines:

            :methods:
                | setUp - Sets up test fixture.
                | test_layer_name - Tests layer identifier string.
                | test_render_layer - Tests drawing of outer reach and inner deadzone circles.
                | test_render_layer_with_deadzone - Tests drawing with deadzone.
                | test_render_layer_with_different_radii - Tests drawing with different radius config.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.

            :exceptions: None.
        '''
        self.canvas = MockCanvas()
        self.vp = ViewportTransform()
        self.validator = MagicMock()
        self.validator.r_min = 86.0
        self.validator.r_max = 270.0
        self.renderer = CanvasReachBoundaryRenderer()

    def test_layer_name(self) -> None:
        '''
            Tests layer identifier string.

            :exceptions: None.
        '''
        self.assertEqual(
            self.renderer.get_layer_name(), 'reach_boundary'
        )

    def test_render_layer(self) -> None:
        '''
            Tests drawing of outer reach and inner deadzone circles.

            :exceptions: None.
        '''
        self.renderer.render_layer(self.canvas, self.vp, self.validator)
        self.assertEqual(len(self.canvas.ovals), 2)
        self.assertEqual(len(self.canvas.texts), 2)

    def test_render_layer_with_deadzone(self) -> None:
        '''
            Tests drawing of outer reach and inner deadzone circles with validator.r_min.

            :exceptions: None.
        '''
        mock_validator = MagicMock()
        mock_validator.r_min = 50.0
        mock_validator.r_max = 350.0
        self.renderer.render_layer(self.canvas, self.vp, mock_validator)
        self.assertEqual(len(self.canvas.ovals), 2)
        self.assertEqual(len(self.canvas.texts), 2)

    def test_render_layer_with_different_radii(self) -> None:
        '''
            Tests drawing with different radius configuration.

            :exceptions: None.
        '''
        mock_validator = MagicMock()
        mock_validator.r_min = 86.0
        mock_validator.r_max = 270.0
        self.renderer.render_layer(self.canvas, self.vp, mock_validator)
        self.assertEqual(len(self.canvas.ovals), 2)
        self.assertEqual(len(self.canvas.texts), 2)


if __name__ == '__main__':
    main()
