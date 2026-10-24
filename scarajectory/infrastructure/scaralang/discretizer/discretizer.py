# -*- coding: UTF-8 -*-

'''
Module
    discretizer.py
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
    Discretizes Cartesian motion waypoints supporting dual-elbow (Righty/Lefty) kinematics.
'''

from __future__ import annotations

from math import radians
from sys import stderr
from typing import ClassVar, Final

from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.pose.angles import JointAngles
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator
from scaralang.core.service.kinematics.solver.analytical.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

from scarajectory.infrastructure.scaralang.discretizer.dependencies import DiscretizerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DualElbowStepDiscretizer:
    '''
        Discretizes Cartesian motion waypoints with adaptive Righty/Lefty elbow selection.

        It defines:

            :attributes:
                | DEFAULT_FEEDRATE_SCALE - Default percentage feedrate scale.
                | _spatial - Injected analytical spatial SCARA kinematics solver engine.
                | _numerical_spatial - Injected numerical DLS spatial kinematics solver.
                | _transmission - Injected bidirectional transmission converter.
                | _duration_calculator - Injected segment duration calculator.
                | _bounds - Injected manipulator kinematic bounds model.
            :methods:
                | __init__ - Initializes step discretizer with dependency bundle.
                | angles_to_steps - Converts joint radians/mm to integer motor steps.
                | discretize_waypoint - Solves IK with dual-elbow selection and maps into JointSteps.
                | get_version - Returns implementation version string.
    '''

    DEFAULT_FEEDRATE_SCALE: ClassVar[int] = 100

    _spatial: ISpatialKinematicsSolver
    _numerical_spatial: INumericalSpatialKinematicsSolver
    _transmission: IJointStepTransmissionConverter
    _duration_calculator: ISegmentDurationCalculator
    _bounds: ScaraBounds

    def __init__(self, dependencies: DiscretizerDependencies) -> None:
        '''
            Initializes step discretizer with injected dependencies bundle.

            :param dependencies: Injected DiscretizerDependencies bundle.
            :exceptions: None.
        '''
        self._spatial: Final[ISpatialKinematicsSolver] = dependencies.spatial
        self._numerical_spatial: Final[INumericalSpatialKinematicsSolver] = (
            dependencies.numerical_spatial
        )
        self._transmission: Final[IJointStepTransmissionConverter] = dependencies.transmission
        self._duration_calculator: Final[ISegmentDurationCalculator] = (
            dependencies.duration_calculator
        )
        self._bounds: Final[ScaraBounds] = dependencies.bounds

    def angles_to_steps(
        self,
        theta1_rad: float,
        theta2_rad: float,
        z_mm: float,
        theta4_rad: float,
    ) -> JointStepCoordinates:
        '''
            Converts joint angles and linear Z travel into discrete motor steps.

            :param theta1_rad: Shoulder joint angle in radians.
            :param theta2_rad: Elbow joint angle in radians.
            :param z_mm: Linear vertical travel in millimeters.
            :param theta4_rad: Wrist joint angle in radians.
            :return: JointStepCoordinates containing integer microsteps.
            :exceptions: None.
        '''
        return self._transmission.angles_to_steps(
            theta1_rad, theta2_rad, z_mm, theta4_rad
        )

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: JointAngles,
    ) -> tuple[JointSteps, JointAngles]:
        '''
            Solves IK with dual-elbow support and converts Cartesian waypoint into motor steps.

            :param waypoint: Target Cartesian Waypoint instance.
            :param prev_angles: Preceding joint angles model.
            :return: Tuple of (JointSteps model, new joint angles model).
            :exceptions:
                | ScaraKinematicsError: If position violates joint limits or is unreachable.
        '''
        pose = CartesianPose(
            x=waypoint.x,
            y=waypoint.y,
            z=waypoint.z,
            phi=radians(waypoint.phi),
        )
        sol_r: ScaraJoints = self._spatial.solve_ik_4d(
            pose=pose,
            elbow_left=False,
        )
        r_valid: bool = (
            sol_r.reachable
            and self._bounds.joints.j1_min_rad <= sol_r.theta1 <= self._bounds.joints.j1_max_rad
            and self._bounds.joints.j2_min_rad <= sol_r.theta2 <= self._bounds.joints.j2_max_rad
        )

        if r_valid:
            selected_sol: ScaraJoints = sol_r
        else:
            sol_l: ScaraJoints = self._spatial.solve_ik_4d(
                pose=pose,
                elbow_left=True,
            )
            l_valid: bool = (
                sol_l.reachable
                and self._bounds.joints.j1_min_rad <= sol_l.theta1 <= self._bounds.joints.j1_max_rad
                and self._bounds.joints.j2_min_rad <= sol_l.theta2 <= self._bounds.joints.j2_max_rad
            )
            if l_valid:
                selected_sol = sol_l
            else:
                if IkStatus.Z_LIMIT_EXCEEDED in (sol_r.status, sol_l.status):
                    raise ScaraKinematicsError(
                        f'Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}, {waypoint.z:.2f}) '
                        f'is outside vertical limits ({sol_r.status.name}).'
                    )

                sol_num: ScaraJoints = self._numerical_spatial.solve_dls_4d(
                    target_pose=pose,
                    initial_joints=ScaraJoints(
                        theta1=prev_angles.theta1,
                        theta2=prev_angles.theta2,
                        z=prev_angles.z,
                        theta4=prev_angles.theta4,
                        reachable=True,
                        status=IkStatus.SUCCESS,
                    ),
                )
                num_valid: bool = (
                    sol_num.reachable
                    and self._bounds.joints.j1_min_rad <= sol_num.theta1 <= self._bounds.joints.j1_max_rad
                    and self._bounds.joints.j2_min_rad <= sol_num.theta2 <= self._bounds.joints.j2_max_rad
                )
                if not num_valid:
                    raise ScaraKinematicsError(
                        f'Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}, {waypoint.z:.2f}) '
                        f'is unreachable: analytical dual-elbow failed '
                        f'(Righty: {sol_r.status.name}, Lefty: {sol_l.status.name}), '
                        f'and numerical DLS fallback failed ({sol_num.status.name}).'
                    )

                stderr.write(
                    f'scarajectory: warning: Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}, {waypoint.z:.2f}) '
                    f'analytical dual-elbow failed (Righty: {sol_r.status.name}, Lefty: {sol_l.status.name}); '
                    f'recovered using numerical DLS fallback.\n'
                )
                selected_sol = sol_num

        target_steps: JointStepCoordinates = self.angles_to_steps(
            selected_sol.theta1,
            selected_sol.theta2,
            selected_sol.z,
            selected_sol.theta4,
        )
        current_steps: JointStepCoordinates = self.angles_to_steps(
            prev_angles.theta1,
            prev_angles.theta2,
            prev_angles.z,
            prev_angles.theta4,
        )
        duration_us: int = self._duration_calculator.calculate_duration(
            current_steps=current_steps,
            target_steps=target_steps,
            speed_mm_s=waypoint.speed,
        )
        return (
            JointSteps(
                target_j1_steps=target_steps.j1,
                target_j2_steps=target_steps.j2,
                target_z_steps=target_steps.z,
                target_j4_steps=target_steps.j4,
                duration_us=duration_us,
                feedrate_scale=self.DEFAULT_FEEDRATE_SCALE,
            ),
            JointAngles(
                theta1=selected_sol.theta1,
                theta2=selected_sol.theta2,
                z=selected_sol.z,
                theta4=selected_sol.theta4,
            ),
        )

    def get_version(self) -> str:
        '''
            Returns implementation version string.

            :return: Implementation version string.
            :exceptions: None.
        '''
        return __version__
