# -*- coding: UTF-8 -*-

'''
Module
    canvas_mouse_handler_test.py
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
    Unit tests for CanvasMouseHandler CAD mouse interaction component.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.model.trajectory.trajectory_plan import TrajectoryPlan
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform
from scarajectory.infrastructure.gui.canvas.canvas_mouse_handler import CanvasMouseHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyEvent:
    '''
        Dummy event object mimicking Tkinter mouse event attributes.
    '''

    def __init__(self, x: int, y: int, num: int = 1, delta: int = 0) -> None:
        self.x = x
        self.y = y
        self.num = num
        self.delta = delta


class TestCanvasMouseHandler(TestCase):
    '''
        Test cases for CanvasMouseHandler mouse interaction logic.

        It defines:

            :methods:
                | setUp - Initializes fixtures for plan, viewport, and mouse handler.
                | test_mouse_down_panning - Tests initiating viewport pan with button 2 or 3.
                | test_mouse_down_select_hit - Tests waypoint selection on hit.
                | test_mouse_drag_pan - Tests viewport pan movement.
                | test_mouse_up_point_tool - Tests committing single point with point tool.
                | test_format_cursor_status - Tests formatting status readout string.
    '''

    def setUp(self) -> None:
        '''
            Initializes fixtures for plan, viewport, and mouse handler.

            :exceptions: None.
        '''
        self.plan = TrajectoryPlan()
        self.vp = ViewportTransform()
        self.state = CanvasInteractionState()
        self.settings = CanvasSettings(default_z=15.0, default_speed=35.0)
        self.handler = CanvasMouseHandler(self.plan, self.vp, self.state)

    def test_mouse_down_panning(self) -> None:
        '''
            Tests initiating viewport pan with button 2 or 3.

            :exceptions: None.
        '''
        event = DummyEvent(x=100, y=150, num=2)
        self.handler.handle_mouse_down(event, 800, 600, CanvasToolMode.POINT, self.settings)
        self.assertTrue(self.state.is_panning)
        self.assertEqual(self.state.pan_x, 100)
        self.assertEqual(self.state.pan_y, 150)

    def test_mouse_down_select_hit(self) -> None:
        '''
            Tests waypoint selection on hit.

            :exceptions: None.
        '''
        pt = Waypoint(x=0.0, y=0.0, z=10.0, phi=0.0, speed=20.0)
        self.plan.add_point(pt)

        # Center of screen (400, 300) corresponds to world (0, 0)
        event = DummyEvent(x=400, y=300, num=1)
        self.handler.handle_mouse_down(event, 800, 600, CanvasToolMode.SELECT, self.settings)

        self.assertEqual(self.state.dragged_node_idx, 0)
        self.assertEqual(self.plan.selected_index, 0)

    def test_mouse_drag_pan(self) -> None:
        '''
            Tests viewport pan movement.

            :exceptions: None.
        '''
        self.state.is_panning = True
        self.state.pan_x = 100
        self.state.pan_y = 100

        event = DummyEvent(x=120, y=115, num=1)
        redraw_needed = self.handler.handle_mouse_drag(
            event, 800, 600, CanvasToolMode.POINT, self.settings
        )
        self.assertTrue(redraw_needed)
        self.assertEqual(self.vp.pan_x, 20.0)
        self.assertEqual(self.vp.pan_y, 15.0)

    def test_mouse_up_point_tool(self) -> None:
        '''
            Tests committing single point with point tool.

            :exceptions: None.
        '''
        down_evt = DummyEvent(x=450, y=250, num=1)
        self.handler.handle_mouse_down(down_evt, 800, 600, CanvasToolMode.POINT, self.settings)

        up_evt = DummyEvent(x=450, y=250, num=1)
        self.handler.handle_mouse_up(up_evt, 800, 600, CanvasToolMode.POINT, self.settings)

        self.assertEqual(self.plan.count, 1)
        self.assertEqual(self.plan.waypoints[0].z, 15.0)
        self.assertEqual(self.plan.waypoints[0].speed, 35.0)
        self.assertIsNone(self.state.drag_start_world)

    def test_format_cursor_status(self) -> None:
        '''
            Tests formatting status readout string.

            :exceptions: None.
        '''
        event = DummyEvent(x=400, y=300)
        status_text = self.handler.format_cursor_status(event, 800, 600)
        self.assertIn('Cursor: X=', status_text)
        self.assertIn('Zoom:', status_text)


if __name__ == '__main__':
    main()
