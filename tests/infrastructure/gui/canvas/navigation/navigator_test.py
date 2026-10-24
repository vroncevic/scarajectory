# -*- coding: UTF-8 -*-

'''
Module
    navigator_test.py
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
    Unit tests for CanvasViewNavigator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.navigation.navigator import CanvasViewNavigator
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasViewNavigatorTestCase(TestCase):
    '''
        Test cases verifying CanvasViewNavigator viewport manipulations.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and mocks.
                | test_protocol_conformance - Verifies protocol conformance.
                | test_fit_reach_view - Verifies fitting reach circle into viewport.
                | test_reset_view - Verifies resetting viewport.
                | test_zoom_in - Verifies scaling viewport view in.
                | test_zoom_out - Verifies scaling viewport view out.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures and mocks.

            :exceptions: None.
        '''
        self.mock_camera = MagicMock()
        self.mock_validator = MagicMock()
        self.mock_validator.r_max = 350.0
        self.mock_target = MagicMock()
        self.mock_target.get_view_dimensions.return_value = (800, 600)
        self.navigator: CanvasViewNavigator = CanvasViewNavigator(
            self.mock_camera,
            self.mock_validator,
            self.mock_target,
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self.navigator, ICanvasViewNavigator)

    def test_fit_reach_view(self) -> None:
        '''
            Verifies fitting reach circle into viewport.

            :exceptions: None.
        '''
        self.navigator.fit_reach_view()
        self.mock_target.get_view_dimensions.assert_called_once()
        self.mock_camera.fit_reach.assert_called_once_with(800, 600, 350.0)
        self.mock_target.redraw.assert_called_once()

    def test_reset_view(self) -> None:
        '''
            Verifies resetting viewport.

            :exceptions: None.
        '''
        self.navigator.reset_view()
        self.mock_camera.reset.assert_called_once()
        self.mock_target.redraw.assert_called_once()

    def test_zoom_in(self) -> None:
        '''
            Verifies scaling viewport view in.

            :exceptions: None.
        '''
        self.navigator.zoom_in()
        self.mock_camera.zoom_in.assert_called_once()
        self.mock_target.redraw.assert_called_once()

    def test_zoom_out(self) -> None:
        '''
            Verifies scaling viewport view out.

            :exceptions: None.
        '''
        self.navigator.zoom_out()
        self.mock_camera.zoom_out.assert_called_once()
        self.mock_target.redraw.assert_called_once()


if __name__ == '__main__':
    main()
