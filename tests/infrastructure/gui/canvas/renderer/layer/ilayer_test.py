# -*- coding: UTF-8 -*-

'''
Module
    ilayer_test.py
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
    Unit tests for ILayerRenderer protocol interface.
'''

from __future__ import annotations

from tkinter import Canvas
from unittest import TestCase, main

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.renderer.layer.ilayer import ILayerRenderer
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyLayerRenderer:
    '''
        Dummy class implementing ILayerRenderer protocol structurally.

        It defines:

            :methods:
                | render_layer - Renders dummy layer.
                | get_layer_name - Returns dummy layer name.
    '''

    def render_layer(
        self,
        canvas: Canvas,
        vp: ViewportTransform,
        validator: ITrajectoryValidator,
    ) -> None:
        '''
            Renders dummy layer.

            :param canvas: Target Tkinter canvas widget.
            :param vp: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
            :exceptions: None.
        '''

    def get_layer_name(self) -> str:
        '''
            Returns dummy layer name.

            :return: Layer name string.
            :exceptions: None.
        '''
        return 'dummy'


class ILayerRendererTestCase(TestCase):
    '''
        Test cases verifying ILayerRenderer protocol implementation.

        It defines:

            :methods:
                | test_structural_conformance - Verifies dummy class conforms to protocol.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies dummy class conforms to protocol.

            :exceptions: None.
        '''
        dummy: DummyLayerRenderer = DummyLayerRenderer()
        self.assertIsInstance(dummy, ILayerRenderer)


if __name__ == '__main__':
    main()
