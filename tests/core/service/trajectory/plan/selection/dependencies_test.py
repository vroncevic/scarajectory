# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for SelectionDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.observer.dispatcher import PlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.dependencies import SelectionDependencies
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


class TestSelectionDependencies(TestCase):
    '''
        Test cases for SelectionDependencies.

        It defines:

            :methods:
                | test_creation - Tests creating SelectionDependencies with explicit values.
                | test_custom_initial_index - Tests custom initial_index.
                | test_frozen - Verifies that the dataclass is immutable.
    '''

    def test_creation(self) -> None:
        '''
            Tests creating SelectionDependencies with explicit values.

            :exceptions: None.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        dispatcher = PlanObserverDispatcher()
        deps = SelectionDependencies(
            waypoint_store=store,
            plan_observer_dispatcher=dispatcher,
            initial_index=-1,
        )

        self.assertIs(deps.waypoint_store, store)
        self.assertIs(deps.plan_observer_dispatcher, dispatcher)
        self.assertEqual(deps.initial_index, -1)

    def test_custom_initial_index(self) -> None:
        '''
            Tests custom initial_index.

            :exceptions: None.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        dispatcher = PlanObserverDispatcher()
        deps = SelectionDependencies(
            waypoint_store=store,
            plan_observer_dispatcher=dispatcher,
            initial_index=2,
        )

        self.assertEqual(deps.initial_index, 2)

    def test_frozen(self) -> None:
        '''
            Verifies that the dataclass is immutable.

            :exceptions: None.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        dispatcher = PlanObserverDispatcher()
        deps = SelectionDependencies(
            waypoint_store=store,
            plan_observer_dispatcher=dispatcher,
            initial_index=-1,
        )

        with self.assertRaises(AttributeError):
            deps.waypoint_store = store  # type: ignore[misc]


if __name__ == '__main__':
    main()
