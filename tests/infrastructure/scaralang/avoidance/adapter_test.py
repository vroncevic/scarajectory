# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for DeadZoneAvoidanceAdapter component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.scaralang.avoidance.adapter import DeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneAvoidanceAdapterTest(TestCase):
    '''Test suite verifying DeadZoneAvoidanceAdapter functionality.'''

    def setUp(self) -> None:
        '''Initializes mock dependencies and test adapter instance.'''
        self.mock_validator: MagicMock = MagicMock(spec=IDeadZoneValidator)
        self.mock_planner: MagicMock = MagicMock(spec=IDeadZoneBypassPlanner)
        self.adapter: DeadZoneAvoidanceAdapter = DeadZoneAvoidanceAdapter(
            validator=self.mock_validator,
            planner=self.mock_planner,
        )

    def test_protocol_conformance(self) -> None:
        '''Verifies DeadZoneAvoidanceAdapter satisfies IDeadZoneAvoidanceAdapter.'''
        self.assertIsInstance(self.adapter, IDeadZoneAvoidanceAdapter)

    def test_crosses_dead_zone_true(self) -> None:
        '''Verifies crosses_dead_zone delegates to scaralang validator.'''
        self.mock_validator.is_segment_crossing_dead_zone.return_value = True
        p1: TrajectoryWaypoint = TrajectoryWaypoint(x=120.0, y=-50.0, z=20.0, speed=40.0, phi=0.0, name='', command='')
        p2: TrajectoryWaypoint = TrajectoryWaypoint(x=-120.0, y=50.0, z=20.0, speed=40.0, phi=0.0, name='', command='')

        result: bool = self.adapter.crosses_dead_zone(p1, p2)
        self.assertTrue(result)
        self.mock_validator.is_segment_crossing_dead_zone.assert_called_once_with(
            Point2D(x=120.0, y=-50.0),
            Point2D(x=-120.0, y=50.0),
        )

    def test_crosses_dead_zone_false(self) -> None:
        '''Verifies crosses_dead_zone returns false when segment is clear.'''
        self.mock_validator.is_segment_crossing_dead_zone.return_value = False
        p1: TrajectoryWaypoint = TrajectoryWaypoint(x=120.0, y=50.0, z=20.0, speed=40.0, phi=0.0, name='', command='')
        p2: TrajectoryWaypoint = TrajectoryWaypoint(x=130.0, y=60.0, z=20.0, speed=40.0, phi=0.0, name='', command='')

        result: bool = self.adapter.crosses_dead_zone(p1, p2)
        self.assertFalse(result)

    def test_is_point_in_dead_zone_true(self) -> None:
        '''Verifies is_point_in_dead_zone returns True when point inside dead zone.'''
        self.mock_validator.is_point_in_dead_zone.return_value = True
        pt: TrajectoryWaypoint = TrajectoryWaypoint(x=10.0, y=15.0, z=20.0, speed=40.0, phi=0.0, name='', command='')

        result: bool = self.adapter.is_point_in_dead_zone(pt)
        self.assertTrue(result)
        self.mock_validator.is_point_in_dead_zone.assert_called_once_with(10.0, 15.0)

    def test_is_point_in_dead_zone_false(self) -> None:
        '''Verifies is_point_in_dead_zone returns False when point outside dead zone.'''
        self.mock_validator.is_point_in_dead_zone.return_value = False
        pt: TrajectoryWaypoint = TrajectoryWaypoint(x=150.0, y=100.0, z=20.0, speed=40.0, phi=0.0, name='', command='')

        result: bool = self.adapter.is_point_in_dead_zone(pt)
        self.assertFalse(result)
        self.mock_validator.is_point_in_dead_zone.assert_called_once_with(150.0, 100.0)

    def test_plan_detour(self) -> None:
        '''Verifies plan_detour maps scaralang waypoints to scarajectory waypoints.'''
        raw_waypoints: list[Waypoint] = [
            Waypoint(
                x=95.0,
                y=10.0,
                z=20.0,
                phi=0.0,
                speed=40.0,
                name='',
                command='',
            ),
            Waypoint(
                x=90.0,
                y=30.0,
                z=20.0,
                phi=0.0,
                speed=40.0,
                name='',
                command='',
            ),
            Waypoint(
                x=-120.0,
                y=50.0,
                z=20.0,
                phi=0.0,
                speed=40.0,
                name='',
                command='',
            ),
        ]
        self.mock_planner.plan_bypass.return_value = raw_waypoints

        p1: TrajectoryWaypoint = TrajectoryWaypoint(x=120.0, y=-50.0, z=20.0, speed=40.0, phi=15.0, name='', command='')
        p2: TrajectoryWaypoint = TrajectoryWaypoint(x=-120.0, y=50.0, z=25.0, speed=50.0, phi=30.0, name='', command='')

        detour: list[TrajectoryWaypoint] = self.adapter.plan_detour(p1, p2)
        self.assertEqual(len(detour), 3)
        self.assertEqual(detour[0].x, 95.0)
        self.assertEqual(detour[0].phi, 30.0)
        self.assertEqual(detour[2].x, -120.0)
        self.assertEqual(detour[2].z, 20.0)

        self.mock_planner.plan_bypass.assert_called_once_with(
            Point2D(x=120.0, y=-50.0),
            Point2D(x=-120.0, y=50.0),
            z=25.0,
            speed=50.0,
        )

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid version string.'''
        self.assertEqual(self.adapter.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
