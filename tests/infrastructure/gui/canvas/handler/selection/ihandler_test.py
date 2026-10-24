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
    Unit tests for ICanvasSelectionMouseHandler protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.handler.selection.ihandler import ICanvasSelectionMouseHandler


class MockSelectionHandler:
    '''
        Mock conforming to ICanvasSelectionMouseHandler structurally.
    '''

    def handle_select_down(self, wx: float, wy: float) -> int:
        '''
            Processes mouse down for selection hit detection.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Hit index.
        '''
        _ = (wx, wy)
        return -1

    def handle_select_drag(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint during selection motion.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Boolean redraw status.
        '''
        _ = (wx, wy)
        return False

    def find_hit_index(self, wx: float, wy: float) -> int:
        '''
            Computes nearest waypoint index within hit radius.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Hit index.
        '''
        _ = (wx, wy)
        return -1

    def clear_selection(self) -> None:
        '''
            Clears active selection and dragged index.
        '''


class TestICanvasSelectionMouseHandler(TestCase):
    '''
        Test cases for ICanvasSelectionMouseHandler protocol compliance.

        It defines:

            :methods:
                | test_structural_compliance - Tests protocol runtime checkable conformance.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies mock satisfies ICanvasSelectionMouseHandler protocol.

            :exceptions: None.
        '''
        handler = MockSelectionHandler()
        self.assertIsInstance(handler, ICanvasSelectionMouseHandler)


if __name__ == '__main__':
    main()
