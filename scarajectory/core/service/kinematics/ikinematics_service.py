# -*- coding: UTF-8 -*-

'''
Module
    ikinematics_service.py
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
    Interface protocol defining analytical SCARA kinematics calculations and reachability.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IKinematicsService(Protocol):
    '''
        Structural interface protocol for analytical SCARA kinematics calculations.

        It defines:

            :attributes:
                | bounds - Active robot geometry bounds and limits model.
                | r_min - Minimum annular workspace reach radius in mm.
                | r_max - Maximum annular workspace reach radius in mm.
            :methods:
                | solve_ik - Solves analytical inverse kinematics for joint angles.
                | solve_fk - Computes Cartesian coordinates from joint angles.
                | is_in_workspace - Checks whether coordinates fall within annular and height envelope.
                | is_joint_reachable - Evaluates if position is reachable within joint and singularity limits.
    '''

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns the active robot geometry and limits model.

            :return: ScaraBounds instance.
        '''

    @property
    def r_min(self) -> float:
        '''
            Returns the minimum annular workspace reach radius in mm.

            :return: Minimum reach radius float value.
        '''

    @property
    def r_max(self) -> float:
        '''
            Returns the maximum annular workspace reach radius in mm.

            :return: Maximum reach radius float value.
        '''

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
