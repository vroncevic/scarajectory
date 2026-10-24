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
    Unit tests for HistoryProvides output bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.service.trajectory.history.navigator.dependencies import PlanHistoryNavigatorDependencies
from scarajectory.core.service.trajectory.history.navigator.factory import PlanHistoryNavigatorFactory
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory
from scarajectory.core.service.trajectory.plan.history.history import TrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.history.provides import HistoryProvides
from scarajectory.core.service.trajectory.plan.observer.dispatcher import PlanObserverDispatcher
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


class TestHistoryProvides(TestCase):
    '''Test cases for HistoryProvides provision bundle.'''

    def setUp(self) -> None:
        '''Initializes mock services for testing.'''
        store_provides = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        )
        store = store_provides.waypoint_store
        dispatcher = PlanObserverDispatcher()
        self.history = TrajectoryPlanHistory(
            waypoint_store=store,
            plan_history=PlanHistoryNavigatorFactory.create(
                PlanHistoryNavigatorDependencies(
                    stack=PlanHistoryStackFactory.create()
                )
            ),
            plan_selection_state=SelectionFactory.create(
                SelectionDependencies(
                    waypoint_store=store,
                    plan_observer_dispatcher=dispatcher,
                    initial_index=-1,
                )
            ).plan_selection_state,
            plan_observer_dispatcher=dispatcher,
        )

    def test_instantiation_and_protocol_type(self) -> None:
        '''Tests provision bundle creation and protocol typing.'''
        provides = HistoryProvides(trajectory_plan_history=self.history)
        self.assertIs(provides.trajectory_plan_history, self.history)
        self.assertIsInstance(provides.trajectory_plan_history, ITrajectoryPlanHistory)

    def test_immutability(self) -> None:
        '''Tests that HistoryProvides is frozen.'''
        provides = HistoryProvides(trajectory_plan_history=self.history)
        with self.assertRaises(FrozenInstanceError):
            provides.trajectory_plan_history = self.history


if __name__ == '__main__':
    main()
