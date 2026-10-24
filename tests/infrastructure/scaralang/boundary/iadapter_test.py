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
    Unit tests for IWorkspaceBoundaryAdapter structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyBoundaryAdapter:
    '''
        Dummy class implementing IWorkspaceBoundaryAdapter structurally.
    '''

    def calculate_forbidden_zone_polygon(
        self,
        bounds: ScaraBounds,
    ) -> tuple[Point2D, ...]:
        '''
            Returns empty tuple of Point2D.

            :param bounds: Kinematic bounds.
            :return: Empty tuple.
            :exceptions: None.
        '''
        _ = bounds
        return ()

    def is_j1_limited(self, bounds: ScaraBounds) -> bool:
        '''
            Returns dummy boolean.

            :param bounds: Kinematic bounds.
            :return: True.
            :exceptions: None.
        '''
        _ = bounds
        return True

    def get_version(self) -> str:
        '''
            Returns dummy version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.3'


class TestIWorkspaceBoundaryAdapter(TestCase):
    '''
        Unit test cases verifying IWorkspaceBoundaryAdapter structural protocol.
    '''

    def test_protocol_implementation(self) -> None:
        '''
            Verifies structural adherence to IWorkspaceBoundaryAdapter protocol.

            :exceptions: None.
        '''
        dummy = DummyBoundaryAdapter()
        self.assertIsInstance(dummy, IWorkspaceBoundaryAdapter)


if __name__ == '__main__':
    main()
