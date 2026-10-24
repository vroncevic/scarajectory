# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Infrastructure adapter delegating workspace boundary calculations to scaralang.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceBoundaryAdapter:
    '''
        Adapter delegating workspace boundary calculations to scaralang.

        It defines:

            :attributes:
                | _boundary_service - Injected scaralang boundary service.
            :methods:
                | __init__ - Initializes adapter with boundary service collaborator.
                | calculate_forbidden_zone_polygon - Calculates vertices of rear unreachable zone.
                | is_j1_limited - Checks whether J1 angular range is bounded below PI.
                | get_version - Returns adapter component version string.
    '''

    _boundary_service: IWorkspaceBoundaryService

    def __init__(self, *, boundary_service: IWorkspaceBoundaryService) -> None:
        '''
            Initializes WorkspaceBoundaryAdapter with scaralang boundary service.

            :param boundary_service: Injected scaralang boundary service collaborator.
            :exceptions: None.
        '''
        self._boundary_service: Final[IWorkspaceBoundaryService] = boundary_service

    def calculate_forbidden_zone_polygon(
        self,
        bounds: ScaraBounds,
    ) -> tuple[Point2D, ...]:
        '''
            Calculates vertices of the rear unreachable boundary crescent.

            :param bounds: Kinematic geometry and limits model.
            :return: Tuple of Point2D Cartesian coordinates in millimeters.
            :exceptions: None.
        '''
        return self._boundary_service.calculate_forbidden_zone_polygon(bounds)

    def is_j1_limited(self, bounds: ScaraBounds) -> bool:
        '''
            Checks whether J1 angular range is bounded below PI.

            :param bounds: Kinematic geometry and limits model.
            :return: True if J1 is bounded below PI, False otherwise.
            :exceptions: None.
        '''
        return self._boundary_service.is_j1_limited(bounds)

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
