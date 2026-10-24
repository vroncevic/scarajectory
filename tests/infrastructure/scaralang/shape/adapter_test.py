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
    Unit tests for ShapePlannerAdapter component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.circle import CircleGeometry
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.shape.iplanner import IAvoidanceShapePlanner
from scaralang.core.service.trajectory.discretization.circle.icircle import ICircleDiscretizer

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.scaralang.shape.adapter import ShapePlannerAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ShapePlannerAdapterTest(TestCase):
    '''Test suite verifying ShapePlannerAdapter functionality.'''

    def setUp(self) -> None:
        '''Initializes mock dependencies and test adapter instance.'''
        self.mock_planner: MagicMock = MagicMock(spec=IAvoidanceShapePlanner)
        self.mock_discretizer: MagicMock = MagicMock(spec=ICircleDiscretizer)
        self.adapter: ShapePlannerAdapter = ShapePlannerAdapter(
            planner=self.mock_planner,
            discretizer=self.mock_discretizer,
        )

    def test_protocol_conformance(self) -> None:
        '''Verifies ShapePlannerAdapter satisfies IShapePlannerAdapter.'''
        self.assertIsInstance(self.adapter, IShapePlannerAdapter)

    def test_plan_contour(self) -> None:
        '''Verifies plan_contour delegates to scaralang planner and maps waypoints.'''
        raw_waypoints: list[Waypoint] = [
            Waypoint(
                x=100.0,
                y=50.0,
                z=10.0,
                phi=0.0,
                speed=25.0,
                name='',
                command='',
            ),
            Waypoint(
                x=100.0,
                y=100.0,
                z=10.0,
                phi=0.0,
                speed=25.0,
                name='',
                command='',
            ),
        ]
        self.mock_planner.plan_contour.return_value = raw_waypoints
        pts: list[Point2D] = [
            Point2D(x=100.0, y=50.0),
            Point2D(x=100.0, y=100.0),
        ]

        result: list[TrajectoryWaypoint] = self.adapter.plan_contour(
            pts,
            z=10.0,
            speed=25.0,
            closed=True,
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].x, 100.0)
        self.assertEqual(result[0].y, 50.0)
        self.assertEqual(result[0].z, 10.0)
        self.assertEqual(result[0].speed, 25.0)
        self.mock_planner.plan_contour.assert_called_once_with(
            pts,
            z=10.0,
            speed=25.0,
            closed=True,
        )

    def test_plan_circle(self) -> None:
        '''Verifies plan_circle discretizes circle and routes through plan_contour.'''
        circle_raw: list[Waypoint] = [
            Waypoint(
                x=100.0,
                y=0.0,
                z=5.0,
                phi=0.0,
                speed=20.0,
                name='',
                command='',
            ),
            Waypoint(
                x=0.0,
                y=100.0,
                z=5.0,
                phi=0.0,
                speed=20.0,
                name='',
                command='',
            ),
        ]
        self.mock_discretizer.discretize.return_value = circle_raw
        self.mock_planner.plan_contour.return_value = circle_raw

        geom: CircleGeometry = CircleGeometry(
            center=Point2D(x=0.0, y=0.0),
            radius=100.0,
            steps=8,
            z=5.0,
            speed=20.0,
        )
        result: list[TrajectoryWaypoint] = self.adapter.plan_circle(geom)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].x, 100.0)
        self.mock_discretizer.discretize.assert_called_once()
        self.mock_planner.plan_contour.assert_called_once()

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        self.assertEqual(self.adapter.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
