# -*- coding: UTF-8 -*-

'''
Module
    renderer_test.py
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
    Unit tests for CanvasPolarGridRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.renderer.grid.renderer import CanvasPolarGridRenderer
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
                | lines - Recorded lines.
                | ovals - Recorded ovals.
                | texts - Recorded texts.
            :methods:
                | __init__ - Initializes mock canvas.
                | winfo_width - Returns canvas width.
                | winfo_height - Returns canvas height.
                | create_line - Records create_line call.
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
        self.lines: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.ovals: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.texts: list[tuple[tuple[float, ...], dict[str, object]]] = []

    def winfo_width(self) -> int:
        '''
            Returns canvas width.

            :return: Canvas width integer.
            :exceptions: None.
        '''
        return self.width

    def winfo_height(self) -> int:
        '''
            Returns canvas height.

            :return: Canvas height integer.
            :exceptions: None.
        '''
        return self.height

    def create_line(self, *args: float, **kwargs: object) -> int:
        '''
            Records create_line call.

            :param args: Coordinates.
            :param kwargs: Style attributes.
            :return: Unique item identifier.
            :exceptions: None.
        '''
        self.lines.append((args, kwargs))
        return len(self.lines)

    def create_oval(self, *args: float, **kwargs: object) -> int:
        '''
            Records create_oval call.

            :param args: Coordinates.
            :param kwargs: Style attributes.
            :return: Unique item identifier.
            :exceptions: None.
        '''
        self.ovals.append((args, kwargs))
        return len(self.ovals)

    def create_text(self, *args: float, **kwargs: object) -> int:
        '''
            Records create_text call.

            :param args: Coordinates.
            :param kwargs: Style attributes.
            :return: Unique item identifier.
            :exceptions: None.
        '''
        self.texts.append((args, kwargs))
        return len(self.texts)


class CanvasPolarGridRendererTestCase(TestCase):
    '''
        Test cases verifying CanvasPolarGridRenderer layer behavior.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and dependencies.
                | test_layer_name - Tests layer identifier string.
                | test_render_layer - Tests drawing of polar rays, concentric rings, and axes.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures and dependencies.

            :exceptions: None.
        '''
        self.canvas = MockCanvas()
        self.vp = ViewportTransform()
        self.validator = MagicMock()
        self.validator.r_min = 86.0
        self.validator.r_max = 270.0
        self.renderer = CanvasPolarGridRenderer()

    def test_layer_name(self) -> None:
        '''
            Tests layer identifier string.

            :exceptions: None.
        '''
        self.assertEqual(self.renderer.get_layer_name(), 'polar_grid')

    def test_render_layer(self) -> None:
        '''
            Tests drawing of polar rays, concentric rings, and axes.

            :exceptions: None.
        '''
        self.renderer.render_layer(self.canvas, self.vp, self.validator)
        self.assertGreater(len(self.canvas.lines), 0)
        self.assertGreater(len(self.canvas.ovals), 0)
        self.assertGreater(len(self.canvas.texts), 0)


if __name__ == '__main__':
    main()
