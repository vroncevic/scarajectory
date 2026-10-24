# -*- coding: UTF-8 -*-

'''
Module
    ihandler_test.py
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
    Unit tests for ICanvasShapeHandler protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.canvas.handler.shape.ihandler import ICanvasShapeHandler
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode


class MockShapeHandler:
    '''
        Mock conforming to ICanvasShapeHandler structurally.
    '''

    def create_waypoint_at(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> TrajectoryWaypoint:
        '''
            Builds a TrajectoryWaypoint at coordinates.

            :param wx: World X.
            :param wy: World Y.
            :param settings: Settings.
            :return: Waypoint.
        '''
        _ = (wx, wy, settings)
        return TrajectoryWaypoint(
            x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, name='stub', command=''
        )

    def create_relocated_waypoint(
        self,
        current: TrajectoryWaypoint,
        wx: float,
        wy: float,
    ) -> TrajectoryWaypoint:
        '''
            Builds updated TrajectoryWaypoint with relocated coordinates.

            :param current: Current waypoint.
            :param wx: World X.
            :param wy: World Y.
            :return: Waypoint.
        '''
        _ = (current, wx, wy)
        return TrajectoryWaypoint(
            x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, name='stub', command=''
        )

    def commit_point(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Commits single point to trajectory plan.

            :param wx: World X.
            :param wy: World Y.
            :param settings: Settings.
        '''
        _ = (wx, wy, settings)

    def commit_shape(
        self,
        tool_mode: CanvasToolMode,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Dispatches shape commitment based on active tool mode.

            :param tool_mode: Tool mode.
            :param p1: Start coordinate tuple.
            :param p2: End coordinate tuple.
            :param settings: Settings.
        '''
        _ = (tool_mode, p1, p2, settings)


class TestICanvasShapeHandler(TestCase):
    '''
        Test cases for ICanvasShapeHandler protocol compliance.

        It defines:

            :methods:
                | test_structural_compliance - Tests protocol runtime checkable conformance.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies mock satisfies ICanvasShapeHandler protocol.

            :exceptions: None.
        '''
        handler = MockShapeHandler()
        self.assertIsInstance(handler, ICanvasShapeHandler)


if __name__ == '__main__':
    main()
