# -*- coding: UTF-8 -*-

'''
Module
    icoordinator_test.py
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
    Unit tests for IShapePlanCoordinator protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.handler.coordinator.icoordinator import IShapePlanCoordinator
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings


class MockShapePlanCoordinator:
    '''
        Mock conforming to IShapePlanCoordinator structurally.
    '''

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
            :param settings: Canvas settings.
        '''
        _ = (wx, wy, settings)

    def commit_line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits straight line.

            :param p1: Start coordinate tuple.
            :param p2: End coordinate tuple.
            :param settings: Canvas settings.
        '''
        _ = (p1, p2, settings)

    def commit_rectangle(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits rectangle.

            :param p1: Start corner coordinate tuple.
            :param p2: End corner coordinate tuple.
            :param settings: Canvas settings.
        '''
        _ = (p1, p2, settings)

    def commit_circle(
        self,
        center: tuple[float, float],
        boundary: tuple[float, float],
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits circle.

            :param center: Center coordinate tuple.
            :param boundary: Boundary coordinate tuple.
            :param settings: Canvas settings.
        '''
        _ = (center, boundary, settings)


class TestIShapePlanCoordinator(TestCase):
    '''
        Test cases for IShapePlanCoordinator protocol compliance.

        It defines:

            :methods:
                | test_structural_compliance - Tests protocol runtime checkable conformance.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies mock satisfies IShapePlanCoordinator protocol.

            :exceptions: None.
        '''
        coordinator = MockShapePlanCoordinator()
        self.assertIsInstance(coordinator, IShapePlanCoordinator)


if __name__ == '__main__':
    main()
