# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for StoreDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.dependencies import StoreDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStoreDependencies(TestCase):
    '''Test cases for StoreDependencies parameter bundle.'''

    def test_empty_waypoints_initialization(self) -> None:
        '''Verifies initialization with empty initial waypoints.'''
        dependencies = StoreDependencies(initial_waypoints=())
        self.assertEqual(dependencies.initial_waypoints, ())

    def test_custom_waypoints_initialization(self) -> None:
        '''Verifies initialization with custom waypoints sequence.'''
        points = (
            TrajectoryWaypoint(x=1.0, y=2.0, z=3.0, speed=10.0, phi=0.0, name='', command=''),
            TrajectoryWaypoint(x=4.0, y=5.0, z=6.0, speed=15.0, phi=1.0, name='', command=''),
        )
        dependencies = StoreDependencies(initial_waypoints=points)
        self.assertEqual(dependencies.initial_waypoints, points)

    def test_immutability(self) -> None:
        '''Tests that StoreDependencies is frozen.'''
        dependencies = StoreDependencies(initial_waypoints=())
        with self.assertRaises(FrozenInstanceError):
            dependencies.initial_waypoints = ()  # type: ignore[misc]


if __name__ == '__main__':
    main()
