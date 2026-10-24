# -*- coding: UTF-8 -*-

'''
Module
    camera_test.py
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
    Unit tests for ViewportCamera component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.transform.camera import ViewportCamera
from scarajectory.infrastructure.gui.canvas.transform.icamera import IViewportCamera
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ViewportCameraTestCase(TestCase):
    '''
        Test cases for ViewportCamera zooming and scaling operations.

        It defines:

            :methods:
                | test_structural_conformance - Verifies conformance to IViewportCamera.
                | test_zoom_in_out - Tests scaling increments and decrements.
                | test_fit_reach - Tests automatic scaling to fit robot workspace.
                | test_reset - Tests reset to default scale and pan offsets.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies conformance to IViewportCamera.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        camera = ViewportCamera(vp)
        self.assertIsInstance(camera, IViewportCamera)

    def test_zoom_in_out(self) -> None:
        '''
            Tests zooming scale limits and operations.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        camera = ViewportCamera(vp)
        initial_scale = vp.scale
        camera.zoom_in()
        self.assertGreater(vp.scale, initial_scale)
        camera.zoom_out()
        self.assertAlmostEqual(vp.scale, initial_scale)

    def test_fit_reach(self) -> None:
        '''
            Tests auto-fit scaling algorithm.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        camera = ViewportCamera(vp)
        camera.fit_reach(800, 600, 270.0)
        self.assertGreater(vp.scale, 0.0)
        self.assertEqual(vp.pan_x, 0.0)
        self.assertEqual(vp.pan_y, 0.0)

    def test_reset(self) -> None:
        '''
            Tests resetting transform state.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        camera = ViewportCamera(vp)
        vp.scale = 3.0
        vp.pan_x = 100.0
        vp.pan_y = -50.0
        camera.reset()
        self.assertEqual(vp.scale, ViewportTransform.DEFAULT_ZOOM)
        self.assertEqual(vp.pan_x, 0.0)
        self.assertEqual(vp.pan_y, 0.0)


if __name__ == '__main__':
    main()
