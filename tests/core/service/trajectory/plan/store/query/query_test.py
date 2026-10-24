# -*- coding: UTF-8 -*-

'''
Module
    query_test.py
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
    Unit tests for WaypointQuery component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.core.service.trajectory.plan.store.query.query import WaypointQuery

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypointQuery(TestCase):
    '''Test cases for WaypointQuery component.'''

    def setUp(self) -> None:
        self.raw_points = [
            TrajectoryWaypoint(x=0.0, y=0.0, z=0.0, speed=10.0, phi=0.0, name='', command=''),
            TrajectoryWaypoint(x=10.0, y=20.0, z=0.0, speed=10.0, phi=0.0, name='', command=''),
        ]
        self.query = WaypointQuery(self.raw_points)

    def test_protocol_conformance(self) -> None:
        '''Verifies structural protocol conformance.'''
        self.assertIsInstance(self.query, IWaypointQuery)

    def test_count(self) -> None:
        '''Verifies count property.'''
        self.assertEqual(self.query.count, 2)

    def test_waypoints_view(self) -> None:
        '''Verifies waypoints returns tuple view.'''
        points = self.query.waypoints
        self.assertEqual(len(points), 2)
        self.assertEqual(points[0].x, 0.0)
        self.assertEqual(points[1].x, 10.0)


if __name__ == '__main__':
    main()
