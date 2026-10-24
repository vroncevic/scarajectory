# -*- coding: UTF-8 -*-

'''
Module
    ihandler_test.py
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
    Unit tests for ICanvasDragHandler protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.handler.drag.ihandler import ICanvasDragHandler
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings


class MockDragHandler:
    '''
        Mock conforming to ICanvasDragHandler structurally.
    '''

    def handle_drag_select(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint during select tool drag.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Boolean status.
        '''
        _ = (wx, wy)
        return False

    def handle_drag_freehand(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> bool:
        '''
            Samples and appends waypoints along freehand path.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active settings.
            :return: Boolean status.
        '''
        _ = (wx, wy, settings)
        return False


class TestICanvasDragHandler(TestCase):
    '''
        Test cases for ICanvasDragHandler protocol compliance.

        It defines:

            :methods:
                | test_structural_compliance - Tests protocol runtime checkable conformance.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies mock satisfies ICanvasDragHandler protocol.

            :exceptions: None.
        '''
        handler = MockDragHandler()
        self.assertIsInstance(handler, ICanvasDragHandler)


if __name__ == '__main__':
    main()
