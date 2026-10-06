# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_validator.py
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
    Defines structural protocol ITrajectoryValidator for kinematic validation port.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryValidator(Protocol):
    '''
        Structural protocol defining kinematic and workspace validation port.

        It defines:

            :properties:
                | r_min - Inner workspace reach radius in mm.
                | r_max - Outer workspace reach radius in mm.
            :methods:
                | validate_point - Validates whether a waypoint is reachable.
                | validate_feedrate - Validates feedrate within safe mechanical limits.
                | validate_plan - Validates entire trajectory plan against bounds.
    '''

    @property
    def r_min(self) -> float:
        '''
            Returns inner workspace reach radius in mm.

            :return: Minimum reach radius float value.
        '''

    @property
    def r_max(self) -> float:
        '''
            Returns outer workspace reach radius in mm.

            :return: Maximum reach radius float value.
        '''

    def validate_point(self, point: Waypoint) -> object:
        '''
            Validates whether a waypoint is within reachable workspace.

            :param point: Waypoint containing 3D coordinates.
            :return: Validation result object.
        '''

    def validate_feedrate(self, speed: float) -> object:
        '''
            Validates whether feedrate is within safe mechanical limits.

            :param speed: Linear speed in mm/s.
            :return: Validation result object.
        '''

    def validate_plan(
        self,
        plan: ITrajectoryReadOnly,
    ) -> tuple[bool, Sequence[str]]:
        '''
            Validates entire trajectory plan against kinematic and feedrate bounds.

            :param plan: ITrajectoryReadOnly instance to validate.
            :return: Tuple of (is_valid, messages_list).
        '''
