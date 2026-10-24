# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for SelectionProvides provision container.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.observer.dispatcher import PlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.coordinator.coordinator import PlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.navigator.inavigator import IPlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.navigator.navigator import PlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.provides import SelectionProvides
from scarajectory.core.service.trajectory.plan.selection.state.istate import IPlanSelectionState
from scarajectory.core.service.trajectory.plan.selection.state.state import PlanSelectionState
from scarajectory.core.service.trajectory.plan.store.dependencies import StoreDependencies
from scarajectory.core.service.trajectory.plan.store.factory import StoreFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSelectionProvides(TestCase):
    '''
        Test cases for SelectionProvides container.

        It defines:

            :methods:
                | test_attributes_and_types - Verifies attribute assignment and types.
                | test_frozen - Verifies that the dataclass is immutable.
    '''

    def test_attributes_and_types(self) -> None:
        '''
            Verifies attribute assignment and protocol types.

            :exceptions: None.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        state = PlanSelectionState(-1)
        navigator = PlanSelectionNavigator(state)
        dispatcher = PlanObserverDispatcher()
        coordinator = PlanSelectionCoordinator(
            waypoint_store=store,
            plan_selection_state=state,
            plan_observer_dispatcher=dispatcher,
        )

        provides = SelectionProvides(
            plan_selection_coordinator=coordinator,
            plan_selection_state=state,
            plan_selection_navigator=navigator,
        )

        self.assertIsInstance(
            provides.plan_selection_coordinator, IPlanSelectionCoordinator
        )
        self.assertIsInstance(
            provides.plan_selection_state, IPlanSelectionState
        )
        self.assertIsInstance(
            provides.plan_selection_navigator, IPlanSelectionNavigator
        )

    def test_frozen(self) -> None:
        '''
            Verifies that the dataclass is immutable.

            :exceptions: None.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        state = PlanSelectionState(-1)
        navigator = PlanSelectionNavigator(state)
        dispatcher = PlanObserverDispatcher()
        coordinator = PlanSelectionCoordinator(
            waypoint_store=store,
            plan_selection_state=state,
            plan_observer_dispatcher=dispatcher,
        )

        provides = SelectionProvides(
            plan_selection_coordinator=coordinator,
            plan_selection_state=state,
            plan_selection_navigator=navigator,
        )

        with self.assertRaises(AttributeError):
            provides.plan_selection_coordinator = coordinator  # type: ignore[misc]


if __name__ == '__main__':
    main()
