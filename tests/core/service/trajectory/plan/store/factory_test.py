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
    Unit tests for StoreFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.bulk_mutator.ibulk_mutator import IWaypointBulkMutator
from scarajectory.core.service.trajectory.plan.store.dependencies import StoreDependencies
from scarajectory.core.service.trajectory.plan.store.factory import StoreFactory
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.plan.store.mutator.imutator import IWaypointMutator
from scarajectory.core.service.trajectory.plan.store.provides import StoreProvides
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStoreFactory(TestCase):
    '''Test cases for StoreFactory.'''

    def test_create_default(self) -> None:
        '''Tests instantiation of empty store provides container.'''
        provides: StoreProvides = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        )
        self.assertIsInstance(provides, StoreProvides)
        self.assertIsInstance(provides.waypoint_store, IWaypointStore)
        self.assertIsInstance(provides.waypoint_query, IWaypointQuery)
        self.assertIsInstance(provides.waypoint_mutator, IWaypointMutator)
        self.assertIsInstance(provides.waypoint_bulk_mutator, IWaypointBulkMutator)
        self.assertEqual(provides.waypoint_store.count, 0)

    def test_create_with_dependencies(self) -> None:
        '''Tests instantiation of store with initial waypoints in dependencies.'''
        wp = TrajectoryWaypoint(x=15.0, y=25.0, z=5.0, speed=80.0, phi=0.0, name='', command='')
        dependencies = StoreDependencies(initial_waypoints=(wp,))
        provides: StoreProvides = StoreFactory.create(dependencies=dependencies)
        self.assertIsInstance(provides, StoreProvides)
        self.assertEqual(provides.waypoint_store.count, 1)
        self.assertEqual(provides.waypoint_query.count, 1)

    def test_get_version(self) -> None:
        '''Tests factory version string query.'''
        version = StoreFactory.get_version()
        self.assertTrue(isinstance(version, str) and len(version) > 0)


if __name__ == '__main__':
    main()
