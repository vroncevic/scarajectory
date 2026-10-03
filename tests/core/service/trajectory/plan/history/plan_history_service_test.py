# -*- coding: UTF-8 -*-

'''
Module
    plan_history_service_test.py
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
    Unit tests for PlanHistoryService component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.core.service.trajectory.plan.history.plan_history_service import PlanHistoryService
from scarajectory.core.service.trajectory.plan.history.plan_history_service_factory import PlanHistoryServiceFactory
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service import PlanMutationService
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


class TestPlanHistoryService(TestCase):
    '''
        Test cases for PlanHistoryService.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_undo_and_redo - Verifies undo and redo execution flows.
                | test_undo_on_empty - Verifies undo when no history exists.
                | test_redo_on_empty - Verifies redo when no redo state exists.
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
        self.mutation = PlanMutationService(
            store=self.store,
            history=self.history,
            selection=self.selection,
            dispatcher=self.dispatcher,
        )
        self.history_service = PlanHistoryService(
            store=self.store,
            history=self.history,
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
        self.assertIsInstance(self.history_service, ITrajectoryHistory)

    def test_undo_on_empty(self) -> None:
        '''
            Verifies undo when no history exists.

            :exceptions: None.
        '''
        self.assertFalse(self.history_service.undo())

    def test_redo_on_empty(self) -> None:
        '''
            Verifies redo when no redo state exists.

            :exceptions: None.
        '''
        self.assertFalse(self.history_service.redo())

    def test_undo_and_redo(self) -> None:
        '''
            Verifies undo and redo execution flows.

            :exceptions: None.
        '''
        self.mutation.add_point(self.pt1)
        self.mutation.add_point(self.pt2)
        self.assertEqual(self.store.count, 2)

        # Undo second point
        success = self.history_service.undo()
        self.assertTrue(success)
        self.assertEqual(self.store.count, 1)
        self.assertEqual(self.store.waypoints[0].x, 10.0)

        # Undo first point
        success = self.history_service.undo()
        self.assertTrue(success)
        self.assertEqual(self.store.count, 0)

        # Redo first point
        success = self.history_service.redo()
        self.assertTrue(success)
        self.assertEqual(self.store.count, 1)

        # Redo second point
        success = self.history_service.redo()
        self.assertTrue(success)
        self.assertEqual(self.store.count, 2)

    def test_factory(self) -> None:
        '''
            Verifies factory creation and version.

            :exceptions: None.
        '''
        inst = PlanHistoryServiceFactory.create(
            store=self.store,
            history=self.history,
            selection=self.selection,
            dispatcher=self.dispatcher,
        )
        self.assertIsInstance(inst, PlanHistoryService)
        self.assertIsInstance(inst, ITrajectoryHistory)
        self.assertIsInstance(PlanHistoryServiceFactory.get_version(), str)


if __name__ == '__main__':
    main()
