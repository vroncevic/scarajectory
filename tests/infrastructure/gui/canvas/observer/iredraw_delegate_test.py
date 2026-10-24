# -*- coding: UTF-8 -*-

'''
Module
    iredraw_delegate_test.py
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
    Unit tests for ICanvasRedrawDelegate structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.observer.iredraw_delegate import ICanvasRedrawDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyRedrawDelegate:
    '''
        Dummy class implementing ICanvasRedrawDelegate for testing.

        It defines:

            :methods:
                | redraw - Performs redraw action.
                | get_view_dimensions - Returns dummy view dimensions.
    '''

    def redraw(self) -> None:
        '''
            Performs dummy redraw action.

            :exceptions: None.
        '''

    def get_view_dimensions(self) -> tuple[int, int]:
        '''
            Returns dummy view dimensions in pixels.

            :return: Tuple of width and height in pixels.
            :exceptions: None.
        '''
        return 800, 600


class TestICanvasRedrawDelegate(TestCase):
    '''
        Test cases verifying ICanvasRedrawDelegate protocol properties.
    '''

    def test_protocol_implementation(self) -> None:
        '''
            Verifies that DummyRedrawDelegate satisfies ICanvasRedrawDelegate.

            :exceptions: None.
        '''
        delegate = DummyRedrawDelegate()
        self.assertIsInstance(delegate, ICanvasRedrawDelegate)
        self.assertEqual(delegate.get_view_dimensions(), (800, 600))


if __name__ == '__main__':
    main()
