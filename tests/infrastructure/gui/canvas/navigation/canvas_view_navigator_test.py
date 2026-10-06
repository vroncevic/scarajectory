# -*- coding: UTF-8 -*-

'''
Module
    canvas_view_navigator_test.py
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
    Unit tests for CanvasViewNavigator and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.navigation.canvas_view_navigator import CanvasViewNavigator
from scarajectory.infrastructure.gui.canvas.navigation.canvas_view_navigator_factory import CanvasViewNavigatorFactory
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasViewNavigator(TestCase):
    '''Test cases verifying CanvasViewNavigator viewport manipulations.'''

    def setUp(self) -> None:
        self.mock_vp = MagicMock()
        self.mock_validator = MagicMock()
        self.mock_validator.r_max = 350.0
        self.mock_target = MagicMock()
        self.mock_target.get_view_dimensions.return_value = (800, 600)
        self.navigator: CanvasViewNavigator = CanvasViewNavigatorFactory.create(
            viewport=self.mock_vp,
            validator=self.mock_validator,
            target=self.mock_target,
        )

    def test_protocol_conformance(self) -> None:
        self.assertIsInstance(self.navigator, ICanvasViewNavigator)
        self.assertEqual(CanvasViewNavigatorFactory.get_version(), '1.0.3')

    def test_fit_reach_view(self) -> None:
        self.navigator.fit_reach_view()
        self.mock_target.get_view_dimensions.assert_called_once()
        self.mock_vp.fit_reach.assert_called_once_with(800, 600, 350.0)
        self.mock_target.redraw.assert_called_once()

    def test_reset_view(self) -> None:
        self.navigator.reset_view()
        self.mock_vp.reset.assert_called_once()
        self.mock_target.redraw.assert_called_once()

    def test_zoom_in(self) -> None:
        self.navigator.zoom_in()
        self.mock_vp.zoom_in.assert_called_once()
        self.mock_target.redraw.assert_called_once()

    def test_zoom_out(self) -> None:
        self.navigator.zoom_out()
        self.mock_vp.zoom_out.assert_called_once()
        self.mock_target.redraw.assert_called_once()


if __name__ == '__main__':
    main()
