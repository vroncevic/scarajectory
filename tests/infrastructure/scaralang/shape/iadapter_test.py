# -*- coding: UTF-8 -*-

'''
Module
    iadapter_test.py
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
    Unit tests for IShapePlannerAdapter structural protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.circle import CircleGeometry

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ValidShapePlannerAdapter:
    '''Mock class implementing IShapePlannerAdapter structurally.'''

    def plan_contour(
        self,
        points: Sequence[Point2D],
        *,
        z: float,
        speed: float,
        closed: bool = True,
    ) -> list[TrajectoryWaypoint]:
        '''Plans contour waypoints.'''
        _ = (points, z, speed, closed)
        return []

    def plan_circle(
        self,
        geometry: CircleGeometry,
    ) -> list[TrajectoryWaypoint]:
        '''Plans circular perimeter waypoints.'''
        _ = geometry
        return []

    def get_version(self) -> str:
        '''Returns mock version.'''
        return '1.0.3'


class _IncompleteShapePlannerAdapter:
    '''Mock class missing methods from IShapePlannerAdapter.'''

    def get_version(self) -> str:
        '''Returns mock version.'''
        return '1.0.3'

    def is_available(self) -> bool:
        '''Returns mock availability.'''
        return False


class IShapePlannerAdapterTest(TestCase):
    '''Test case verifying IShapePlannerAdapter structural subtyping.'''

    def test_protocol_conformance(self) -> None:
        '''Verifies valid structural implementation satisfies protocol.'''
        adapter: _ValidShapePlannerAdapter = _ValidShapePlannerAdapter()
        self.assertIsInstance(adapter, IShapePlannerAdapter)

    def test_protocol_rejection(self) -> None:
        '''Verifies incomplete implementation is rejected by protocol.'''
        incomplete: _IncompleteShapePlannerAdapter = (
            _IncompleteShapePlannerAdapter()
        )
        self.assertNotIsInstance(incomplete, IShapePlannerAdapter)


if __name__ == '__main__':
    main()
