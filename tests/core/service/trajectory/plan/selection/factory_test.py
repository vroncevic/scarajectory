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
    Unit tests for SelectionFactory top-level factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.observer.dispatcher import PlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.dependencies import SelectionDependencies
from scarajectory.core.service.trajectory.plan.selection.factory import SelectionFactory
from scarajectory.core.service.trajectory.plan.selection.navigator.inavigator import IPlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.provides import SelectionProvides
from scarajectory.core.service.trajectory.plan.selection.state.istate import IPlanSelectionState
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


class TestSelectionFactory(TestCase):
    '''
        Test cases for SelectionFactory.

        It defines:

            :methods:
                | test_create - Verifies top-level selection subsystem assembly.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies top-level selection subsystem assembly.

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

        provides: SelectionProvides = SelectionFactory.create(deps)

        self.assertIsInstance(provides, SelectionProvides)
        self.assertIsInstance(
            provides.plan_selection_coordinator, IPlanSelectionCoordinator
        )
        self.assertIsInstance(
            provides.plan_selection_state, IPlanSelectionState
        )
        self.assertIsInstance(
            provides.plan_selection_navigator, IPlanSelectionNavigator
        )

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        version = SelectionFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
