# -*- coding: UTF-8 -*-

'''
Module
    istore_test.py
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
    Unit tests for IWaypointStore structural protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase
from unittest import main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyWaypointStore:
    '''Dummy class conforming structurally to IWaypointStore.'''

    @property
    def waypoints(self) -> Sequence[TrajectoryWaypoint]:
        '''Returns empty waypoint sequence.'''
        return ()

    @property
    def count(self) -> int:
        '''Returns zero waypoint count.'''
        return 0

    def add(self, point: TrajectoryWaypoint) -> None:
        '''Appends a waypoint.'''
        _ = point

    def insert(self, index: int, point: TrajectoryWaypoint) -> None:
        '''Inserts a waypoint at index.'''
        _ = (index, point)

    def update(self, index: int, point: TrajectoryWaypoint) -> bool:
        '''Updates a waypoint at index.'''
        _ = (index, point)
        return True

    def remove(self, index: int) -> bool:
        '''Removes a waypoint at index.'''
        _ = index
        return True

    def clear(self) -> None:
        '''Clears all stored waypoints.'''

    def replace(self, waypoints: Sequence[TrajectoryWaypoint]) -> None:
        '''Replaces waypoints with a new sequence.'''
        _ = waypoints


class IncompleteWaypointStore:
    '''Dummy class failing structural conformance to IWaypointStore.'''

    @property
    def count(self) -> int:
        '''Returns zero waypoint count.'''
        return 0

    def extra_method(self) -> bool:
        '''Auxiliary method to satisfy minimum method count.'''
        return False


class TestIWaypointStore(TestCase):
    '''Test cases verifying IWaypointStore protocol conformance.'''

    def test_protocol_isinstance_check(self) -> None:
        '''Verifies structural subtyping via isinstance.'''
        store = DummyWaypointStore()
        self.assertIsInstance(store, IWaypointStore)

    def test_protocol_failure_on_missing_methods(self) -> None:
        '''Verifies isinstance returns False when methods are missing.'''
        incomplete = IncompleteWaypointStore()
        self.assertNotIsInstance(incomplete, IWaypointStore)


if __name__ == '__main__':
    main()
