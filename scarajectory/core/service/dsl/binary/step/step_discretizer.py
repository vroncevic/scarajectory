# -*- coding: UTF-8 -*-

'''
Module
    step_discretizer.py
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
    Converts Cartesian waypoints into discrete motor joint steps with timing.
'''

from __future__ import annotations

from math import pi, radians

from scarajectory.core.model.communication.protocol.joint_steps import JointSteps
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepDiscretizer:
    '''
        Discretizes Cartesian motion waypoints into hardware motor step coordinates.

        It defines:

            :attributes:
                | _kinematics - Analytical SCARA kinematics calculation engine.
                | _transmission - Mechanical gear ratio and motor resolution model.
            :methods:
                | __init__ - Initializes step discretizer with kinematics and transmission.
                | discretize_waypoint - Solves IK and maps Cartesian waypoint into JointSteps.
                | calculate_segment_duration - Computes execution duration in microseconds.
                | angles_to_steps - Converts joint radians/mm to integer motor steps.
    '''

    _kinematics: IKinematicsService
    _transmission: TransmissionParameters

    def __init__(
        self,
        *,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters
    ) -> None:
        '''
            Initializes step discretizer with kinematics and transmission models.

            :param kinematics: Injected IKinematicsService instance.
            :param transmission: Injected TransmissionParameters instance.
            :exceptions: None.
        '''
        self._kinematics = kinematics
        self._transmission = transmission

    def _steps_per_rad(self, gear_ratio: float) -> float:
        '''
            Calculates motor step scale factor per radian of joint rotation.

            :param gear_ratio: Mechanical reduction ratio.
            :return: Steps per radian float value.
        '''
        return (
            self._transmission.steps_per_rev
            * self._transmission.microstepping
            * gear_ratio
        ) / (2.0 * pi)

    def _steps_per_mm_z(self) -> float:
        '''
            Calculates motor step scale factor per linear millimeter of Z travel.

            :return: Steps per millimeter float value.
        '''
        return (
            self._transmission.steps_per_rev
            * self._transmission.microstepping
        ) / self._transmission.leadscrew_pitch_z

    def angles_to_steps(
        self,
        theta1_rad: float,
        theta2_rad: float,
        z_mm: float,
        theta4_rad: float
    ) -> tuple[int, int, int, int]:
        '''
            Converts joint angles and linear Z travel into discrete motor steps.

            :param theta1_rad: Shoulder joint angle in radians.
            :param theta2_rad: Elbow joint angle in radians.
            :param z_mm: Linear vertical travel in millimeters.
            :param theta4_rad: Wrist joint angle in radians.
            :return: Tuple of (j1, j2, z, j4) integer microsteps.
        '''
        j1: int = round(theta1_rad * self._steps_per_rad(self._transmission.gear_ratio_j1))
        j2: int = round(theta2_rad * self._steps_per_rad(self._transmission.gear_ratio_j2))
        z: int = round(z_mm * self._steps_per_mm_z())
        j4: int = round(theta4_rad * self._steps_per_rad(self._transmission.gear_ratio_j4))
        return (j1, j2, z, j4)

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: tuple[float, float, float, float] | None = None
    ) -> tuple[JointSteps, tuple[float, float, float, float]]:
        '''
            Solves IK and converts Cartesian waypoint into motor steps with duration.

            :param waypoint: Target Cartesian Waypoint instance.
            :param prev_angles: Optional preceding joint angles (th1, th2, z, th4).
            :return: Tuple of (JointSteps model, new joint angles tuple).
            :exceptions: ValueError if position is unreachable.
        '''
        ik_sol: tuple[float, float] | None = self._kinematics.solve_ik(
            waypoint.x, waypoint.y, elbow_left=False
        )
        if ik_sol is None:
            raise ValueError(
                f'Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}) is outside kinematic reach.'
            )
        th1, th2 = ik_sol
        z_mm: float = waypoint.z
        th4: float = radians(waypoint.phi)
        new_angles: tuple[float, float, float, float] = (th1, th2, z_mm, th4)

        j1, j2, z_steps, j4 = self.angles_to_steps(
            th1, th2, z_mm, th4
        )
        current_steps: tuple[int, int, int, int] = (0, 0, 0, 0)
        if prev_angles is not None:
            current_steps = self.angles_to_steps(*prev_angles)

        target_steps: tuple[int, int, int, int] = (j1, j2, z_steps, j4)
        duration_us: int = self.calculate_segment_duration(
            current_steps=current_steps,
            target_steps=target_steps,
            speed_mm_s=waypoint.speed
        )
        return (
            JointSteps(
                target_j1_steps=j1,
                target_j2_steps=j2,
                target_z_steps=z_steps,
                target_j4_steps=j4,
                duration_us=duration_us,
                feedrate_scale=100
            ),
            new_angles
        )

    def calculate_segment_duration(
        self,
        *,
        current_steps: tuple[int, int, int, int],
        target_steps: tuple[int, int, int, int],
        speed_mm_s: float
    ) -> int:
        '''
            Computes segment execution duration in microseconds.

            :param current_steps: Initial joint step coordinates.
            :param target_steps: Target joint step coordinates.
            :param speed_mm_s: Planned linear tool speed in mm/s.
            :return: Microsecond execution duration.
            :exceptions: None.
        '''
        deltas: tuple[int, int, int, int] = (
            abs(target_steps[0] - current_steps[0]),
            abs(target_steps[1] - current_steps[1]),
            abs(target_steps[2] - current_steps[2]),
            abs(target_steps[3] - current_steps[3])
        )
        max_delta: int = max(deltas)
        if max_delta == 0:
            return 1000

        safe_speed: float = max(1.0, speed_mm_s)
        # Approximate step frequency: 200 steps/mm base reference
        duration_sec: float = max_delta / (safe_speed * 10.0)
        duration_us: int = int(duration_sec * 1000000.0)
        return max(duration_us, 5000)
