# -*- coding: UTF-8 -*-

'''
Module
    viewport_transform_test.py
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
    Unit tests for ViewportTransform.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestViewportTransform(unittest.TestCase):
    '''
        Test cases for ViewportTransform math and coordinate mapping.

        It defines:

            :methods:
                | test_coordinate_roundtrip - Tests world to screen and screen to world roundtrip.
                | test_zoom_in_out - Tests scaling increments and decrements.
                | test_fit_reach - Tests automatic scaling to fit robot workspace.
                | test_reset - Tests reset to default scale and pan offsets.
    '''

    def test_coordinate_roundtrip(self) -> None:
        '''
            Tests coordinate conversion roundtrip fidelity.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        vp.scale = 1.5
        vp.pan_x = 50.0
        vp.pan_y = -20.0
        w, h = 800, 600
        orig_wx, orig_wy = 120.5, -45.2

        sx, sy = vp.world_to_screen(orig_wx, orig_wy, w, h)
        calc_wx, calc_wy = vp.screen_to_world(sx, sy, w, h)

        self.assertAlmostEqual(orig_wx, calc_wx, places=4)
        self.assertAlmostEqual(orig_wy, calc_wy, places=4)

    def test_zoom_in_out(self) -> None:
        '''
            Tests zooming scale limits and operations.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        initial_scale = vp.scale
        vp.zoom_in()
        self.assertGreater(vp.scale, initial_scale)
        vp.zoom_out()
        self.assertAlmostEqual(vp.scale, initial_scale)

    def test_fit_reach(self) -> None:
        '''
            Tests auto-fit scaling algorithm.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        vp.fit_reach(800, 600)
        self.assertGreater(vp.scale, 0.0)
        self.assertEqual(vp.pan_x, 0.0)
        self.assertEqual(vp.pan_y, 0.0)

    def test_reset(self) -> None:
        '''
            Tests resetting transform state.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        vp.scale = 3.0
        vp.pan_x = 100.0
        vp.pan_y = 50.0
        vp.reset()
        self.assertEqual(vp.scale, ViewportTransform.DEFAULT_ZOOM)
        self.assertEqual(vp.pan_x, 0.0)
        self.assertEqual(vp.pan_y, 0.0)


if __name__ == '__main__':
    unittest.main()
