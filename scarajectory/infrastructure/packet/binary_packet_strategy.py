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
    Binary packet formatting strategy compiling Waypoint instances into packed binary wire frames.
'''

from __future__ import annotations

from math import radians
from typing import Final

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.transmission.itransmission_step_calculator import ITransmissionStepCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPacketStrategy:
    '''
        Formats waypoints into wire-protocol binary frames packed with CRC16 and delimiters.

        It defines:

            :attributes:
                | _kinematics - Injected kinematics service for inverse kinematic calculations.
                | _transmission - Injected transmission parameters for gear ratio retrieval.
                | _builder - Injected binary frame builder for wire serialization.
                | _calculator - Injected step calculator for kinematic conversions.
            :methods:
                | __init__ - Initializes strategy with collaborators.
                | format_waypoint_packet - Formats and packs waypoint into binary frame bytes.
    '''

    _kinematics: IKinematicsService
    _transmission: TransmissionParameters
    _builder: IBinaryFrameBuilder
    _calculator: ITransmissionStepCalculator

    def __init__(
        self,
        *,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters,
        frame_builder: IBinaryFrameBuilder,
        step_calculator: ITransmissionStepCalculator,
    ) -> None:
        '''
            Initializes strategy with kinematics, transmission, and frame builder collaborators.

            :param kinematics: Injected IKinematicsService implementation.
            :param transmission: Injected TransmissionParameters configuration DTO.
            :param frame_builder: Injected IBinaryFrameBuilder builder implementation.
            :param step_calculator: Injected ITransmissionStepCalculator instance.
        '''
        self._kinematics: Final[IKinematicsService] = kinematics
        self._transmission: Final[TransmissionParameters] = transmission
        self._builder: Final[IBinaryFrameBuilder] = frame_builder
        self._calculator: Final[ITransmissionStepCalculator] = step_calculator

    def format_waypoint_packet(self, *, waypoint: Waypoint, seq_num: int = 0) -> bytes:
        '''
            Packs trajectory waypoint into binary JointSteps frame with CRC16 framing.

            :param waypoint: Waypoint containing coordinates, orientation, and speed.
            :param seq_num: Packet cyclic sequence number (0-255).
            :return: Serialized binary frame byte payload.
        '''
        point = Point2D(x=waypoint.x, y=waypoint.y)
        ik_res = self._kinematics.solve_ik(point=point)
        th1: float = 0.0
        th2: float = 0.0
        if bool(ik_res):
            th1, th2 = ik_res
        th4: float = radians(waypoint.phi)

        steps_j1: int = self._calculator.revolute_steps(
            angle_rad=th1, gear_ratio=self._transmission.gear_ratio_j1
        )
        steps_j2: int = self._calculator.revolute_steps(
            angle_rad=th2, gear_ratio=self._transmission.gear_ratio_j2
        )
        steps_z: int = self._calculator.linear_z_steps(z_mm=waypoint.z)
        steps_j4: int = self._calculator.revolute_steps(
            angle_rad=th4, gear_ratio=self._transmission.gear_ratio_j4
        )
        duration_us: int = self._calculator.calculate_duration_us(speed=waypoint.speed)

        joint_steps: JointSteps = JointSteps(
            target_j1_steps=steps_j1,
            target_j2_steps=steps_j2,
            target_z_steps=steps_z,
            target_j4_steps=steps_j4,
            duration_us=duration_us,
            feedrate_scale=100,
        )
        frame: BinaryFrame = self._builder.build_joint_move(
            seq_num=seq_num,
            steps=joint_steps,
        )
        return self._builder.pack_frame(frame=frame)
