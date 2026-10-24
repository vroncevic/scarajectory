# -*- coding: UTF-8 -*-

'''
Module
    history_test.py
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
    Unit tests for TrajectoryPlanHistory coordinator.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.dependencies import HistoryStackDependencies
from scarajectory.core.service.trajectory.history.factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory
from scarajectory.core.service.trajectory.plan.history.dependencies import HistoryDependencies
from scarajectory.core.service.trajectory.plan.history.factory import HistoryFactory
from scarajectory.core.service.trajectory.plan.history.history import TrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.observer.itrajectory_observer import ITrajectoryObserver
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


class MockObserver:
    '''Mock observer tracking notification events.'''

    def __init__(self) -> None:
        self.notified = False

    def on_trajectory_updated(self) -> None:
        '''Flags that change notification was received.'''
        self.notified = True

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.3'


class TestTrajectoryPlanHistory(TestCase):
    '''Test cases for TrajectoryPlanHistory.'''

    def setUp(self) -> None:
        '''Initializes collaborators and TrajectoryPlanHistory instance.'''
        store_provides = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        )
        self.store = store_provides.waypoint_store
        stack = PlanHistoryStackFactory.create()
        history_provides = PlanHistoryFactory.create(
            HistoryStackDependencies(stack=stack)
        )
        self.history_storage = history_provides.history
        self.history_saver = history_provides.saver
        self.dispatcher = PlanObserverDispatcher()
        self.selection = SelectionFactory.create(
            SelectionDependencies(
                waypoint_store=self.store,
                plan_observer_dispatcher=self.dispatcher,
                initial_index=-1,
            )
        ).plan_selection_state

        self.observer = MockObserver()
        self.assertIsInstance(self.observer, ITrajectoryObserver)
        self.dispatcher.add_observer(self.observer)

        self.history_coordinator = TrajectoryPlanHistory(
            waypoint_store=self.store,
            plan_history=self.history_storage,
            plan_selection_state=self.selection,
            plan_observer_dispatcher=self.dispatcher,
        )

    def test_protocol_conformance(self) -> None:
        '''Tests that TrajectoryPlanHistory conforms to ITrajectoryPlanHistory.'''
        self.assertIsInstance(self.history_coordinator, ITrajectoryPlanHistory)

    def test_undo_when_cannot_undo(self) -> None:
        '''Tests that undo returns False when history stack is empty.'''
        result = self.history_coordinator.undo()
        self.assertFalse(result)
        self.assertFalse(self.observer.notified)

    def test_redo_when_cannot_redo(self) -> None:
        '''Tests that redo returns False when redo stack is empty.'''
        result = self.history_coordinator.redo()
        self.assertFalse(result)
        self.assertFalse(self.observer.notified)

    def test_undo_and_redo_workflow(self) -> None:
        '''Tests full undo and redo cycle restoring store, clamping selection, and notifying.'''
        wp1 = TrajectoryWaypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=5.0, name='', command='')
        wp2 = TrajectoryWaypoint(x=30.0, y=40.0, z=0.0, phi=0.0, speed=10.0, name='', command='')

        # Initial state: 1 waypoint
        self.store.replace([wp1])
        self.history_saver.save_state([wp1])

        # State after addition: 2 waypoints
        self.store.replace([wp1, wp2])
        self.selection.set_selected_index(1, 2)

        self.observer.notified = False
        undo_success = self.history_coordinator.undo()
        self.assertTrue(undo_success)
        self.assertEqual(self.store.count, 1)
        self.assertEqual(self.store.waypoints[0].x, 10.0)
        self.assertEqual(self.selection.selected_index, 0)
        self.assertTrue(self.observer.notified)

        self.observer.notified = False
        redo_success = self.history_coordinator.redo()
        self.assertTrue(redo_success)
        self.assertEqual(self.store.count, 2)
        self.assertEqual(self.store.waypoints[1].x, 30.0)
        self.assertTrue(self.observer.notified)

    def test_factory_creation(self) -> None:
        '''Tests creation via HistoryFactory.'''
        deps = HistoryDependencies(
            waypoint_store=self.store,
            plan_history=self.history_storage,
            plan_selection_state=self.selection,
            plan_observer_dispatcher=self.dispatcher,
        )
        provides = HistoryFactory.create(deps)
        self.assertIsInstance(provides.trajectory_plan_history, TrajectoryPlanHistory)
        self.assertIsInstance(provides.trajectory_plan_history, ITrajectoryPlanHistory)


if __name__ == '__main__':
    main()
