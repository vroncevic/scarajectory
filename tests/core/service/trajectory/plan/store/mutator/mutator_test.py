# -*- coding: UTF-8 -*-

'''
Module
    mutator_test.py
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
    Unit tests for WaypointMutator component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.mutator.imutator import IWaypointMutator
from scarajectory.core.service.trajectory.plan.store.mutator.mutator import WaypointMutator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypointMutator(TestCase):
    '''Test cases for WaypointMutator component.'''

    def setUp(self) -> None:
        self.raw_points: list[TrajectoryWaypoint] = []
        self.mutator = WaypointMutator(self.raw_points)

    def test_protocol_conformance(self) -> None:
        '''Verifies structural protocol conformance.'''
        self.assertIsInstance(self.mutator, IWaypointMutator)

    def test_add_and_insert(self) -> None:
        '''Verifies appending and inserting waypoints.'''
        p1 = TrajectoryWaypoint(x=1.0, y=2.0, z=3.0, speed=10.0, phi=4.0, name='', command='')
        p2 = TrajectoryWaypoint(x=5.0, y=6.0, z=7.0, speed=10.0, phi=8.0, name='', command='')
        self.mutator.add(p1)
        self.assertEqual(len(self.raw_points), 1)
        self.mutator.insert(0, p2)
        self.assertEqual(self.raw_points[0], p2)
        self.assertEqual(self.raw_points[1], p1)

    def test_update_and_remove(self) -> None:
        '''Verifies updating and removing waypoints.'''
        p1 = TrajectoryWaypoint(x=1.0, y=2.0, z=3.0, speed=10.0, phi=4.0, name='', command='')
        p2 = TrajectoryWaypoint(x=5.0, y=6.0, z=7.0, speed=10.0, phi=8.0, name='', command='')
        self.mutator.add(p1)
        self.assertTrue(self.mutator.update(0, p2))
        self.assertEqual(self.raw_points[0], p2)
        self.assertFalse(self.mutator.update(99, p1))
        self.assertTrue(self.mutator.remove(0))
        self.assertEqual(len(self.raw_points), 0)
        self.assertFalse(self.mutator.remove(0))


if __name__ == '__main__':
    main()
