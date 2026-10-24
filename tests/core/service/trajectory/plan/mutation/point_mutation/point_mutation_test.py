# -*- coding: UTF-8 -*-

'''
Module
    point_mutation_test.py
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
    Unit tests for PlanPointMutator implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.dependencies import HistoryStackDependencies
from scarajectory.core.service.trajectory.history.factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.point_mutation import PlanPointMutator
from scarajectory.core.service.trajectory.plan.observer.factory import ObserverFactory
from scarajectory.core.service.trajectory.plan.selection.dependencies import SelectionDependencies
from scarajectory.core.service.trajectory.plan.selection.factory import SelectionFactory
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


class TestPlanPointMutator(TestCase):
    '''
        Test cases for PlanPointMutator.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_add_point - Verifies appending waypoint.
                | test_insert_point - Verifies inserting waypoint at index.
                | test_update_point - Verifies updating waypoint.
                | test_remove_point - Verifies removing waypoint.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test.

            :exceptions: None.
        '''
        store_provides = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        )
        self.store = store_provides.waypoint_store
        history_provides = PlanHistoryFactory.create(
            HistoryStackDependencies(stack=PlanHistoryStackFactory.create())
        )
        self.history = history_provides.history
        dispatcher = ObserverFactory.create().plan_observer_dispatcher
        selection_provides = SelectionFactory.create(
            SelectionDependencies(
                waypoint_store=self.store,
                plan_observer_dispatcher=dispatcher,
                initial_index=-1,
            )
        )
        self.selection = selection_provides.plan_selection_state
        self.mutator = PlanPointMutator(
            waypoint_store=self.store,
            plan_history_saver=history_provides.saver,
            plan_selection_navigator=selection_provides.plan_selection_navigator,
            plan_observer_dispatcher=dispatcher,
        )
        self.pt1 = TrajectoryWaypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=50.0, name='', command='')
        self.pt2 = TrajectoryWaypoint(x=30.0, y=40.0, z=5.0, phi=0.0, speed=60.0, name='', command='')
        self.pt3 = TrajectoryWaypoint(x=50.0, y=60.0, z=10.0, phi=0.0, speed=70.0, name='', command='')

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self.mutator, IPlanPointMutator)

    def test_add_point(self) -> None:
        '''
            Verifies appending waypoint.

            :exceptions: None.
        '''
        self.mutator.add_point(self.pt1)
        self.assertEqual(self.store.count, 1)
        self.assertEqual(self.selection.selected_index, 0)

        # History should have state saved
        self.assertTrue(self.history.can_undo())

        self.mutator.add_point(self.pt2)
        self.assertEqual(self.store.count, 2)
        self.assertEqual(self.selection.selected_index, 1)

    def test_insert_point(self) -> None:
        '''
            Verifies inserting waypoint at index.

            :exceptions: None.
        '''
        self.mutator.add_point(self.pt1)
        self.mutator.add_point(self.pt3)
        self.mutator.insert_point(1, self.pt2)

        self.assertEqual(self.store.count, 3)
        self.assertEqual(self.selection.selected_index, 1)
        self.assertEqual(self.store.waypoints[1].x, 30.0)

    def test_update_point(self) -> None:
        '''
            Verifies updating waypoint.

            :exceptions: None.
        '''
        self.mutator.add_point(self.pt1)
        updated_pt = TrajectoryWaypoint(x=15.0, y=25.0, z=0.0, phi=0.0, speed=55.0, name='', command='')
        success = self.mutator.update_point(0, updated_pt)
        self.assertTrue(success)
        self.assertEqual(self.store.waypoints[0].x, 15.0)

        invalid_success = self.mutator.update_point(99, updated_pt)
        self.assertFalse(invalid_success)

    def test_remove_point(self) -> None:
        '''
            Verifies removing waypoint.

            :exceptions: None.
        '''
        self.mutator.add_point(self.pt1)
        self.mutator.add_point(self.pt2)
        success = self.mutator.remove_point(0)
        self.assertTrue(success)
        self.assertEqual(self.store.count, 1)
        self.assertEqual(self.store.waypoints[0].x, 30.0)

        invalid_success = self.mutator.remove_point(99)
        self.assertFalse(invalid_success)


if __name__ == '__main__':
    main()
