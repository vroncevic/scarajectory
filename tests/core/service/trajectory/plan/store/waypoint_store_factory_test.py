# -*- coding: UTF-8 -*-

'''
Module
    waypoint_store_factory_test.py
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
    Unit tests for WaypointStoreFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
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


class TestWaypointStoreFactory(TestCase):
    '''
        Test cases for WaypointStoreFactory.

        It defines:

            :methods:
                | test_create_empty - Tests creation of empty WaypointStore.
                | test_create_with_waypoints - Tests creation with initial waypoints.
                | test_get_version - Tests factory version query.
    '''

    def test_create_empty(self) -> None:
        '''
            Tests instantiation of empty WaypointStore.

            :exceptions: None.
        '''
        store: WaypointStore = WaypointStoreFactory.create()
        self.assertIsInstance(store, WaypointStore)
        self.assertEqual(store.count, 0)

    def test_create_with_waypoints(self) -> None:
        '''
            Tests instantiation of WaypointStore with initial waypoints.

            :exceptions: None.
        '''
        wp = Waypoint(x=15.0, y=25.0, z=5.0, speed=80.0)
        store: WaypointStore = WaypointStoreFactory.create_with_waypoints([wp])
        self.assertIsInstance(store, WaypointStore)
        self.assertEqual(store.count, 1)

    def test_get_version(self) -> None:
        '''
            Tests factory version string.

            :exceptions: None.
        '''
        version = WaypointStoreFactory.get_version()
        self.assertTrue(isinstance(version, str) and len(version) > 0)


if __name__ == '__main__':
    main()
