# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for SelectionNavigatorFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.selection.navigator.factory import SelectionNavigatorFactory
from scarajectory.core.service.trajectory.plan.selection.navigator.inavigator import IPlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.navigator.navigator import PlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.state.state import PlanSelectionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSelectionNavigatorFactory(TestCase):
    '''
        Test cases for SelectionNavigatorFactory.

        It defines:

            :methods:
                | test_create - Verifies factory creation.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creation.

            :exceptions: None.
        '''
        state = PlanSelectionState(-1)
        navigator = SelectionNavigatorFactory.create(state)
        self.assertIsInstance(navigator, PlanSelectionNavigator)
        self.assertIsInstance(navigator, IPlanSelectionNavigator)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        version = SelectionNavigatorFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
