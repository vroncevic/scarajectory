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
    Unit tests for ICanvasViewportPanHandler protocol structural compliance.
'''

from __future__ import annotations

from tkinter import Event
from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.handler.pan.ihandler import ICanvasViewportPanHandler


class MockPanHandler:
    '''
        Mock conforming to ICanvasViewportPanHandler structurally.
    '''

    def try_start_pan(self, event: Event) -> bool:
        '''
            Checks event and initiates viewport pan.

            :param event: Tkinter mouse Event.
            :return: Boolean status.
        '''
        _ = event
        return True

    def pan_drag(self, event_x: int, event_y: int) -> bool:
        '''
            Translates viewport offsets during active drag.

            :param event_x: Mouse X coordinate.
            :param event_y: Mouse Y coordinate.
            :return: Boolean status.
        '''
        _ = (event_x, event_y)
        return True

    def stop_pan(self) -> bool:
        '''
            Terminates active viewport panning on release.

            :return: Boolean status.
        '''
        return True

    def is_panning(self) -> bool:
        '''
            Queries active panning state.

            :return: Boolean status.
        '''
        return False


class TestICanvasViewportPanHandler(TestCase):
    '''
        Test cases for ICanvasViewportPanHandler protocol compliance.

        It defines:

            :methods:
                | test_structural_compliance - Tests protocol runtime checkable conformance.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies mock satisfies ICanvasViewportPanHandler protocol.

            :exceptions: None.
        '''
        handler = MockPanHandler()
        self.assertIsInstance(handler, ICanvasViewportPanHandler)


if __name__ == '__main__':
    main()
