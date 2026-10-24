# -*- coding: UTF-8 -*-

'''
Module
    projector_test.py
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
    Unit tests for CoordinateProjector component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.transform.iprojector import ICoordinateProjector
from scarajectory.infrastructure.gui.canvas.transform.projector import CoordinateProjector
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CoordinateProjectorTestCase(TestCase):
    '''
        Test cases for CoordinateProjector coordinate mapping.

        It defines:

            :methods:
                | test_structural_conformance - Verifies conformance to ICoordinateProjector.
                | test_coordinate_roundtrip - Tests world to screen and screen to world roundtrip.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies conformance to ICoordinateProjector.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        projector = CoordinateProjector(vp)
        self.assertIsInstance(projector, ICoordinateProjector)

    def test_coordinate_roundtrip(self) -> None:
        '''
            Tests coordinate conversion roundtrip fidelity.

            :exceptions: None.
        '''
        vp = ViewportTransform()
        vp.scale = 1.5
        vp.pan_x = 50.0
        vp.pan_y = -20.0
        projector = CoordinateProjector(vp)
        w, h = 800, 600
        orig_wx, orig_wy = 120.5, -45.2

        sx, sy = projector.world_to_screen(orig_wx, orig_wy, w, h)
        calc_wx, calc_wy = projector.screen_to_world(sx, sy, w, h)

        self.assertAlmostEqual(orig_wx, calc_wx, places=4)
        self.assertAlmostEqual(orig_wy, calc_wy, places=4)


if __name__ == '__main__':
    main()
