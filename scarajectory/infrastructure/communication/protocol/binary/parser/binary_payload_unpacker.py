# -*- coding: UTF-8 -*-

'''
Module
    binary_payload_unpacker.py
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
    Dedicated deserializer decoding binary packet payloads into typed domain models.
'''

from __future__ import annotations

from struct import unpack
from typing import ClassVar

from scarajectory.core.model.communication.event.fault_event import FaultEvent
from scarajectory.core.model.communication.event.move_event import MoveEvent
from scarajectory.core.model.communication.protocol.joint_steps import JointSteps
from scarajectory.core.model.communication.telemetry.diagnostics_bundle import DiagnosticsBundle
from scarajectory.core.model.communication.telemetry.diagnostics_snapshot import DiagnosticsSnapshot
from scarajectory.core.model.communication.telemetry.scara_status import ScaraStatus
from scarajectory.core.service.communication.telemetry.diagnostics_snapshot_factory import DiagnosticsSnapshotFactory
from scarajectory.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPayloadUnpacker:
    '''
        Deserializer decoding raw binary frame payloads into structured domain models.

        It defines:

            :attributes:
                | STATUS_PAYLOAD_FORMAT - Struct format for 19-byte status payload.
                | JOINT_STEPS_FORMAT - Struct format for 22-byte joint step payload.
                | MOVE_EVENT_FORMAT - Struct format for 5-byte move event payload.
                | FAULT_EVENT_FORMAT - Struct format for 6-byte fault event payload.
                | ACK_FORMAT - Struct format for 2-byte ACK payload.
                | NACK_FORMAT - Struct format for 2-byte NACK payload.
                | DIAGNOSTICS_FORMAT - Struct format for 56-byte diagnostics payload.
            :methods:
                | unpack_scara_status - Deserializes 19-byte status payload into ScaraStatus.
                | unpack_robot_status - Backward-compatible alias for unpack_scara_status.
                | unpack_joint_steps - Deserializes 22-byte joint steps into JointSteps.
                | unpack_move_event - Deserializes 5-byte move event into MoveEvent.
                | unpack_fault_event - Deserializes 6-byte fault event into FaultEvent.
                | unpack_ack - Deserializes 2-byte ACK into (acked_msg_id, queue_depth).
                | unpack_nack - Deserializes 2-byte NACK into (rejected_msg_id, error_code).
                | unpack_diagnostics - Deserializes 56-byte diagnostics report.
                | unpack_tool_cmd - Deserializes 2-byte tool command into (tool_id, state).
    '''

    STATUS_PAYLOAD_FORMAT: ClassVar[str] = str(BinaryStructFormat.STATUS)
    JOINT_STEPS_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOINT_STEPS)
    TOOL_CMD_FORMAT: ClassVar[str] = str(BinaryStructFormat.TOOL_CMD)
    MOVE_EVENT_FORMAT: ClassVar[str] = str(BinaryStructFormat.MOVE_EVENT)
    FAULT_EVENT_FORMAT: ClassVar[str] = str(BinaryStructFormat.FAULT_EVENT)
    ACK_FORMAT: ClassVar[str] = str(BinaryStructFormat.ACK)
    NACK_FORMAT: ClassVar[str] = str(BinaryStructFormat.NACK)
    DIAGNOSTICS_FORMAT: ClassVar[str] = str(BinaryStructFormat.DIAGNOSTICS)

    @classmethod
    def unpack_tool_cmd(cls, data: bytes) -> tuple[int, bool]:
        '''
            Deserializes a 2-byte binary payload into tool ID and boolean state.

            :param data: Input raw binary bytes.
            :return: Tuple containing (tool_id, state).
        '''
        values: tuple[int, int] = unpack(cls.TOOL_CMD_FORMAT, data[:2])
        return values[0], bool(values[1])

    @classmethod
    def unpack_scara_status(cls, data: bytes) -> ScaraStatus:
        '''
            Deserializes a 19-byte binary payload into a ScaraStatus instance.

            :param data: Input raw binary bytes.
            :return: ScaraStatus instance.
        '''
        values: tuple[int, int, int, int, int, int, int] = unpack(
            cls.STATUS_PAYLOAD_FORMAT, data[:19]
        )
        return ScaraStatus(
            system_state=values[0],
            is_busy=bool(values[1]),
            queue_count=values[2],
            j1_steps=values[3],
            j2_steps=values[4],
            z_steps=values[5],
            j4_steps=values[6]
        )

    @classmethod
    def unpack_robot_status(cls, data: bytes) -> ScaraStatus:
        '''
            Backward-compatible alias for unpack_scara_status.

            :param data: Input raw binary bytes.
            :return: ScaraStatus instance.
        '''
        return cls.unpack_scara_status(data)

    @classmethod
    def unpack_joint_steps(cls, data: bytes) -> JointSteps:
        '''
            Deserializes a 22-byte binary payload into a JointSteps instance.

            :param data: Input raw binary bytes.
            :return: JointSteps instance.
        '''
        values: tuple[int, int, int, int, int, int] = unpack(
            cls.JOINT_STEPS_FORMAT, data[:22]
        )
        return JointSteps(
            target_j1_steps=values[0],
            target_j2_steps=values[1],
            target_z_steps=values[2],
            target_j4_steps=values[3],
            duration_us=values[4],
            feedrate_scale=values[5]
        )

    @classmethod
    def unpack_move_event(cls, data: bytes) -> MoveEvent:
        '''
            Deserializes a 5-byte binary payload into a MoveEvent instance.

            :param data: Input raw binary bytes.
            :return: MoveEvent instance.
        '''
        values: tuple[int, int] = unpack(cls.MOVE_EVENT_FORMAT, data[:5])
        return MoveEvent(event_type=values[0], segment_id=values[1])

    @classmethod
    def unpack_fault_event(cls, data: bytes) -> FaultEvent:
        '''
            Deserializes a 6-byte binary payload into a FaultEvent instance.

            :param data: Input raw binary bytes.
            :return: FaultEvent instance.
        '''
        values: tuple[int, int, int] = unpack(cls.FAULT_EVENT_FORMAT, data[:6])
        return FaultEvent(
            severity=values[0],
            fault_code=values[1],
            extra_info=values[2]
        )

    @classmethod
    def unpack_ack(cls, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into ACK message ID and queue depth.

            :param data: Input raw binary bytes.
            :return: Tuple containing (acked_message_id, queue_depth).
        '''
        values: tuple[int, int] = unpack(cls.ACK_FORMAT, data[:2])
        return values[0], values[1]

    @classmethod
    def unpack_nack(cls, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into NACK message ID and error code.

            :param data: Input raw binary bytes.
            :return: Tuple containing (rejected_message_id, error_code).
        '''
        values: tuple[int, int] = unpack(cls.NACK_FORMAT, data[:2])
        return values[0], values[1]

    @classmethod
    def unpack_diagnostics(cls, data: bytes) -> DiagnosticsSnapshot:
        '''
            Deserializes a 56-byte binary payload into a DiagnosticsSnapshot.

            :param data: Input raw binary bytes.
            :return: DiagnosticsSnapshot instance.
        '''
        values = unpack(cls.DIAGNOSTICS_FORMAT, data[:56])
        bundle: DiagnosticsBundle = DiagnosticsBundle(
            rx_frames_total=values[0],
            tx_frames_total=values[1],
            crc_errors=values[2],
            rx_buffer_overruns=values[3],
            queue_high_watermark=values[4],
            mem_pool_min_free=values[5],
            total_steps_executed_j1=values[6],
            total_steps_executed_j2=values[7],
            total_steps_executed_z=values[8],
            total_steps_executed_j4=values[9],
            following_error_j1=values[10],
            following_error_j2=values[11],
            following_error_z=values[12],
            following_error_j4=values[13],
            stall_guard_flags=values[14],
            driver_fault_flags=values[15],
            uptime_ms=values[16]
        )
        return DiagnosticsSnapshotFactory.create(bundle=bundle)
