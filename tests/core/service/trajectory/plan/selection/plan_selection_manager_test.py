# -*- coding: UTF-8 -*-

'''
Module
    plan_selection_manager_test.py
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
    Unit tests for PlanSelectionManager component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.selection.iplan_selection_manager import IPlanSelectionManager
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_navigator import IPlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_state import IPlanSelectionState
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager import PlanSelectionManager
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager_factory import PlanSelectionManagerFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_navigator import PlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.plan_selection_navigator_factory import PlanSelectionNavigatorFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_state import PlanSelectionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanSelectionManager(TestCase):
    '''
        Test cases for PlanSelectionManager.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_initial_and_reset - Tests initial state and reset.
                | test_set_selected_index - Tests setting selected index within bounds.
                | test_select_last - Tests selecting last element.
                | test_select_first_or_none - Tests selecting first element or none.
                | test_clamp_to_count - Tests clamping to valid upper count.
                | test_factory - Tests factory methods.
                | test_protocol_conformance - Verifies structural protocol conformance.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        self.selection: PlanSelectionManager = PlanSelectionManagerFactory.create()

    def test_initial_and_reset(self) -> None:
        '''
            Tests initial state and reset.

            :exceptions: None.
        '''
        self.assertEqual(self.selection.selected_index, -1)
        self.selection.select_index(3)
        self.assertEqual(self.selection.selected_index, 3)
        self.selection.reset()
        self.assertEqual(self.selection.selected_index, -1)

    def test_set_selected_index(self) -> None:
        '''
            Tests setting selected index within bounds.

            :exceptions: None.
        '''
        # Total count 3: valid indices are -1, 0, 1, 2
        self.assertTrue(self.selection.set_selected_index(1, total_count=3))
        self.assertEqual(self.selection.selected_index, 1)

        self.assertTrue(self.selection.set_selected_index(-1, total_count=3))
        self.assertEqual(self.selection.selected_index, -1)

        self.assertFalse(self.selection.set_selected_index(3, total_count=3))
        self.assertFalse(self.selection.set_selected_index(-2, total_count=3))

    def test_select_last(self) -> None:
        '''
            Tests selecting last element.

            :exceptions: None.
        '''
        self.selection.select_last(total_count=5)
        self.assertEqual(self.selection.selected_index, 4)

    def test_select_first_or_none(self) -> None:
        '''
            Tests selecting first element or none.

            :exceptions: None.
        '''
        self.selection.select_first_or_none(total_count=5)
        self.assertEqual(self.selection.selected_index, 0)

        self.selection.select_first_or_none(total_count=0)
        self.assertEqual(self.selection.selected_index, -1)

    def test_clamp_to_count(self) -> None:
        '''
            Tests clamping to valid upper count.

            :exceptions: None.
        '''
        self.selection.select_index(5)
        self.selection.clamp_to_count(total_count=3)
        self.assertEqual(self.selection.selected_index, 2)

        # Clamping when within count does not modify
        self.selection.clamp_to_count(total_count=10)
        self.assertEqual(self.selection.selected_index, 2)

    def test_factory(self) -> None:
        '''
            Tests factory methods.

            :exceptions: None.
        '''
        mgr = PlanSelectionManagerFactory.create_with_index(2)
        self.assertEqual(mgr.selected_index, 2)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self.selection, IPlanSelectionManager)
        self.assertIsInstance(self.selection, IPlanSelectionNavigator)
        self.assertIsInstance(self.selection, IPlanSelectionState)

    def test_fine_grained_components(self) -> None:
        '''
            Verifies isolated operation of fine-grained selection components.

            :exceptions: None.
        '''
        state: PlanSelectionState = PlanSelectionState(initial_index=-1)
        nav: PlanSelectionNavigator = PlanSelectionNavigatorFactory.create(state)

        self.assertIsInstance(state, IPlanSelectionState)
        self.assertIsInstance(nav, IPlanSelectionNavigator)
        self.assertEqual(PlanSelectionNavigatorFactory.get_version(), '1.0.4')

        self.assertEqual(state.selected_index, -1)
        self.assertTrue(state.set_selected_index(2, 5))
        self.assertEqual(state.selected_index, 2)
        self.assertFalse(state.set_selected_index(10, 5))

        state.clamp_to_count(2)
        self.assertEqual(state.selected_index, 1)

        nav.select_index(3)
        self.assertEqual(state.selected_index, 3)

        nav.select_last(8)
        self.assertEqual(state.selected_index, 7)

        nav.select_first_or_none(5)
        self.assertEqual(state.selected_index, 0)

        nav.select_first_or_none(0)
        self.assertEqual(state.selected_index, -1)

        nav.select_index(4)
        nav.reset()
        self.assertEqual(state.selected_index, -1)


if __name__ == '__main__':
    main()
