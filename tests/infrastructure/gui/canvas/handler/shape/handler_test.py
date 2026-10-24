# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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
    Unit tests for CanvasShapeHandler geometric shape creation and plan
    dispatching.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.canvas.handler.coordinator.icoordinator import IShapePlanCoordinator
from scarajectory.infrastructure.gui.canvas.handler.shape.handler import CanvasShapeHandler
from scarajectory.infrastructure.gui.canvas.handler.shape.factory import CanvasShapeHandlerFactory
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasShapeHandler(TestCase):
    '''
        Tests for CanvasShapeHandler CAD geometry discretization.

        It defines:

            :methods:
                | setUp - Initializes mock coordinator and handler fixture.
                | test_create_waypoint_at - Tests waypoint creation at coordinates.
                | test_create_relocated_waypoint - Tests relocated waypoint creation.
                | test_commit_point - Tests delegation to coordinator commit_point.
                | test_commit_shape_dispatch - Tests shape commitment dispatching for all modes.
    '''

    coordinator: MagicMock
    settings: CanvasSettings
    handler: CanvasShapeHandler

    def setUp(self) -> None:
        '''
            Initializes mock coordinator and handler fixture.

            :exceptions: None.
        '''
        self.coordinator = MagicMock(spec=IShapePlanCoordinator)
        self.settings = CanvasSettings(default_z=15.0, default_speed=35.0)
        self.handler = CanvasShapeHandlerFactory.create(
            coordinator=self.coordinator
        )

    def test_create_waypoint_at(self) -> None:
        '''
            Tests waypoint creation at world coordinates.

            :exceptions: None.
        '''
        waypoint: TrajectoryWaypoint = self.handler.create_waypoint_at(
            12.0, 34.0, self.settings
        )
        self.assertEqual(waypoint.x, 12.0)
        self.assertEqual(waypoint.y, 34.0)
        self.assertEqual(waypoint.z, 15.0)
        self.assertEqual(waypoint.speed, 35.0)
        self.assertEqual(waypoint.phi, 0.0)

    def test_create_relocated_waypoint(self) -> None:
        '''
            Tests relocated waypoint creation preserving other properties.

            :exceptions: None.
        '''
        current: TrajectoryWaypoint = TrajectoryWaypoint(
            x=10.0,
            y=20.0,
            z=25.0,
            speed=50.0,
            phi=15.0,
            name='P1',
            command='G1',
        )
        updated: TrajectoryWaypoint = self.handler.create_relocated_waypoint(
            current, 30.0, 40.0
        )
        self.assertEqual(updated.x, 30.0)
        self.assertEqual(updated.y, 40.0)
        self.assertEqual(updated.z, 25.0)
        self.assertEqual(updated.speed, 50.0)
        self.assertEqual(updated.phi, 15.0)
        self.assertEqual(updated.name, 'P1')
        self.assertEqual(updated.command, 'G1')

    def test_commit_point(self) -> None:
        '''
            Tests delegation of commit_point to coordinator.

            :exceptions: None.
        '''
        self.handler.commit_point(50.0, 60.0, self.settings)
        self.coordinator.commit_point.assert_called_once_with(
            50.0, 60.0, self.settings
        )

    def test_commit_shape_dispatch(self) -> None:
        '''
            Tests shape commitment dispatching for all modes.

            :exceptions: None.
        '''
        # Point mode
        self.handler.commit_shape(
            CanvasToolMode.POINT, (0.0, 0.0), (10.0, 10.0), self.settings
        )
        self.coordinator.commit_point.assert_called_once_with(
            10.0, 10.0, self.settings
        )

        # Line mode
        self.handler.commit_shape(
            CanvasToolMode.LINE, (0.0, 0.0), (30.0, 30.0), self.settings
        )
        self.coordinator.commit_line.assert_called_once_with(
            (0.0, 0.0), (30.0, 30.0), self.settings
        )

        # Circle mode
        self.handler.commit_shape(
            CanvasToolMode.CIRCLE, (0.0, 0.0), (20.0, 0.0), self.settings
        )
        self.coordinator.commit_circle.assert_called_once_with(
            (0.0, 0.0), (20.0, 0.0), self.settings
        )

        # Rectangle mode
        self.handler.commit_shape(
            CanvasToolMode.RECTANGLE, (0.0, 0.0), (40.0, 40.0), self.settings
        )
        self.coordinator.commit_rectangle.assert_called_once_with(
            (0.0, 0.0), (40.0, 40.0), self.settings
        )

        # Unsupported mode
        self.handler.commit_shape(
            CanvasToolMode.SELECT, (0.0, 0.0), (50.0, 50.0), self.settings
        )


if __name__ == '__main__':
    main()
