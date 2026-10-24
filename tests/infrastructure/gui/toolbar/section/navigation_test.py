# -*- coding: UTF-8 -*-

'''
Module
    navigation_test.py
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
    Unit tests for NavigationSection component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.toolbar.section.navigation import NavigationSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NavigationSectionTestCase(TestCase):
    '''
        Test cases verifying viewport navigation and history controls.

        It defines:

            :methods:
                | setUpClass - Sets up root Tk fixture.
                | tearDownClass - Tears down root Tk fixture.
                | setUp - Sets up mock dependencies and section component.
                | tearDown - Tears down section widget.
                | test_initialization - Tests widget instantiation.
                | test_reset_view_delegation - Tests delegation to navigator reset_view.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up root Tk fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down root Tk fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up mock dependencies and section component.

            :exceptions: None.
        '''
        self.mock_navigator = MagicMock(spec=ICanvasViewNavigator)
        self.mock_history = MagicMock(spec=ITrajectoryPlanHistory)
        self.section = NavigationSection(
            self.root, self.mock_navigator, self.mock_history
        )

    def tearDown(self) -> None:
        '''
            Tears down section widget.

            :exceptions: None.
        '''
        self.section.destroy()

    def test_initialization(self) -> None:
        '''
            Tests widget instantiation.

            :exceptions: None.
        '''
        self.assertIsInstance(self.section, NavigationSection)

    def test_reset_view_delegation(self) -> None:
        '''
            Tests that reset_view delegates to navigator reset_view.

            :exceptions: None.
        '''
        self.section.reset_view()
        self.mock_navigator.reset_view.assert_called_once()


if __name__ == '__main__':
    main()
