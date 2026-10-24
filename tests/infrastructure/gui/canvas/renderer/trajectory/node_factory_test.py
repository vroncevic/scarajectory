# -*- coding: UTF-8 -*-

'''
Module
    node_factory_test.py
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
    Unit tests for CanvasWaypointNodeRendererFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.renderer.trajectory.node import CanvasWaypointNodeRenderer
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.node_factory import CanvasWaypointNodeRendererFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasWaypointNodeRendererFactoryTestCase(TestCase):
    '''
        Test cases for CanvasWaypointNodeRendererFactory.

        It defines:

            :methods:
                | test_factory_creates_instance - Verifies factory creates instance.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies factory creates CanvasWaypointNodeRenderer.

            :exceptions: None.
        '''
        renderer = CanvasWaypointNodeRendererFactory.create()
        self.assertIsInstance(renderer, CanvasWaypointNodeRenderer)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(CanvasWaypointNodeRendererFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
