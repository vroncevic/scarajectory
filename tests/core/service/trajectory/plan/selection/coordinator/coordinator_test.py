# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.observer.factory import ObserverFactory
from scarajectory.core.service.trajectory.plan.observer.itrajectory_observer import ITrajectoryObserver
from scarajectory.core.service.trajectory.plan.selection.coordinator.coordinator import PlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.state.state import PlanSelectionState
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


class TestPlanSelectionCoordinator(TestCase):
    '''
        Test cases for PlanSelectionCoordinator.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_selection_lifecycle - Verifies selection queries and updates.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test.

            :exceptions: None.
        '''
        self.store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        self.store.add(TrajectoryWaypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=50.0, name='', command=''))
        self.store.add(TrajectoryWaypoint(x=30.0, y=40.0, z=5.0, phi=0.0, speed=60.0, name='', command=''))

        self.state = PlanSelectionState(-1)

        observer_provides = ObserverFactory.create()
        self.dispatcher = observer_provides.plan_observer_dispatcher
        self.observer = MockObserver()
        self.assertIsInstance(self.observer, ITrajectoryObserver)
        self.dispatcher.add_observer(self.observer)

        self.coordinator = PlanSelectionCoordinator(
            waypoint_store=self.store,
            plan_selection_state=self.state,
            plan_observer_dispatcher=self.dispatcher,
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance with IPlanSelectionCoordinator.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, IPlanSelectionCoordinator)

    def test_selection_lifecycle(self) -> None:
        '''
            Verifies selection queries and updates with notification dispatch.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.selected_index, -1)
        self.assertFalse(self.observer.notified)

        self.coordinator.set_selected_index(1)
        self.assertEqual(self.coordinator.selected_index, 1)
        self.assertTrue(self.observer.notified)

        # Reset flag
        self.observer.notified = False
        # Same index should not re-notify
        self.coordinator.set_selected_index(1)
        self.assertFalse(self.observer.notified)

        # Out of bounds should not update or notify
        self.coordinator.set_selected_index(99)
        self.assertEqual(self.coordinator.selected_index, 1)
        self.assertFalse(self.observer.notified)

        # Deselect (-1) should notify
        self.coordinator.set_selected_index(-1)
        self.assertEqual(self.coordinator.selected_index, -1)
        self.assertTrue(self.observer.notified)


if __name__ == '__main__':
    main()
