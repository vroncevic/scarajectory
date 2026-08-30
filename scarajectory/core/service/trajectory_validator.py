# -*- coding: UTF-8 -*-

'''
Module
    trajectory_validator.py
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
    Concrete implementation of ITrajectoryValidator enforcing SCARA physical geometry bounds.
'''

from __future__ import annotations

import math
from typing import Final, override

from scarajectory.core.model.point_dto import PointDTO
from scarajectory.core.model.validation_result_dto import ValidationResultDTO
from scarajectory.core.model.scara_bounds_dto import ScaraBoundsDTO
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryValidator(ITrajectoryValidator):
    '''
        Enforces SCARA mechanical reachability and kinematic envelope validation.

        It defines:

            :attributes:
                | _bounds - Kinematic parameters of the SCARA arm.
                | _r_min - Minimum reach distance from origin in mm.
                | _r_max - Maximum reach distance from origin in mm.
            :methods:
                | __init__ - Initializes validator geometry boundaries.
                | bounds - Returns active bounds DTO.
                | r_min - Returns inner workspace radius.
                | r_max - Returns outer workspace radius.
                | validate_point_dto - Validates PointDTO coordinates against annular reach.
                | validate_feedrate - Validates that speed is within safe mechanical range.
    '''

    _bounds: Final[ScaraBoundsDTO]
    _r_min: Final[float]
    _r_max: Final[float]

    def __init__(self, bounds: ScaraBoundsDTO = ScaraBoundsDTO()) -> None:
        '''
            Initializes validator geometry boundaries using ScaraBoundsDTO.

            :param bounds: ScaraBoundsDTO encapsulating link lengths and limits.
            :exceptions: None.
        '''
        self._bounds = bounds
        self._r_min = abs(bounds.l1 - bounds.l2)
        self._r_max = bounds.l1 + bounds.l2

    @property
    def bounds(self) -> ScaraBoundsDTO:
        '''
            Returns active bounds DTO.

            :return: ScaraBoundsDTO instance.
            :exceptions: None.
        '''
        return self._bounds

    @property
    def r_min(self) -> float:
        '''
            Returns inner workspace radius (mm).

            :return: Minimum reach radius.
            :exceptions: None.
        '''
        return self._r_min

    @property
    def r_max(self) -> float:
        '''
            Returns outer workspace radius (mm).

            :return: Maximum reach radius.
            :exceptions: None.
        '''
        return self._r_max

    @override
    def validate_point_dto(self, point: PointDTO) -> ValidationResultDTO:
        '''
            Validates PointDTO coordinates against annular horizontal reach and vertical bounds.

            :param point: Target PointDTO.
            :return: ValidationResultDTO with pass/fail and descriptive reason.
            :exceptions: None.
        '''
        r: float = math.hypot(point.x, point.y)
        if r > self._r_max + 1e-4:
            return ValidationResultDTO(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) exceeds maximum reach R_max={self._r_max:.1f} mm (r={r:.1f} mm)'
            )
        if r < self._r_min - 1e-4:
            return ValidationResultDTO(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) is inside deadzone R_min={self._r_min:.1f} mm (r={r:.1f} mm)'
            )
        if point.z < self._bounds.z_min - 1e-4 or point.z > self._bounds.z_max + 1e-4:
            return ValidationResultDTO(
                is_valid=False,
                message=f'Elevation Z={point.z:.1f} mm is out of range [{self._bounds.z_min:.1f}, {self._bounds.z_max:.1f}] mm'
            )
        return ValidationResultDTO(is_valid=True, message='Point is reachable')

    @override
    def validate_feedrate(self, speed: float) -> ValidationResultDTO:
        '''
            Validates that speed is within safe mechanical operation range.

            :param speed: Feedrate in mm/s.
            :return: ValidationResultDTO.
            :exceptions: None.
        '''
        if speed < self._bounds.min_speed:
            return ValidationResultDTO(
                is_valid=False,
                message=f'Speed {speed:.1f} mm/s is too slow (minimum {self._bounds.min_speed:.1f} mm/s)'
            )
        if speed > self._bounds.max_speed:
            return ValidationResultDTO(
                is_valid=False,
                message=f'Speed {speed:.1f} mm/s exceeds max safe feedrate {self._bounds.max_speed:.1f} mm/s'
            )
        return ValidationResultDTO(is_valid=True, message='Speed is valid')
