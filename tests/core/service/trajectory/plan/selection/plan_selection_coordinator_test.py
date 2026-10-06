# -*- coding: UTF-8 -*-

'''
Module
    plan_selection_coordinator_test.py
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
    Unit tests for PlanSelectionCoordinator component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher_factory import PlanObserverDispatcherFactory
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.plan_selection_coordinator import PlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.plan_selection_coordinator_factory import PlanSelectionCoordinatorFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager_factory import PlanSelectionManagerFactory
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanSelectionCoordinator(TestCase):
    '''
        Test cases for PlanSelectionCoordinator.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_selection_lifecycle - Verifies selection queries and updates.
                | test_factory - Verifies factory creation and version.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test.

            :exceptions: None.
        '''
        self.store = WaypointStoreFactory.create()
        self.selection = PlanSelectionManagerFactory.create()
        self.dispatcher = PlanObserverDispatcherFactory.create()
        self.coordinator = PlanSelectionCoordinator(
            store=self.store,
            selection=self.selection,
            dispatcher=self.dispatcher,
        )
        self.pt1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=50.0)
        self.pt2 = Waypoint(x=30.0, y=40.0, z=5.0, phi=0.0, speed=60.0)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, IPlanSelectionCoordinator)

    def test_selection_lifecycle(self) -> None:
        '''
            Verifies selection queries and updates.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.selected_index, -1)

        self.store.add(self.pt1)
        self.store.add(self.pt2)

        self.coordinator.set_selected_index(1)
        self.assertEqual(self.coordinator.selected_index, 1)

        self.coordinator.set_selected_index(0)
        self.assertEqual(self.coordinator.selected_index, 0)

        # Invalid index out of bounds is ignored
        self.coordinator.set_selected_index(99)
        self.assertEqual(self.coordinator.selected_index, 0)

        # Deselect with -1
        self.coordinator.set_selected_index(-1)
        self.assertEqual(self.coordinator.selected_index, -1)

    def test_factory(self) -> None:
        '''
            Verifies factory creation and version.

            :exceptions: None.
        '''
        inst = PlanSelectionCoordinatorFactory.create(
            store=self.store,
            selection=self.selection,
            dispatcher=self.dispatcher,
        )
        self.assertIsInstance(inst, PlanSelectionCoordinator)
        self.assertIsInstance(inst, IPlanSelectionCoordinator)
        self.assertIsInstance(PlanSelectionCoordinatorFactory.get_version(), str)


if __name__ == '__main__':
    main()
