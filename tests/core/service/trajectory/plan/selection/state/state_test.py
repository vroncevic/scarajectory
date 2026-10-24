# -*- coding: UTF-8 -*-

'''
Module
    state_test.py
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
    Unit tests for PlanSelectionState component.
'''

from __future__ import annotations

from unittest import TestCase, main

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


class TestPlanSelectionState(TestCase):
    '''
        Test cases for PlanSelectionState.

        It defines:

            :methods:
                | test_initial_state - Tests initial selected index.
                | test_set_selected_index - Tests setting selected index within bounds.
                | test_clamp_to_count - Tests clamping index to valid count.
                | test_set_index_direct - Tests setting index directly.
                | test_protocol_conformance - Verifies structural protocol conformance.
    '''

    def test_initial_state(self) -> None:
        '''
            Tests initial selected index with default and custom index.

            :exceptions: None.
        '''
        state_default = PlanSelectionState(-1)
        self.assertEqual(state_default.selected_index, -1)

        state_custom = PlanSelectionState(3)
        self.assertEqual(state_custom.selected_index, 3)

    def test_set_selected_index(self) -> None:
        '''
            Tests setting selected index within bounds and out of bounds.

            :exceptions: None.
        '''
        state = PlanSelectionState(-1)
        self.assertTrue(state.set_selected_index(2, 5))
        self.assertEqual(state.selected_index, 2)

        # Same index returns False (no change)
        self.assertFalse(state.set_selected_index(2, 5))

        # Out of bounds returns False
        self.assertFalse(state.set_selected_index(5, 5))
        self.assertFalse(state.set_selected_index(-2, 5))
        self.assertEqual(state.selected_index, 2)

        # Deselect (-1) is valid
        self.assertTrue(state.set_selected_index(-1, 5))
        self.assertEqual(state.selected_index, -1)

    def test_clamp_to_count(self) -> None:
        '''
            Tests clamping index to valid count.

            :exceptions: None.
        '''
        state = PlanSelectionState(5)
        state.clamp_to_count(3)
        self.assertEqual(state.selected_index, 2)

        state.clamp_to_count(10)
        self.assertEqual(state.selected_index, 2)

    def test_set_index_direct(self) -> None:
        '''
            Tests setting index directly without bounds check.

            :exceptions: None.
        '''
        state = PlanSelectionState(-1)
        state.set_index_direct(7)
        self.assertEqual(state.selected_index, 7)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance with IPlanSelectionState.

            :exceptions: None.
        '''
        state = PlanSelectionState(-1)
        self.assertIsInstance(state, IPlanSelectionState)


if __name__ == '__main__':
    main()
