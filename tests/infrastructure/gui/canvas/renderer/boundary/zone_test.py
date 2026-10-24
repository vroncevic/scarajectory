# -*- coding: UTF-8 -*-

'''
Module
    zone_test.py
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
    Unit tests for CanvasForbiddenZoneRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.pose.point_2d import Point2D

from scarajectory.infrastructure.gui.canvas.renderer.boundary.zone import CanvasForbiddenZoneRenderer
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
                | polygons - Recorded polygons.
                | texts - Recorded texts.
            :methods:
                | __init__ - Initializes mock canvas.
                | winfo_width - Returns canvas width.
                | winfo_height - Returns canvas height.
                | create_polygon - Records create_polygon call.
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
        self.polygons: list[tuple[tuple[float, ...], dict[str, object]]] = []
        self.texts: list[tuple[tuple[float, ...], dict[str, object]]] = []

    def winfo_width(self) -> int:
        '''
            Returns canvas width.

            :return: Width integer.
            :exceptions: None.
        '''
        return self.width

    def winfo_height(self) -> int:
        '''
            Returns canvas height.

            :return: Height integer.
            :exceptions: None.
        '''
        return self.height

    def create_polygon(self, *args: float, **kwargs: object) -> int:
        '''
            Records polygon draw call.

            :param args: Coordinates.
            :param kwargs: Options.
            :return: Polygon count integer.
            :exceptions: None.
        '''
        self.polygons.append((args, kwargs))
        return len(self.polygons)

    def create_text(self, *args: float, **kwargs: object) -> int:
        '''
            Records text draw call.

            :param args: Coordinates.
            :param kwargs: Options.
            :return: Text count integer.
            :exceptions: None.
        '''
        self.texts.append((args, kwargs))
        return len(self.texts)


class CanvasForbiddenZoneRendererTestCase(TestCase):
    '''
        Test cases verifying CanvasForbiddenZoneRenderer layer behavior.

        It defines:

            :methods:
                | setUp - Sets up test fixture with canvas, viewport transform, and mocks.
                | test_layer_name - Tests layer identifier string.
                | test_render_layer - Tests drawing of J1 limit forbidden crescent polygon and text.
                | test_render_layer_empty_polygon - Tests rendering when adapter returns empty polygon.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with canvas, viewport transform, and mocks.

            :exceptions: None.
        '''
        self.canvas = MockCanvas()
        self.vp = ViewportTransform()
        self.mock_adapter = MagicMock()
        self.mock_adapter.calculate_forbidden_zone_polygon.return_value = (
            Point2D(x=10.0, y=20.0),
            Point2D(x=30.0, y=40.0),
            Point2D(x=50.0, y=60.0),
        )
        self.renderer = CanvasForbiddenZoneRenderer(
            boundary_adapter=self.mock_adapter
        )
        self.mock_validator = MagicMock()
        self.mock_validator.r_max = 280.0
        self.mock_validator.bounds.joints.j1_max_rad = 2.61

    def test_layer_name(self) -> None:
        '''
            Tests layer identifier string.

            :exceptions: None.
        '''
        self.assertEqual(
            self.renderer.get_layer_name(), 'forbidden_zone'
        )

    def test_render_layer(self) -> None:
        '''
            Tests drawing of J1 limit forbidden crescent polygon and text.

            :exceptions: None.
        '''
        self.renderer.render_layer(self.canvas, self.vp, self.mock_validator)
        self.assertEqual(len(self.canvas.polygons), 1)
        self.assertEqual(len(self.canvas.texts), 1)
        self.mock_adapter.calculate_forbidden_zone_polygon.assert_called_once()

    def test_render_layer_empty_polygon(self) -> None:
        '''
            Tests rendering when boundary adapter returns empty polygon.

            :exceptions: None.
        '''
        self.mock_adapter.calculate_forbidden_zone_polygon.return_value = ()
        self.renderer.render_layer(self.canvas, self.vp, self.mock_validator)
        self.assertEqual(len(self.canvas.polygons), 0)


if __name__ == '__main__':
    main()
