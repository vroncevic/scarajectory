# -*- coding: UTF-8 -*-

'''
Module
    icanvas_mouse_handler_test.py
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
    Unit testing for ICanvasMouseHandler protocol conformance.
'''

from __future__ import annotations

from tkinter import Event
from typing import Any
from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.handler.canvas_event_context import (
    CanvasEventContext,
)
from scarajectory.infrastructure.gui.canvas.handler.icanvas_mouse_handler import (
    ICanvasMouseHandler,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingCanvasMouseHandlerStub:
    '''Conforming stub implementation satisfying ICanvasMouseHandler.'''

    def handle_mouse_down(
        self, event: Event[Any], context: CanvasEventContext
    ) -> None:
        '''Handles mouse down.'''
        _ = (event, context)

    def handle_mouse_drag(
        self, event: Event[Any], context: CanvasEventContext
    ) -> bool:
        '''Handles mouse drag.'''
        _ = (event, context)
        return False

    def handle_mouse_up(
        self, event: Event[Any], context: CanvasEventContext
    ) -> None:
        '''Handles mouse up.'''
        _ = (event, context)

    def format_cursor_status(
        self, event: Event[Any], width: int, height: int
    ) -> str:
        '''Formats cursor status.'''
        _ = (event, width, height)
        return 'Status'


class IncompleteCanvasMouseHandlerStub:
    '''Non-conforming stub implementation missing format_cursor_status.'''

    def handle_mouse_down(
        self, event: Event[Any], context: CanvasEventContext
    ) -> None:
        '''Handles mouse down.'''
        _ = (event, context)

    def handle_mouse_drag(
        self, event: Event[Any], context: CanvasEventContext
    ) -> bool:
        '''Handles mouse drag.'''
        _ = (event, context)
        return False


class CanvasMouseHandlerProtocolTestCase(TestCase):
    '''
        Tests ICanvasMouseHandler runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies ICanvasMouseHandler protocol.'''
        stub = ConformingCanvasMouseHandlerStub()
        self.assertIsInstance(stub, ICanvasMouseHandler)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails ICanvasMouseHandler protocol check.'''
        stub = IncompleteCanvasMouseHandlerStub()
        self.assertNotIsInstance(stub, ICanvasMouseHandler)


if __name__ == '__main__':
    main()
