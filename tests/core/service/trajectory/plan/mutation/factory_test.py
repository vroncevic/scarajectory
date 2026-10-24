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
    Unit tests for MutationFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.history.saver.dependencies import PlanHistorySaverDependencies
from scarajectory.core.service.trajectory.history.saver.factory import PlanHistorySaverFactory
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.dependencies import MutationDependencies
from scarajectory.core.service.trajectory.plan.mutation.factory import MutationFactory
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.mutation.provides import MutationProvides
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


class TestMutationFactory(TestCase):
    '''
        Test cases for MutationFactory.

        It defines:

            :methods:
                | test_create - Verifies factory assembly and returned provides bundle.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory assembly and returned provides bundle.

            :exceptions: None.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        history_saver = PlanHistorySaverFactory.create(
            PlanHistorySaverDependencies(
                stack=PlanHistoryStackFactory.create()
            )
        )
        dispatcher = ObserverFactory.create().plan_observer_dispatcher
        selection = SelectionFactory.create(
            SelectionDependencies(
                waypoint_store=store,
                plan_observer_dispatcher=dispatcher,
                initial_index=-1,
            )
        )

        deps = MutationDependencies(
            waypoint_store=store,
            plan_history_saver=history_saver,
            plan_selection_navigator=selection.plan_selection_navigator,
            plan_observer_dispatcher=dispatcher,
        )

        provides: MutationProvides = MutationFactory.create(deps)

        self.assertIsInstance(provides, MutationProvides)
        self.assertIsInstance(provides.plan_point_mutator, IPlanPointMutator)
        self.assertIsInstance(provides.plan_bulk_mutator, IPlanBulkMutator)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        version = MutationFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
