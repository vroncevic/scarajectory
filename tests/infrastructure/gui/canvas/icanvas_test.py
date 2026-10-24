# -*- coding: UTF-8 -*-

'''
Module
    icanvas_test.py
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
    Unit tests for ICanvas protocol interface.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyCanvas:
    '''
        Dummy class implementing ICanvas protocol structurally.

        It defines:

            :methods:
                | set_tool_mode - Sets tool mode.
                | update_settings - Updates settings.
    '''

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Sets tool mode.

            :param mode: Tool mode enum.
            :exceptions: None.
        '''

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates settings.

            :param settings: Canvas settings DTO.
            :exceptions: None.
        '''


class ICanvasTestCase(TestCase):
    '''
        Test cases verifying ICanvas protocol implementation.

        It defines:

            :methods:
                | test_structural_conformance - Verifies dummy class conforms to protocol.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies dummy class conforms to protocol.

            :exceptions: None.
        '''
        dummy = DummyCanvas()
        self.assertIsInstance(dummy, ICanvas)


if __name__ == '__main__':
    main()
