# -*- coding: UTF-8 -*-

'''
Module
    inavigator_test.py
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
    Unit tests for ICanvasViewNavigator protocol interface.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyNavigator:
    '''
        Dummy class implementing ICanvasViewNavigator protocol structurally.

        It defines:

            :methods:
                | fit_reach_view - Fits maximum reach circle into viewport.
                | reset_view - Resets viewport zoom to 100% and centers workspace.
                | zoom_in - Scales viewport view in by zoom factor.
                | zoom_out - Scales viewport view out by zoom factor.
    '''

    def fit_reach_view(self) -> None:
        '''
            Fits maximum reach circle into viewport.

            :exceptions: None.
        '''

    def reset_view(self) -> None:
        '''
            Resets viewport zoom to 100% and centers workspace.

            :exceptions: None.
        '''

    def zoom_in(self) -> None:
        '''
            Scales viewport view in by zoom factor.

            :exceptions: None.
        '''

    def zoom_out(self) -> None:
        '''
            Scales viewport view out by zoom factor.

            :exceptions: None.
        '''


class ICanvasViewNavigatorTestCase(TestCase):
    '''
        Test cases verifying ICanvasViewNavigator protocol implementation.

        It defines:

            :methods:
                | test_structural_conformance - Verifies dummy class conforms to protocol.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies dummy class conforms to protocol.

            :exceptions: None.
        '''
        dummy: DummyNavigator = DummyNavigator()
        self.assertIsInstance(dummy, ICanvasViewNavigator)


if __name__ == '__main__':
    main()
