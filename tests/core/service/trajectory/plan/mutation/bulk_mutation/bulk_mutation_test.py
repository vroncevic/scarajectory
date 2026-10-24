# -*- coding: UTF-8 -*-

'''
Module
    bulk_mutation_test.py
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
    Unit tests for PlanBulkMutator implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.saver.dependencies import PlanHistorySaverDependencies
from scarajectory.core.service.trajectory.history.saver.factory import PlanHistorySaverFactory
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.bulk_mutation import PlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
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


class TestPlanBulkMutator(TestCase):
    '''
        Test cases for PlanBulkMutator.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_clear - Verifies clearing waypoints.
                | test_set_waypoints - Verifies replacing waypoints.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test.

            :exceptions: None.
        '''
        self.store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        history_saver = PlanHistorySaverFactory.create(
            PlanHistorySaverDependencies(
                stack=PlanHistoryStackFactory.create()
            )
        )
        dispatcher = ObserverFactory.create().plan_observer_dispatcher
        selection_provides = SelectionFactory.create(
            SelectionDependencies(
                waypoint_store=self.store,
                plan_observer_dispatcher=dispatcher,
                initial_index=-1,
            )
        )
        self.selection = selection_provides.plan_selection_state
        self.mutator = PlanBulkMutator(
            waypoint_store=self.store,
            plan_history_saver=history_saver,
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
        self.assertIsInstance(self.mutator, IPlanBulkMutator)

    def test_clear(self) -> None:
        '''
            Verifies clearing waypoints.

            :exceptions: None.
        '''
        self.store.add(self.pt1)
        self.store.add(self.pt2)
        self.mutator.clear()
        self.assertEqual(self.store.count, 0)
        self.assertEqual(self.selection.selected_index, -1)

        # Clear on empty does nothing and does not error
        self.mutator.clear()
        self.assertEqual(self.store.count, 0)

    def test_set_waypoints(self) -> None:
        '''
            Verifies replacing waypoints.

            :exceptions: None.
        '''
        self.mutator.set_waypoints((self.pt1, self.pt2, self.pt3))
        self.assertEqual(self.store.count, 3)
        self.assertEqual(self.selection.selected_index, 0)

        self.mutator.set_waypoints(())
        self.assertEqual(self.store.count, 0)
        self.assertEqual(self.selection.selected_index, -1)


if __name__ == '__main__':
    main()
