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
    Defines abstract interface ITrajectoryValidator for validating kinematic reachability.
'''

from __future__ import annotations

from abc import ABC, abstractmethod

from scarajectory.core.model.point_dto import PointDTO
from scarajectory.core.model.validation_result_dto import ValidationResultDTO

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ITrajectoryValidator(ABC):
    '''
        Abstract contract for kinematic and workspace validators using DTOs.

        It defines:

            :methods:
                | validate_point_dto - Validates whether a point DTO is within reachable workspace.
                | validate_feedrate - Validates whether the feedrate is within safe mechanical limits.
    '''

    @abstractmethod
    def validate_point_dto(self, point: PointDTO) -> ValidationResultDTO:
        '''
            Validates whether a point DTO is within reachable workspace.

            :param point: PointDTO containing 3D coordinates and feedrate.
            :return: ValidationResultDTO with status and details.
            :exceptions: None.
        '''

    @abstractmethod
    def validate_feedrate(self, speed: float) -> ValidationResultDTO:
        '''
            Validates whether the feedrate is within safe mechanical limits.

            :param speed: Linear speed in mm/s.
            :return: ValidationResultDTO with status and details.
            :exceptions: None.
        '''
