# -*- coding: UTF-8 -*-

'''
Module
    canvas_shape_handler_test.py
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
    Unit tests for CanvasShapeHandler geometric shape discretization.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.ishape_discretizer import (
    IShapeDiscretizer,
)
from scaralang.core.service.trajectory.discretization.shape_discretizer_factory import (
    ShapeDiscretizerFactory,
)
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.canvas.handler.canvas_shape_handler import (
    CanvasShapeHandler,
)
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubTrajectoryPlan:
    '''
        Structural stub for trajectory mutable plan.
    '''

    def __init__(self) -> None:
        self.waypoints: list[Waypoint] = []

    def add_point(self, point: Waypoint) -> None:
        '''Adds waypoint to plan.'''
        self.waypoints.append(point)

    def set_waypoints(self, waypoints: list[Waypoint]) -> None:
        '''Sets all waypoints on plan.'''
        self.waypoints = list(waypoints)


class CanvasShapeHandlerTestCase(TestCase):
    '''
        Tests for CanvasShapeHandler CAD geometry discretization.

        It defines:

            :methods:
                | setUp - Initializes plan, discretizer, and settings fixture.
                | test_create_and_commit_point - Tests waypoint creation and single point commit.
                | test_commit_line - Tests straight line discretization and length thresholding.
                | test_commit_circle - Tests circular trajectory discretization and radius check.
                | test_commit_rectangle - Tests rectangle perimeter discretization and dimensions.
                | test_commit_shape_dispatch - Tests shape commitment dispatching for all modes.
    '''

    plan: StubTrajectoryPlan
    discretizer: IShapeDiscretizer
    settings: CanvasSettings
    handler: CanvasShapeHandler

    def setUp(self) -> None:
        '''
            Initializes plan, discretizer, and settings fixture.

            :exceptions: None.
        '''
        self.plan = StubTrajectoryPlan()
        self.discretizer = ShapeDiscretizerFactory.create()
        self.settings = CanvasSettings(default_z=15.0, default_speed=35.0)
        self.handler = CanvasShapeHandler(
            plan=self.plan,  # type: ignore[arg-type]
            discretizer=self.discretizer,
        )

    def test_create_and_commit_point(self) -> None:
        '''
            Tests waypoint creation and single point commit.

            :exceptions: None.
        '''
        waypoint = self.handler.create_waypoint_at(12.0, 34.0, self.settings)
        self.assertEqual(waypoint.x, 12.0)
        self.assertEqual(waypoint.y, 34.0)
        self.assertEqual(waypoint.z, 15.0)
        self.assertEqual(waypoint.speed, 35.0)

        self.handler.commit_point(50.0, 60.0, self.settings)
        self.assertEqual(len(self.plan.waypoints), 1)
        self.assertEqual(self.plan.waypoints[0].x, 50.0)
        self.assertEqual(self.plan.waypoints[0].y, 60.0)

    def test_commit_line(self) -> None:
        '''
            Tests straight line discretization and length thresholding.

            :exceptions: None.
        '''
        # Below length threshold: hypot <= 1.0
        self.handler.commit_line(0.0, 0.0, 0.4, 0.4, self.settings)
        self.assertEqual(len(self.plan.waypoints), 0)

        # Above length threshold
        self.handler.commit_line(0.0, 0.0, 20.0, 20.0, self.settings)
        self.assertGreater(len(self.plan.waypoints), 0)

    def test_commit_circle(self) -> None:
        '''
            Tests circular trajectory discretization and radius check.

            :exceptions: None.
        '''
        # Below minimum radius (radius < 5.0)
        self.handler.commit_circle(0.0, 0.0, 2.0, 2.0, self.settings)
        self.assertEqual(len(self.plan.waypoints), 0)

        # Above minimum radius (radius >= 5.0)
        self.handler.commit_circle(0.0, 0.0, 10.0, 0.0, self.settings)
        self.assertGreater(len(self.plan.waypoints), 0)

    def test_commit_rectangle(self) -> None:
        '''
            Tests rectangle perimeter discretization and dimensions.

            :exceptions: None.
        '''
        # Dimensions too small (dx <= 2.0 or dy <= 2.0)
        self.handler.commit_rectangle(0.0, 0.0, 1.0, 1.0, self.settings)
        self.assertEqual(len(self.plan.waypoints), 0)

        # Sufficient dimensions
        self.handler.commit_rectangle(0.0, 0.0, 20.0, 30.0, self.settings)
        self.assertGreater(len(self.plan.waypoints), 0)

    def test_commit_shape_dispatch(self) -> None:
        '''
            Tests shape commitment dispatching for all modes.

            :exceptions: None.
        '''
        # Point mode
        self.handler.commit_shape(
            CanvasToolMode.POINT, 0.0, 0.0, 10.0, 10.0, self.settings
        )
        self.assertEqual(len(self.plan.waypoints), 1)

        # Line mode
        self.handler.commit_shape(
            CanvasToolMode.LINE, 0.0, 0.0, 30.0, 30.0, self.settings
        )
        count_after_line = len(self.plan.waypoints)
        self.assertGreater(count_after_line, 1)

        # Circle mode
        self.handler.commit_shape(
            CanvasToolMode.CIRCLE, 0.0, 0.0, 20.0, 0.0, self.settings
        )
        count_after_circle = len(self.plan.waypoints)
        self.assertGreater(count_after_circle, count_after_line)

        # Rectangle mode
        self.handler.commit_shape(
            CanvasToolMode.RECTANGLE, 0.0, 0.0, 40.0, 40.0, self.settings
        )
        count_after_rect = len(self.plan.waypoints)
        self.assertGreater(count_after_rect, count_after_circle)

        # Unsupported / other mode (e.g. SELECT)
        self.handler.commit_shape(
            CanvasToolMode.SELECT, 0.0, 0.0, 50.0, 50.0, self.settings
        )
        self.assertEqual(len(self.plan.waypoints), count_after_rect)


if __name__ == '__main__':
    main()
