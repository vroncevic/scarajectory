# -*- coding: UTF-8 -*-

'''
Module
    plan_observer_dispatcher_test.py
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
    Unit tests for PlanObserverDispatcher component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher import PlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher_factory import PlanObserverDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockObserverUpdated:
    '''
        Mock observer implementing on_trajectory_updated.
    '''

    called: bool

    def __init__(self) -> None:
        self.called = False

    def on_trajectory_updated(self) -> None:
        self.called = True

    def on_point_selected(self, index: int) -> None:
        pass


class MockObserverLegacy:
    '''
        Mock observer implementing legacy on_plan_changed.
    '''

    called: bool

    def __init__(self) -> None:
        self.called = False

    def on_plan_changed(self) -> None:
        self.called = True


class TestPlanObserverDispatcher(TestCase):
    '''
        Test cases for PlanObserverDispatcher.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_add_and_remove - Tests adding and removing observers.
                | test_notify_change_updated - Tests notification with on_trajectory_updated.
                | test_notify_change_legacy - Tests notification with legacy on_plan_changed.
                | test_factory - Tests factory creation.
                | test_protocol_conformance - Verifies structural protocol conformance.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        self.dispatcher: PlanObserverDispatcher = PlanObserverDispatcherFactory.create()

    def test_add_and_remove(self) -> None:
        '''
            Tests adding and removing observers.

            :exceptions: None.
        '''
        obs = MockObserverUpdated()
        self.assertEqual(self.dispatcher.count, 0)

        self.dispatcher.add_observer(obs)
        self.assertEqual(self.dispatcher.count, 1)

        # Duplicate addition ignored
        self.dispatcher.add_observer(obs)
        self.assertEqual(self.dispatcher.count, 1)

        self.dispatcher.remove_observer(obs)
        self.assertEqual(self.dispatcher.count, 0)

    def test_notify_change_updated(self) -> None:
        '''
            Tests notification with on_trajectory_updated.

            :exceptions: None.
        '''
        obs = MockObserverUpdated()
        self.dispatcher.add_observer(obs)
        self.assertFalse(obs.called)

        self.dispatcher.notify_change()
        self.assertTrue(obs.called)

    def test_notify_change_legacy(self) -> None:
        '''
            Tests notification with legacy on_plan_changed.

            :exceptions: None.
        '''
        obs = MockObserverLegacy()
        self.dispatcher.add_observer(obs)
        self.assertFalse(obs.called)

        self.dispatcher.notify_change()
        self.assertTrue(obs.called)

    def test_factory(self) -> None:
        '''
            Tests factory creation.

            :exceptions: None.
        '''
        disp = PlanObserverDispatcherFactory.create()
        self.assertIsInstance(disp, PlanObserverDispatcher)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self.dispatcher, IPlanObserverDispatcher)


if __name__ == '__main__':
    main()
