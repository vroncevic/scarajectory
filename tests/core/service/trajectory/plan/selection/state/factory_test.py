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
    Unit tests for SelectionStateFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.selection.state.factory import SelectionStateFactory
from scarajectory.core.service.trajectory.plan.selection.state.istate import IPlanSelectionState
from scarajectory.core.service.trajectory.plan.selection.state.state import PlanSelectionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSelectionStateFactory(TestCase):
    '''
        Test cases for SelectionStateFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory creation with default index.
                | test_create_custom - Verifies factory creation with custom index.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_default(self) -> None:
        '''
            Verifies factory creation with default index.

            :exceptions: None.
        '''
        state = SelectionStateFactory.create(-1)
        self.assertIsInstance(state, PlanSelectionState)
        self.assertIsInstance(state, IPlanSelectionState)
        self.assertEqual(state.selected_index, -1)

    def test_create_custom(self) -> None:
        '''
            Verifies factory creation with custom index.

            :exceptions: None.
        '''
        state = SelectionStateFactory.create(4)
        self.assertIsInstance(state, PlanSelectionState)
        self.assertIsInstance(state, IPlanSelectionState)
        self.assertEqual(state.selected_index, 4)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        version = SelectionStateFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
