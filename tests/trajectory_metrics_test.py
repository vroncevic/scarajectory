# -*- coding: UTF-8 -*-

'''
Module
    trajectory_metrics_test.py
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
    Unit tests for TrajectoryMetrics domain service.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.discretization.waypoint_factory import WaypointFactory
from scarajectory.core.service.trajectory.metrics.trajectory_metrics import TrajectoryMetrics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryMetrics(TestCase):
    '''
        Test cases for TrajectoryMetrics distance, radial offset and duration calculations.

        It defines:

            :methods:
                | test_distance_between - Tests 3D Euclidean distance calculation between two points.
                | test_radial_distance - Tests 2D planar radial distance from base.
                | test_calculate_distance - Tests cumulative distance along waypoint path.
                | test_calculate_duration - Tests cumulative execution duration.
    '''

    def test_distance_between(self) -> None:
        '''
            Tests 3D distance calculation between two waypoints.
        '''
        p1 = WaypointFactory.create(x=0.0, y=0.0, z=0.0, speed=40.0)
        p2 = WaypointFactory.create(x=3.0, y=4.0, z=0.0, speed=40.0)
        self.assertAlmostEqual(TrajectoryMetrics.distance_between(p1, p2), 5.0)

        p3 = WaypointFactory.create(x=3.0, y=4.0, z=12.0, speed=40.0)
        self.assertAlmostEqual(TrajectoryMetrics.distance_between(p1, p3), 13.0)

    def test_radial_distance(self) -> None:
        '''
            Tests 2D radial distance from origin.
        '''
        p = WaypointFactory.create(x=30.0, y=40.0, z=0.0, speed=40.0)
        self.assertAlmostEqual(TrajectoryMetrics.radial_distance(p), 50.0)

    def test_calculate_distance(self) -> None:
        '''
            Tests cumulative distance along path of waypoints.
        '''
        self.assertEqual(TrajectoryMetrics.calculate_distance([]), 0.0)
        self.assertEqual(
            TrajectoryMetrics.calculate_distance(
                [WaypointFactory.create(x=10.0, y=10.0, z=0.0, speed=40.0)]
            ),
            0.0
        )

        pts = [
            WaypointFactory.create(x=0.0, y=0.0, z=0.0, speed=40.0),
            WaypointFactory.create(x=10.0, y=0.0, z=0.0, speed=40.0),
            WaypointFactory.create(x=10.0, y=10.0, z=0.0, speed=40.0),
        ]
        self.assertAlmostEqual(TrajectoryMetrics.calculate_distance(pts), 20.0)

    def test_calculate_duration(self) -> None:
        '''
            Tests duration estimation based on segment distances and feedrates.
        '''
        self.assertEqual(TrajectoryMetrics.calculate_duration([]), 0.0)
        pts = [
            WaypointFactory.create(x=0.0, y=0.0, z=0.0, speed=100.0),
            WaypointFactory.create(x=50.0, y=0.0, z=0.0, speed=50.0),  # dist 50 / speed 50 = 1.0s
            WaypointFactory.create(x=50.0, y=50.0, z=0.0, speed=25.0)  # dist 50 / speed 25 = 2.0s
        ]
        self.assertAlmostEqual(TrajectoryMetrics.calculate_duration(pts), 3.0)


if __name__ == '__main__':
    main()
