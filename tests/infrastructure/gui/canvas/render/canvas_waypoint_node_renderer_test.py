# -*- coding: UTF-8 -*-

'''
Module
    canvas_waypoint_node_renderer_test.py
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
    Unit tests for CanvasWaypointNodeRenderer component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.canvas.render.waypoint_node_renderer import CanvasWaypointNodeRenderer
from scarajectory.infrastructure.gui.canvas.render.waypoint_node_renderer_factory import CanvasWaypointNodeRendererFactory
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasWaypointNodeRenderer(TestCase):
    '''
        Test cases for CanvasWaypointNodeRenderer.
    '''

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies factory creates CanvasWaypointNodeRenderer.
        '''
        renderer = CanvasWaypointNodeRendererFactory.create()
        self.assertIsInstance(renderer, CanvasWaypointNodeRenderer)

    def test_draw_nodes_renders_ovals_and_text(self) -> None:
        '''
            Verifies draw_nodes creates oval and text on Tkinter canvas.
        '''
        mock_canvas = MagicMock()
        mock_canvas.winfo_width.return_value = 800
        mock_canvas.winfo_height.return_value = 600
        vp = ViewportTransform()
        waypoints = [
            Waypoint(x=100.0, y=100.0, z=0.0, phi=0.0, speed=100.0),
            Waypoint(x=150.0, y=150.0, z=0.0, phi=0.0, speed=100.0),
        ]
        mock_validator = MagicMock()
        mock_validator.validate_point.return_value.is_valid = True

        renderer = CanvasWaypointNodeRenderer()
        renderer.draw_nodes(mock_canvas, vp, waypoints, mock_validator)

        self.assertEqual(mock_canvas.create_oval.call_count, 2)
        self.assertEqual(mock_canvas.create_text.call_count, 2)
