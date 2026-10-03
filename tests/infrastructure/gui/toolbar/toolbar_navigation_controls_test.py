# -*- coding: UTF-8 -*-

'''
Module
    toolbar_navigation_controls_test.py
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
    Unit tests for ToolbarNavigationControls and its factory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.toolbar.navigation_controls import ToolbarNavigationControls
from scarajectory.infrastructure.gui.toolbar.navigation_controls_factory import ToolbarNavigationControlsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolbarNavigationControls(TestCase):
    '''
        Test cases verifying viewport navigation and history controls.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def setUp(self) -> None:
        self.mock_navigator = MagicMock()
        self.mock_history = MagicMock()
        self.controls: ToolbarNavigationControls = (
            ToolbarNavigationControlsFactory.create(
                self.root, self.mock_navigator, self.mock_history
            )
        )

    def tearDown(self) -> None:
        self.controls.destroy()

    def test_reset_view_delegation(self) -> None:
        '''
            Tests that reset_view delegates to navigator reset_view.
        '''
        self.controls.reset_view()
        self.mock_navigator.reset_view.assert_called_once()

    def test_factory_version(self) -> None:
        '''
            Tests factory version retrieval.
        '''
        self.assertEqual(ToolbarNavigationControlsFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
