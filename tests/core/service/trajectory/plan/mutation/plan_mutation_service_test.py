# -*- coding: UTF-8 -*-

'''
Module
    plan_mutation_service_test.py
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
    Unit tests for PlanMutationService component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.plan.mutation.iplan_mutation_service import IPlanMutationService
from scarajectory.core.service.trajectory.plan.mutation.iplan_point_mutator import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service import PlanMutationService
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service_factory import PlanMutationServiceFactory
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher_factory import PlanObserverDispatcherFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager_factory import PlanSelectionManagerFactory
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanMutationService(TestCase):
    '''
        Test cases for PlanMutationService.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_add_point - Verifies appending waypoint.
                | test_insert_point - Verifies inserting waypoint at index.
                | test_update_point - Verifies updating waypoint.
                | test_remove_point - Verifies removing waypoint.
                | test_clear - Verifies clearing waypoints.
                | test_set_waypoints - Verifies replacing waypoints.
                | test_factory - Verifies factory creation and version.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test.

            :exceptions: None.
        '''
        self.store = WaypointStoreFactory.create()
        self.history = PlanHistoryFactory.create()
        self.selection = PlanSelectionManagerFactory.create()
        self.dispatcher = PlanObserverDispatcherFactory.create()
        self.service = PlanMutationService(
            store=self.store,
            history=self.history,
            selection=self.selection,
            dispatcher=self.dispatcher,
        )
        self.pt1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=50.0)
        self.pt2 = Waypoint(x=30.0, y=40.0, z=5.0, phi=0.0, speed=60.0)
        self.pt3 = Waypoint(x=50.0, y=60.0, z=10.0, phi=0.0, speed=70.0)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self.service, IPlanMutationService)
        self.assertIsInstance(self.service, IPlanPointMutator)
        self.assertIsInstance(self.service, IPlanBulkMutator)

    def test_add_point(self) -> None:
        '''
            Verifies appending waypoint.

            :exceptions: None.
        '''
        self.service.add_point(self.pt1)
        self.assertEqual(self.store.count, 1)
        self.assertEqual(self.selection.selected_index, 0)

        # History should have state saved
        prev = self.history.undo(list(self.store.waypoints))
        self.assertIsNotNone(prev)

        # Restore
        self.history.redo(list(self.store.waypoints))

        self.service.add_point(self.pt2)
        self.assertEqual(self.store.count, 2)
        self.assertEqual(self.selection.selected_index, 1)

    def test_insert_point(self) -> None:
        '''
            Verifies inserting waypoint at index.

            :exceptions: None.
        '''
        self.service.add_point(self.pt1)
        self.service.add_point(self.pt3)
        self.service.insert_point(1, self.pt2)

        self.assertEqual(self.store.count, 3)
        self.assertEqual(self.selection.selected_index, 1)
        self.assertEqual(self.store.waypoints[1].x, 30.0)

    def test_update_point(self) -> None:
        '''
            Verifies updating waypoint.

            :exceptions: None.
        '''
        self.service.add_point(self.pt1)
        updated_pt = Waypoint(x=15.0, y=25.0, z=0.0, phi=0.0, speed=55.0)
        success = self.service.update_point(0, updated_pt)
        self.assertTrue(success)
        self.assertEqual(self.store.waypoints[0].x, 15.0)

        invalid_success = self.service.update_point(99, updated_pt)
        self.assertFalse(invalid_success)

    def test_remove_point(self) -> None:
        '''
            Verifies removing waypoint.

            :exceptions: None.
        '''
        self.service.add_point(self.pt1)
        self.service.add_point(self.pt2)
        success = self.service.remove_point(0)
        self.assertTrue(success)
        self.assertEqual(self.store.count, 1)
        self.assertEqual(self.store.waypoints[0].x, 30.0)

        invalid_success = self.service.remove_point(99)
        self.assertFalse(invalid_success)

    def test_clear(self) -> None:
        '''
            Verifies clearing waypoints.

            :exceptions: None.
        '''
        self.service.add_point(self.pt1)
        self.service.add_point(self.pt2)
        self.service.clear()
        self.assertEqual(self.store.count, 0)
        self.assertEqual(self.selection.selected_index, -1)

        # Clear on empty does nothing and does not error
        self.service.clear()
        self.assertEqual(self.store.count, 0)

    def test_set_waypoints(self) -> None:
        '''
            Verifies replacing waypoints.

            :exceptions: None.
        '''
        self.service.set_waypoints((self.pt1, self.pt2, self.pt3))
        self.assertEqual(self.store.count, 3)
        self.assertEqual(self.selection.selected_index, 0)

        self.service.set_waypoints(())
        self.assertEqual(self.store.count, 0)
        self.assertEqual(self.selection.selected_index, -1)

    def test_factory(self) -> None:
        '''
            Verifies factory creation and version.

            :exceptions: None.
        '''
        inst = PlanMutationServiceFactory.create(
            store=self.store,
            history=self.history,
            selection=self.selection,
            dispatcher=self.dispatcher,
        )
        self.assertIsInstance(inst, PlanMutationService)
        self.assertIsInstance(inst, IPlanMutationService)
        self.assertIsInstance(PlanMutationServiceFactory.get_version(), str)


if __name__ == '__main__':
    main()
