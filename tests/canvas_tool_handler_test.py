# -*- coding: UTF-8 -*-

'''
Module
    canvas_tool_handler_test.py
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
    Unit tests for CanvasToolHandler CAD geometry operations.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.canvas_settings_dto import CanvasSettingsDTO
from scarajectory.infrastructure.gui.components.canvas_tool_handler import CanvasToolHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasToolHandler(unittest.TestCase):
    '''
        Test cases for CanvasToolHandler geometry discretization and hit detection.

        It defines:

            :methods:
                | setUp - Initializes settings fixture.
                | test_hit_detection - Tests selecting nearest waypoint.
                | test_freehand_distance_check - Tests distance thresholding for continuous drawing.
                | test_discretize_line - Tests generating linear segment waypoints.
                | test_discretize_circle - Tests generating circular loop waypoints.
                | test_discretize_rectangle - Tests generating closed rectangular waypoints.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        self.settings = CanvasSettingsDTO(default_z=20.0, default_speed=40.0)

    def test_hit_detection(self) -> None:
        '''
            Tests find_hit_index algorithm.

            :exceptions: None.
        '''
        pts = [
            Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0),
            Waypoint(x=100.0, y=100.0, z=0.0, phi=0.0, speed=10.0)
        ]
        hit = CanvasToolHandler.find_hit_index(pts, 10.5, 19.8, 5.0)
        self.assertEqual(hit, 0)

        miss = CanvasToolHandler.find_hit_index(pts, 50.0, 50.0, 5.0)
        self.assertEqual(miss, -1)

    def test_freehand_distance_check(self) -> None:
        '''
            Tests distance threshold for adding freehand points.

            :exceptions: None.
        '''
        last = Waypoint(x=0.0, y=0.0, z=0.0, phi=0.0, speed=10.0)
        self.assertFalse(CanvasToolHandler.is_freehand_distance_met(last, 1.0, 1.0, 5.0))
        self.assertTrue(CanvasToolHandler.is_freehand_distance_met(last, 10.0, 0.0, 5.0))

    def test_discretize_line(self) -> None:
        '''
            Tests line waypoint generation.

            :exceptions: None.
        '''
        pts = CanvasToolHandler.discretize_line((0.0, 0.0), (100.0, 0.0), self.settings)
        self.assertEqual(len(pts), 2)
        self.assertEqual(pts[0].x, 0.0)
        self.assertEqual(pts[1].x, 100.0)

    def test_discretize_circle(self) -> None:
        '''
            Tests circle waypoint generation and loop closure.

            :exceptions: None.
        '''
        pts = CanvasToolHandler.discretize_circle((100.0, 100.0), 30.0, 8, self.settings)
        self.assertEqual(len(pts), 9)
        self.assertAlmostEqual(pts[0].x, pts[-1].x, places=3)
        self.assertAlmostEqual(pts[0].y, pts[-1].y, places=3)

    def test_discretize_rectangle(self) -> None:
        '''
            Tests rectangle waypoint generation and loop closure.

            :exceptions: None.
        '''
        pts = CanvasToolHandler.discretize_rectangle((10.0, 20.0), (50.0, 60.0), self.settings)
        self.assertEqual(len(pts), 5)
        self.assertEqual(pts[0].x, pts[-1].x)
        self.assertEqual(pts[0].y, pts[-1].y)


if __name__ == '__main__':
    unittest.main()
