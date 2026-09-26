# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_builder.py
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
    Concrete implementation of binary wire frame assembler.
'''

from __future__ import annotations

from struct import pack
from typing import ClassVar

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.joint_steps import JointSteps
from scarajectory.core.model.communication.protocol.message_id import MessageId
from scarajectory.core.model.communication.protocol.tool_id import ToolId
from scarajectory.infrastructure.communication.protocol.binary.binary_delimiter import BinaryDelimiter
from scarajectory.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scarajectory.infrastructure.communication.protocol.binary.checksum.crc16_ccitt import Crc16Ccitt

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameBuilder:
    '''
        Assembles and checksums wire protocol binary frames for transmission.

        It defines:

            :attributes:
                | SOF1 - First start of frame byte delimiter (0xAA).
                | SOF2 - Second start of frame byte delimiter (0x55).
                | EOF - End of frame byte delimiter (0x0D).
                | JOINT_STEPS_FORMAT - Struct format for 22-byte joint step payload.
                | TOOL_CMD_FORMAT - Struct format for 2-byte tool actuation payload.
                | HEADER_FORMAT - Struct format for 3-byte frame header (msg, seq, len).
                | TRAILER_FORMAT - Struct format for 3-byte frame trailer (crc16, eof).
            :methods:
                | build_frame - Encodes generic binary command frame with CRC16.
                | build_joint_move - Builds joint step movement frame.
                | build_system_cmd - Builds parameterless system command.
                | build_tool_cmd - Builds tool state actuation frame.
                | pack_frame - Serializes complete frame with delimiters and CRC.
    '''

    SOF1: ClassVar[int] = int(BinaryDelimiter.SOF1)
    SOF2: ClassVar[int] = int(BinaryDelimiter.SOF2)
    EOF: ClassVar[int] = int(BinaryDelimiter.EOF)
    JOINT_STEPS_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOINT_STEPS)
    TOOL_CMD_FORMAT: ClassVar[str] = str(BinaryStructFormat.TOOL_CMD)
    HEADER_FORMAT: ClassVar[str] = str(BinaryStructFormat.HEADER)
    TRAILER_FORMAT: ClassVar[str] = str(BinaryStructFormat.TRAILER)

    def build_frame(
        self,
        *,
        msg_id: MessageId,
        seq_num: int,
        payload: bytes = b''
    ) -> BinaryFrame:
        '''
            Constructs and checksums a complete wire protocol BinaryFrame.

            :param msg_id: Command message identifier.
            :param seq_num: Cyclic sequence index (0 - 255).
            :param payload: Raw body bytes (0 to 64 bytes).
            :return: Fully assembled BinaryFrame with valid CRC16.
        '''
        safe_seq: int = seq_num & 0xFF
        header_data: bytes = pack(self.HEADER_FORMAT, int(msg_id), safe_seq, len(payload) & 0xFF)
        crc: int = Crc16Ccitt.calculate(header_data + payload)

        return BinaryFrame(msg_id=msg_id, seq_num=safe_seq, payload=payload, crc16=crc)

    def build_joint_move(
        self,
        *,
        seq_num: int,
        steps: JointSteps
    ) -> BinaryFrame:
        '''
            Builds a joint step motion frame from JointSteps model.

            :param seq_num: Cyclic sequence index.
            :param steps: JointSteps target instance.
            :return: Assembled BinaryFrame with joint move payload.
        '''
        payload: bytes = pack(
            self.JOINT_STEPS_FORMAT,
            steps.target_j1_steps,
            steps.target_j2_steps,
            steps.target_z_steps,
            steps.target_j4_steps,
            steps.duration_us,
            steps.feedrate_scale
        )

        return self.build_frame(msg_id=MessageId.CMD_MOVE_JOINT_STEPS, seq_num=seq_num, payload=payload)

    def build_system_cmd(
        self,
        *,
        msg_id: MessageId,
        seq_num: int
    ) -> BinaryFrame:
        '''
            Builds a parameterless system command frame (ENABLE, ESTOP, PING, etc.).

            :param msg_id: Target command message identifier.
            :param seq_num: Cyclic sequence index.
            :return: Assembled parameterless BinaryFrame.
        '''
        return self.build_frame(msg_id=msg_id, seq_num=seq_num, payload=b'')

    def build_tool_cmd(
        self,
        *,
        seq_num: int,
        tool_id: int,
        state: bool
    ) -> BinaryFrame:
        '''
            Builds a tool actuation command frame (PUMP, VALVE).

            :param seq_num: Cyclic sequence index.
            :param tool_id: Tool identifier (0=PUMP, 1=VALVE).
            :param state: True to activate, False to deactivate.
            :return: Assembled tool command BinaryFrame.
        '''
        target_cmd: MessageId = (
            MessageId.CMD_TOOL_PUMP if tool_id == ToolId.PUMP else MessageId.CMD_TOOL_VALVE
        )
        tool_payload: bytes = pack(self.TOOL_CMD_FORMAT, tool_id & 0xFF, 1 if state else 0)

        return self.build_frame(msg_id=target_cmd, seq_num=seq_num, payload=tool_payload)

    def pack_frame(self, *, frame: BinaryFrame) -> bytes:
        '''
            Encodes the frame into a byte string according to wire format.

            :param frame: BinaryFrame instance to serialize.
            :return: Formatted bytes: SOF1 + SOF2 + MSG + SEQ + LEN + DATA + CRC + EOF.
        '''
        header: bytes = pack(self.HEADER_FORMAT, int(frame.msg_id), frame.seq_num & 0xFF, len(frame.payload) & 0xFF)
        trailer: bytes = pack(self.TRAILER_FORMAT, frame.crc16 & 0xFFFF, self.EOF)

        return bytes([self.SOF1, self.SOF2]) + header + frame.payload + trailer
