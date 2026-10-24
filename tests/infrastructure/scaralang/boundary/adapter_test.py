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
    Unit tests for WorkspaceBoundaryAdapter component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scarajectory.infrastructure.scaralang.boundary.adapter import WorkspaceBoundaryAdapter
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceBoundaryAdapter(TestCase):
    '''
        Unit test cases verifying WorkspaceBoundaryAdapter behavior and delegation.
    '''

    mock_service: MagicMock
    adapter: WorkspaceBoundaryAdapter
    bounds: ScaraBounds

    def setUp(self) -> None:
        '''
            Sets up test fixture with mocked boundary service and sample bounds.

            :exceptions: None.
        '''
        self.mock_service = MagicMock()
        self.adapter = WorkspaceBoundaryAdapter(
            boundary_service=self.mock_service
        )
        self.bounds = DefaultScaraProfile.create_bounds()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that adapter structurally satisfies IWorkspaceBoundaryAdapter.

            :exceptions: None.
        '''
        self.assertIsInstance(self.adapter, IWorkspaceBoundaryAdapter)

    def test_calculate_forbidden_zone_polygon(self) -> None:
        '''
            Verifies delegation of polygon calculation to underlying service.

            :exceptions: None.
        '''
        expected = (Point2D(x=10.0, y=20.0), Point2D(x=30.0, y=40.0))
        self.mock_service.calculate_forbidden_zone_polygon.return_value = expected

        result = self.adapter.calculate_forbidden_zone_polygon(self.bounds)
        self.assertEqual(result, expected)
        self.mock_service.calculate_forbidden_zone_polygon.assert_called_once_with(
            self.bounds
        )

    def test_is_j1_limited(self) -> None:
        '''
            Verifies delegation of J1 limit check to underlying service.

            :exceptions: None.
        '''
        self.mock_service.is_j1_limited.return_value = True

        result = self.adapter.is_j1_limited(self.bounds)
        self.assertTrue(result)
        self.mock_service.is_j1_limited.assert_called_once_with(self.bounds)

    def test_get_version(self) -> None:
        '''
            Verifies adapter returns version string.

            :exceptions: None.
        '''
        self.assertIsInstance(self.adapter.get_version(), str)


if __name__ == '__main__':
    main()
