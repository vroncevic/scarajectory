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
    Implementation of kinematic reachability validator delegating to kinematics service.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.model.trajectory.validation_result import ValidationResult
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.core.model.trajectory.trajectory_metrics import TrajectoryMetrics
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scarajectory.core.service.kinematics.kinematics_service import KinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryValidator:
    '''
        Enforces SCARA mechanical reachability and kinematic envelope validation.

        It defines:

            :attributes:
                | _kinematics - Injected analytical kinematics service.
                | _bounds - Kinematic parameters of the SCARA arm.
                | _r_min - Minimum reach distance from origin in mm.
                | _r_max - Maximum reach distance from origin in mm.
            :methods:
                | __init__ - Initializes validator and kinematics service.
                | bounds - Returns active bounds model.
                | r_min - Returns inner workspace radius.
                | r_max - Returns outer workspace radius.
                | kinematics - Returns active kinematics service.
                | validate_point - Validates Waypoint coordinates against reachability rules.
                | validate_feedrate - Validates that speed is within safe mechanical range.
                | validate_plan - Validates entire trajectory plan against kinematic bounds.
    '''

    _kinematics: IKinematicsService
    _bounds: ScaraBounds
    _r_min: float
    _r_max: float

    def __init__(
        self,
        bounds: ScaraBounds = ScaraBounds(),
        kinematics: IKinematicsService | None = None
    ) -> None:
        '''
            Initializes validator using injected or default KinematicsService.

            :param bounds: ScaraBounds encapsulating link lengths and limits.
            :param kinematics: Optional IKinematicsService instance.
        '''
        self._kinematics: Final[IKinematicsService] = (
            kinematics if kinematics is not None else KinematicsService(bounds=bounds)
        )
        self._bounds: Final[ScaraBounds] = self._kinematics.bounds
        self._r_min: Final[float] = self._kinematics.r_min
        self._r_max: Final[float] = self._kinematics.r_max

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns active bounds model.

            :return: ScaraBounds instance.
        '''
        return self._bounds

    @property
    def r_min(self) -> float:
        '''
            Returns inner workspace radius (mm).

            :return: Minimum reach radius.
        '''
        return self._r_min

    @property
    def r_max(self) -> float:
        '''
            Returns outer workspace radius (mm).

            :return: Maximum reach radius.
        '''
        return self._r_max

    @property
    def kinematics(self) -> IKinematicsService:
        '''
            Returns active kinematics service.

            :return: IKinematicsService instance.
        '''
        return self._kinematics

    def validate_point(self, point: Waypoint) -> ValidationResult:
        '''
            Validates Waypoint coordinates against annular horizontal reach and vertical bounds.

            :param point: Target Waypoint.
            :return: ValidationResult with pass/fail and descriptive reason.
        '''
        in_workspace, ws_msg = self._kinematics.is_in_workspace(point.x, point.y, point.z)
        if not in_workspace:
            return ValidationResult(is_valid=False, message=ws_msg)

        is_reachable, reasons = self._kinematics.is_joint_reachable(point.x, point.y)
        if not is_reachable:
            if reasons and 'Mathematically unreachable' in reasons[0]:
                return ValidationResult(
                    is_valid=False,
                    message=f'Point ({point.x:.1f}, {point.y:.1f}) is kinematically unreachable'
                )
            reason_str: str = ', '.join(reasons) if reasons else 'Joint limits exceeded'
            return ValidationResult(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) violates joint limits: {reason_str}'
            )

        return ValidationResult(is_valid=True, message='Point is reachable')

    def validate_feedrate(self, speed: float) -> ValidationResult:
        '''
            Validates that speed is within safe mechanical operation range.

            :param speed: Feedrate in mm/s.
            :return: ValidationResult.
        '''
        if speed < self._bounds.min_speed:
            return ValidationResult(
                is_valid=False,
                message=f'Speed {speed:.1f} mm/s is too slow (minimum {self._bounds.min_speed:.1f} mm/s)'
            )
        if speed > self._bounds.max_speed:
            return ValidationResult(
                is_valid=False,
                message=f'Speed {speed:.1f} mm/s exceeds max safe feedrate {self._bounds.max_speed:.1f} mm/s'
            )
        return ValidationResult(is_valid=True, message='Speed is valid')

    def validate_plan(self, plan: ITrajectoryReadOnly) -> tuple[bool, list[str]]:
        '''
            Validates the current trajectory plan against robot kinematic bounds.

            :param plan: ITrajectoryReadOnly instance to validate.
            :return: Tuple of (is_valid, messages_list).
        '''
        waypoints = plan.waypoints
        if not waypoints:
            return False, ['Trajectory plan is empty. Please add waypoints.']

        messages: list[str] = []
        all_valid: bool = True

        for index, pt in enumerate(waypoints, start=1):
            res_pt: ValidationResult = self.validate_point(pt)
            if not res_pt.is_valid:
                all_valid = False
                messages.append(f'Point P{index} ({pt.x:.1f}, {pt.y:.1f}, {pt.z:.1f}): {res_pt.message}')

            res_spd: ValidationResult = self.validate_feedrate(pt.speed)
            if not res_spd.is_valid:
                all_valid = False
                messages.append(f'Point P{index} Speed ({pt.speed:.1f} mm/s): {res_spd.message}')

        if all_valid:
            total_dist: float = TrajectoryMetrics.calculate_distance(waypoints)
            est_time: float = TrajectoryMetrics.calculate_duration(waypoints)
            messages.append(
                f'Validation PASSED: All {len(waypoints)} waypoints are within reachable workspace.\n'
                f'Total Path Distance: {total_dist:.2f} mm | Estimated Time: {est_time:.2f} s'
            )

        return all_valid, messages
