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
    Implementation of kinematic reachability validator enforcing SCARA physical geometry bounds.
'''

from __future__ import annotations

from math import hypot, sqrt, atan2, pi, degrees
from typing import Final

from scarajectory.core.model.point import Point
from scarajectory.core.model.validation_result import ValidationResult
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.model.trajectory_metrics import TrajectoryMetrics

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
                | _bounds - Kinematic parameters of the SCARA arm.
                | _r_min - Minimum reach distance from origin in mm.
                | _r_max - Maximum reach distance from origin in mm.
            :methods:
                | __init__ - Initializes validator geometry boundaries.
                | bounds - Returns active bounds model.
                | r_min - Returns inner workspace radius.
                | r_max - Returns outer workspace radius.
                | validate_point_dto - Validates Point coordinates against annular reach.
                | validate_feedrate - Validates that speed is within safe mechanical range.
                | validate_plan - Validates entire trajectory plan against kinematic bounds.
    '''

    _bounds: ScaraBounds
    _r_min: float
    _r_max: float

    def __init__(self, bounds: ScaraBounds = ScaraBounds()) -> None:
        '''
            Initializes validator geometry boundaries using ScaraBounds.

            :param bounds: ScaraBounds encapsulating link lengths and limits.
            :exceptions: None.
        '''
        self._bounds: Final[ScaraBounds] = bounds
        self._r_min: Final[float] = abs(bounds.l1 - bounds.l2)
        self._r_max: Final[float] = bounds.l1 + bounds.l2

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns active bounds model.

            :return: ScaraBounds instance.
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

    def validate_point_dto(self, point: Point) -> ValidationResult:
        '''
            Validates Point coordinates against annular horizontal reach and vertical bounds.

            :param point: Target Point.
            :return: ValidationResult with pass/fail and descriptive reason.
            :exceptions: None.
        '''
        r: float = hypot(point.x, point.y)
        if r > self._r_max + 1e-4:
            return ValidationResult(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) exceeds maximum reach R_max={self._r_max:.1f} mm (r={r:.1f} mm)'
            )
        if r < self._r_min - 1e-4:
            return ValidationResult(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) is inside deadzone R_min={self._r_min:.1f} mm (r={r:.1f} mm)'
            )
        if point.z < self._bounds.z_min - 1e-4 or point.z > self._bounds.z_max + 1e-4:
            return ValidationResult(
                is_valid=False,
                message=f'Elevation Z={point.z:.1f} mm is out of range [{self._bounds.z_min:.1f}, {self._bounds.z_max:.1f}] mm'
            )

        l1: float = self._bounds.l1
        l2: float = self._bounds.l2
        r_sq: float = point.x * point.x + point.y * point.y
        cos_q2: float = (r_sq - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
        if abs(cos_q2) > 1.0:
            return ValidationResult(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) is kinematically unreachable'
            )

        reachable_any: bool = False
        reasons: list[str] = []
        for elbow_left in (False, True):
            sin_q2: float = sqrt(max(0.0, 1.0 - cos_q2 * cos_q2))
            if elbow_left:
                sin_q2 = -sin_q2
            theta2: float = atan2(sin_q2, cos_q2)
            k1: float = l1 + l2 * cos_q2
            k2: float = l2 * sin_q2
            theta1: float = atan2(point.y, point.x) - atan2(k2, k1)
            theta1 = (theta1 + pi) % (2.0 * pi) - pi

            if theta1 < self._bounds.j1_min_rad or theta1 > self._bounds.j1_max_rad:
                reasons.append(f'J1 angle {degrees(theta1):.1f}° exceeds limit')
                continue
            if theta2 < self._bounds.j2_min_rad or theta2 > self._bounds.j2_max_rad:
                reasons.append(f'J2 angle {degrees(theta2):.1f}° exceeds limit')
                continue
            if abs(theta2) < self._bounds.singularity_theta2_min_rad:
                reasons.append('J2 in singularity deadband')
                continue
            reachable_any = True
            break

        if not reachable_any:
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
            :exceptions: None.
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

    def validate_plan(self, plan: ITrajectoryPlan) -> tuple[bool, list[str]]:
        '''
            Validates the current trajectory plan against robot kinematic bounds.

            :param plan: ITrajectoryPlan instance to validate.
            :return: Tuple of (is_valid, messages_list).
            :exceptions: None.
        '''
        waypoints = plan.waypoints
        if not waypoints:
            return False, ['Trajectory plan is empty. Please add waypoints.']

        messages: list[str] = []
        all_valid: bool = True

        for index, pt in enumerate(waypoints, start=1):
            pt_dto = pt.to_dto()
            res_pt: ValidationResult = self.validate_point_dto(pt_dto)
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
