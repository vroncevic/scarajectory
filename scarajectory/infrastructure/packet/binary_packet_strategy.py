# -*- coding: UTF-8 -*-

'''
Module
    binary_packet_strategy.py
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

from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.service.compiler.binary.step.istep_discretizer import IStepDiscretizer
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.trajectory.waypoint import Waypoint

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
                | _discretizer - Injected step discretizer for kinematic conversions.
                | _builder - Injected binary frame builder for wire serialization.
                | _prev_angles - Internal angle state for relative motion discretization.
            :methods:
                | __init__ - Initializes strategy with collaborators.
                | format_waypoint_packet - Formats and packs waypoint into binary frame bytes.
    '''

    _discretizer: IStepDiscretizer
    _builder: IBinaryFrameBuilder
    _prev_angles: tuple[float, float, float, float]

    def __init__(
        self,
        *,
        discretizer: IStepDiscretizer,
        frame_builder: IBinaryFrameBuilder,
    ) -> None:
        '''
            Initializes strategy with step discretizer and frame builder collaborators.

            :param discretizer: Injected IStepDiscretizer implementation.
            :param frame_builder: Injected IBinaryFrameBuilder builder implementation.
        '''
        self._discretizer: Final[IStepDiscretizer] = discretizer
        self._builder: Final[IBinaryFrameBuilder] = frame_builder
        self._prev_angles = (0.0, 0.0, 0.0, 0.0)

    def format_waypoint_packet(
        self,
        *,
        waypoint: Waypoint,
        seq_num: int = 0,
    ) -> bytes:
        '''
            Packs trajectory waypoint into binary JointSteps frame with CRC16 framing.

            :param waypoint: Waypoint containing coordinates, orientation, and speed.
            :param seq_num: Packet cyclic sequence number (0-255).
            :return: Serialized binary frame byte payload.
        '''
        try:
            joint_steps, self._prev_angles = self._discretizer.discretize_waypoint(
                waypoint=waypoint,
                prev_angles=self._prev_angles,
            )
        except ScaraKinematicsError:
            target_steps: tuple[int, int, int, int] = self._discretizer.angles_to_steps(
                *self._prev_angles
            )
            joint_steps = JointSteps(
                target_j1_steps=target_steps[0],
                target_j2_steps=target_steps[1],
                target_z_steps=target_steps[2],
                target_j4_steps=target_steps[3],
                duration_us=10000,
                feedrate_scale=100,
            )
        frame: BinaryFrame = self._builder.build_joint_move(
            seq_num=seq_num,
            steps=joint_steps,
        )
        return self._builder.pack_frame(frame=frame)
