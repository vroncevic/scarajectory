# -*- coding: UTF-8 -*-

'''
Module
    waypoint_store_test.py
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
    Unit tests for WaypointStore component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.store.iwaypoint_bulk_mutator import IWaypointBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_mutator import IWaypointMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_query import IWaypointQuery
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.core.service.trajectory.plan.store.waypoint_bulk_mutator import WaypointBulkMutator
from scarajectory.core.service.trajectory.plan.store.waypoint_mutator import WaypointMutator
from scarajectory.core.service.trajectory.plan.store.waypoint_query import WaypointQuery
from scarajectory.core.service.trajectory.plan.store.waypoint_store import WaypointStore
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypointStore(TestCase):
    '''
        Test cases for WaypointStore collection storage.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_add_and_count - Tests adding points and count.
                | test_insert - Tests inserting points at specific index.
                | test_update - Tests modifying points at valid and invalid indices.
                | test_remove - Tests removing points at valid and invalid indices.
                | test_clear - Tests clearing all points.
                | test_replace - Tests replacing points with new sequence.
                | test_factory - Tests factory creation methods.
                | test_protocol_conformance - Verifies structural protocol conformance.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        self.store: WaypointStore = WaypointStoreFactory.create()

    def test_add_and_count(self) -> None:
        '''
            Tests adding points and checking count.

            :exceptions: None.
        '''
        self.assertEqual(self.store.count, 0)
        self.assertEqual(len(self.store.waypoints), 0)

        p1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.store.add(p1)

        self.assertEqual(self.store.count, 1)
        self.assertEqual(self.store.waypoints[0].x, 10.0)

    def test_insert(self) -> None:
        '''
            Tests inserting points at specific index.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        p2 = Waypoint(x=30.0, y=40.0, z=0.0, phi=0.0, speed=10.0)
        self.store.add(p1)
        self.store.insert(0, p2)

        self.assertEqual(self.store.count, 2)
        self.assertEqual(self.store.waypoints[0].x, 30.0)
        self.assertEqual(self.store.waypoints[1].x, 10.0)

    def test_update(self) -> None:
        '''
            Tests modifying points at valid and invalid indices.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.store.add(p1)

        p_mod = Waypoint(x=55.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.assertTrue(self.store.update(0, p_mod))
        self.assertEqual(self.store.waypoints[0].x, 55.0)

        self.assertFalse(self.store.update(5, p_mod))
        self.assertFalse(self.store.update(-1, p_mod))

    def test_remove(self) -> None:
        '''
            Tests removing points at valid and invalid indices.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.store.add(p1)

        self.assertFalse(self.store.remove(5))
        self.assertFalse(self.store.remove(-1))
        self.assertTrue(self.store.remove(0))
        self.assertEqual(self.store.count, 0)

    def test_clear(self) -> None:
        '''
            Tests clearing all points.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.store.add(p1)
        self.store.clear()
        self.assertEqual(self.store.count, 0)

    def test_replace(self) -> None:
        '''
            Tests replacing points with new sequence.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        p2 = Waypoint(x=20.0, y=30.0, z=0.0, phi=0.0, speed=10.0)
        self.store.replace([p1, p2])
        self.assertEqual(self.store.count, 2)

    def test_factory(self) -> None:
        '''
            Tests factory creation methods.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        loaded = WaypointStoreFactory.create_with_waypoints([p1])
        self.assertEqual(loaded.count, 1)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self.store, IWaypointStore)
        self.assertIsInstance(self.store, IWaypointQuery)
        self.assertIsInstance(self.store, IWaypointMutator)
        self.assertIsInstance(self.store, IWaypointBulkMutator)

    def test_fine_grained_components(self) -> None:
        '''
            Verifies isolated operation of fine-grained store components.

            :exceptions: None.
        '''
        raw_list: list[Waypoint] = []
        query: WaypointQuery = WaypointQuery(raw_list)
        mutator: WaypointMutator = WaypointMutator(raw_list)
        bulk: WaypointBulkMutator = WaypointBulkMutator(raw_list)

        self.assertIsInstance(query, IWaypointQuery)
        self.assertIsInstance(mutator, IWaypointMutator)
        self.assertIsInstance(bulk, IWaypointBulkMutator)

        p1 = Waypoint(x=5.0, y=5.0, z=0.0, phi=0.0, speed=10.0)
        mutator.add(p1)
        self.assertEqual(query.count, 1)
        self.assertEqual(query.waypoints[0].x, 5.0)

        p2 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=15.0)
        mutator.insert(0, p2)
        self.assertEqual(query.count, 2)
        self.assertEqual(query.waypoints[0].x, 10.0)

        p3 = Waypoint(x=15.0, y=15.0, z=0.0, phi=0.0, speed=20.0)
        self.assertTrue(mutator.update(1, p3))
        self.assertEqual(query.waypoints[1].x, 15.0)

        self.assertTrue(mutator.remove(0))
        self.assertEqual(query.count, 1)

        bulk.clear()
        self.assertEqual(query.count, 0)

        bulk.replace([p1, p2, p3])
        self.assertEqual(query.count, 3)


if __name__ == '__main__':
    main()
