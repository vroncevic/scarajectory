# -*- coding: UTF-8 -*-

'''
Module
    kinematics_service.py
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
    Dedicated analytical SCARA kinematics service solving forward and inverse kinematics.
'''

from __future__ import annotations

from math import atan2, cos, degrees, hypot, pi, sin, sqrt
from typing import Final

from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsService:
    '''
        Dedicated analytical SCARA forward and inverse kinematics calculation engine.

        It defines:

            :attributes:
                | _bounds - ScaraBounds containing link lengths, angular limits and margins.
                | _r_min - Minimum annular reach distance from origin in mm.
                | _r_max - Maximum annular reach distance from origin in mm.
            :methods:
                | __init__ - Initializes kinematics service with robot bounds.
                | bounds - Returns active bounds model.
                | r_min - Returns minimum reach radius in mm.
                | r_max - Returns maximum reach radius in mm.
                | solve_ik - Solves analytical inverse kinematics for joint angles.
                | solve_fk - Computes Cartesian coordinates from joint angles.
                | is_in_workspace - Checks if Cartesian coordinates lie within the workspace envelope.
                | is_joint_reachable - Evaluates reachability within joint limits and singularity deadband.
    '''

    _bounds: ScaraBounds
    _r_min: float
    _r_max: float

    def __init__(self, bounds: ScaraBounds = ScaraBounds()) -> None:
        '''
            Initializes kinematics service with robot bounds and computes reach radii.

            :param bounds: ScaraBounds instance.
        '''
        self._bounds: Final[ScaraBounds] = bounds
        self._r_min: Final[float] = abs(bounds.l1 - bounds.l2)
        self._r_max: Final[float] = bounds.l1 + bounds.l2

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns the active robot geometry and limits model.

            :return: ScaraBounds instance.
        '''
        return self._bounds

    @property
    def r_min(self) -> float:
        '''
            Returns the minimum annular workspace reach radius in mm.

            :return: Minimum reach radius float value.
        '''
        return self._r_min

    @property
    def r_max(self) -> float:
        '''
            Returns the maximum annular workspace reach radius in mm.

            :return: Maximum reach radius float value.
        '''
        return self._r_max

    def solve_ik(
        self,
        x: float,
        y: float,
        elbow_left: bool = False
    ) -> tuple[float, float] | None:
        '''
            Solves analytical inverse kinematics for SCARA 2-DOF arm.

            :param x: Target Cartesian X coordinate in mm.
            :param y: Target Cartesian Y coordinate in mm.
            :param elbow_left: True for elbow-left configuration, False for elbow-right.
            :return: Tuple of (theta1, theta2) in radians, or None if mathematically unreachable.
        '''
        l1: float = self._bounds.l1
        l2: float = self._bounds.l2
        r_sq: float = x * x + y * y
        cos_q2: float = (r_sq - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)

        if abs(cos_q2) > 1.0:
            return None

        sin_q2: float = sqrt(max(0.0, 1.0 - cos_q2 * cos_q2))
        if elbow_left:
            sin_q2 = -sin_q2

        theta2: float = atan2(sin_q2, cos_q2)
        k1: float = l1 + l2 * cos_q2
        k2: float = l2 * sin_q2
        theta1: float = atan2(y, x) - atan2(k2, k1)
        theta1 = (theta1 + pi) % (2.0 * pi) - pi

        return theta1, theta2

    def solve_fk(
        self,
        theta1: float,
        theta2: float
    ) -> tuple[float, float]:
        '''
            Computes Cartesian end-effector position from joint angles via forward kinematics.

            :param theta1: Joint 1 (shoulder) angle in radians.
            :param theta2: Joint 2 (elbow) angle in radians.
            :return: Tuple of (x, y) Cartesian coordinates in mm.
        '''
        l1: float = self._bounds.l1
        l2: float = self._bounds.l2
        total_angle: float = theta1 + theta2
        x: float = l1 * cos(theta1) + l2 * cos(total_angle)
        y: float = l1 * sin(theta1) + l2 * sin(total_angle)
        return x, y

    def is_in_workspace(
        self,
        x: float,
        y: float,
        z: float
    ) -> tuple[bool, str]:
        '''
            Checks whether target coordinates lie within the physical annular workspace and Z limits.

            :param x: Target Cartesian X coordinate in mm.
            :param y: Target Cartesian Y coordinate in mm.
            :param z: Target Cartesian Z coordinate in mm.
            :return: Tuple of (is_in_bounds, error_or_warning_message).
        '''
        r: float = hypot(x, y)
        if r > self._r_max + 1e-4:
            return (
                False,
                f'Point ({x:.1f}, {y:.1f}) exceeds maximum reach R_max={self._r_max:.1f} mm (r={r:.1f} mm)'
            )
        if r < self._r_min - 1e-4:
            return (
                False,
                f'Point ({x:.1f}, {y:.1f}) is inside deadzone R_min={self._r_min:.1f} mm (r={r:.1f} mm)'
            )
        if z < self._bounds.z_min - 1e-4 or z > self._bounds.z_max + 1e-4:
            return (
                False,
                f'Elevation Z={z:.1f} mm is out of range [{self._bounds.z_min:.1f}, {self._bounds.z_max:.1f}] mm'
            )
        return True, 'Point is within Cartesian workspace'

    def is_joint_reachable(
        self,
        x: float,
        y: float
    ) -> tuple[bool, list[str]]:
        '''
            Evaluates whether target position can be achieved within physical joint limits and singularity deadband.

            :param x: Target Cartesian X coordinate in mm.
            :param y: Target Cartesian Y coordinate in mm.
            :return: Tuple of (is_reachable, list_of_warning_messages).
        '''
        reasons: list[str] = []
        reachable_any: bool = False

        for elbow_left in (False, True):
            ik_res = self.solve_ik(x, y, elbow_left=elbow_left)
            if ik_res is None:
                reasons.append('Mathematically unreachable (cos_q2 > 1.0)')
                continue

            theta1, theta2 = ik_res

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
            return False, reasons

        return True, []
