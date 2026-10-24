# -*- coding: UTF-8 -*-

'''
Module
    strategy.py
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
    Formats waypoints into wire-protocol binary frames packed with CRC16 and delimiters.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.kinematics.pose.angles import JointAngles
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.imotion_builder import IBinaryMotionFrameBuilder

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPacketStrategy:
    '''
        Formats waypoints into wire-protocol binary frames packed with CRC16 and delimiters.

        It defines:

            :attributes:
                | _step_discretizer - Injected step discretizer for kinematic conversions.
                | _motion_frame_builder - Injected binary motion frame builder.
                | _frame_packer - Injected binary frame wire packer.
                | _prev_angles - Internal angle state for relative motion discretization.
            :methods:
                | __init__ - Initializes strategy with collaborators.
                | format_waypoint_packet - Formats and packs waypoint into binary frame bytes.
                | reset - Resets internal kinematic angle tracking state to home position.
                | get_version - Returns component version string.
    '''

    _step_discretizer: IStepDiscretizer
    _motion_frame_builder: IBinaryMotionFrameBuilder
    _frame_packer: IBinaryFramePacker
    _prev_angles: JointAngles

    def __init__(
        self,
        *,
        step_discretizer: IStepDiscretizer,
        motion_frame_builder: IBinaryMotionFrameBuilder,
        frame_packer: IBinaryFramePacker,
    ) -> None:
        '''
            Initializes strategy with step discretizer and frame builder collaborators.

            :param step_discretizer: Injected IStepDiscretizer implementation.
            :param motion_frame_builder: Injected IBinaryMotionFrameBuilder implementation.
            :param frame_packer: Injected IBinaryFramePacker implementation.
        '''
        self._step_discretizer: Final[IStepDiscretizer] = step_discretizer
        self._motion_frame_builder: Final[IBinaryMotionFrameBuilder] = motion_frame_builder
        self._frame_packer: Final[IBinaryFramePacker] = frame_packer
        self._prev_angles = JointAngles(
            theta1=0.0,
            theta2=0.0,
            z=0.0,
            theta4=0.0,
        )

    def format_waypoint_packet(
        self,
        *,
        waypoint: TrajectoryWaypoint,
        seq_num: int = 0,
    ) -> bytes:
        '''
            Packs trajectory waypoint into binary JointSteps frame with CRC16 framing.

            :param waypoint: TrajectoryWaypoint containing coordinates, orientation, and speed.
            :param seq_num: Packet cyclic sequence number (0-255).
            :return: Serialized binary frame byte payload.
        '''
        try:
            scaralang_wp: Waypoint = Waypoint(
                x=waypoint.x,
                y=waypoint.y,
                z=waypoint.z,
                phi=waypoint.phi,
                speed=waypoint.speed,
                name=waypoint.name,
                command=waypoint.command,
            )
            joint_steps, self._prev_angles = self._step_discretizer.discretize_waypoint(
                waypoint=scaralang_wp,
                prev_angles=self._prev_angles,
            )
        except ScaraKinematicsError:
            target_steps: JointStepCoordinates = self._step_discretizer.angles_to_steps(
                self._prev_angles.theta1,
                self._prev_angles.theta2,
                self._prev_angles.z,
                self._prev_angles.theta4,
            )
            joint_steps = JointSteps(
                target_j1_steps=target_steps.j1,
                target_j2_steps=target_steps.j2,
                target_z_steps=target_steps.z,
                target_j4_steps=target_steps.j4,
                duration_us=10000,
                feedrate_scale=100,
            )

        frame: BinaryFrame = self._motion_frame_builder.build_joint_move(
            seq_num=seq_num,
            steps=joint_steps,
        )

        return self._frame_packer.pack_frame(frame=frame)

    def reset(self) -> None:
        '''
            Resets internal kinematic angle tracking state to home position.

            :exceptions: None.
        '''
        self._prev_angles = JointAngles(
            theta1=0.0,
            theta2=0.0,
            z=0.0,
            theta4=0.0,
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
