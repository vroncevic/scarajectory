# -*- coding: UTF-8 -*-

"""
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
"""

from __future__ import annotations

from math import pi, radians
from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder import BinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPacketStrategy:
    """
        Formats waypoints into wire-protocol binary frames packed with CRC16 and delimiters.

        It defines:

            :attributes:
                | _kinematics - Injected kinematics service for inverse kinematic calculations.
                | _transmission - Injected transmission parameters for radian/mm to step conversions.
                | _builder - Injected binary frame builder for wire serialization.
            :methods:
                | __init__ - Initializes strategy with collaborators.
                | format_waypoint_packet - Formats and packs waypoint into binary frame bytes.
    """

    _kinematics: Final[IKinematicsService]
    _transmission: Final[TransmissionParameters]
    _builder: Final[BinaryFrameBuilder]

    def __init__(
        self,
        *,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters,
        frame_builder: BinaryFrameBuilder,
    ) -> None:
        self._kinematics = kinematics
        self._transmission = transmission
        self._builder = frame_builder

    def _steps_per_rad(self, gear_ratio: float) -> float:
        return (
            self._transmission.steps_per_rev
            * self._transmission.microstepping
            * gear_ratio
        ) / (2.0 * pi)

    def _steps_per_mm_z(self) -> float:
        return (
            self._transmission.steps_per_rev
            * self._transmission.microstepping
        ) / self._transmission.leadscrew_pitch_z

    def format_waypoint_packet(self, *, waypoint: Waypoint, seq_num: int = 0) -> bytes:
        ik_res: tuple[float, float] | None = self._kinematics.solve_ik(waypoint.x, waypoint.y)
        th1: float = ik_res[0] if ik_res is not None else 0.0
        th2: float = ik_res[1] if ik_res is not None else 0.0
        th4: float = radians(waypoint.phi)

        steps_j1: int = round(th1 * self._steps_per_rad(self._transmission.gear_ratio_j1))
        steps_j2: int = round(th2 * self._steps_per_rad(self._transmission.gear_ratio_j2))
        steps_z: int = round(waypoint.z * self._steps_per_mm_z())
        steps_j4: int = round(th4 * self._steps_per_rad(self._transmission.gear_ratio_j4))
        duration_us: int = int(max(1000.0, (1000000.0 / max(1.0, waypoint.speed))))

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
