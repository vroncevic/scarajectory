# -*- coding: UTF-8 -*-

'''
Module
    binary_protocol_test.py
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
    Unit tests for binary protocol constants, unpackers, frame parser FSM, and sub-controllers.
'''

from __future__ import annotations

from os.path import abspath, dirname
from struct import pack
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.communication.event.fault_event import FaultEvent
from scarajectory.core.model.communication.event.move_event import MoveEvent
from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.joint_steps import JointSteps
from scarajectory.core.model.communication.protocol.message_id import MessageId
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.communication.protocol.tool_id import ToolId
from scarajectory.core.model.communication.telemetry.diagnostics_snapshot import DiagnosticsSnapshot
from scarajectory.core.model.communication.telemetry.scara_status import ScaraStatus
from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.communication.protocol.ibinary_frame_parser import IBinaryFrameParser
from scarajectory.infrastructure.communication.controller.base_sub_controller import BaseSubController
from scarajectory.infrastructure.communication.protocol.binary.binary_delimiter import BinaryDelimiter
from scarajectory.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker
from scarajectory.infrastructure.communication.protocol.binary.parser.parser_state import ParserState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockRawChannel:
    '''
        Mock raw channel for testing BaseSubController.
    '''

    def __init__(self) -> None:
        self.connected: bool = True
        self.commands: list[str] = []
        self.frames_bytes: list[bytes] = []

    def is_connected(self) -> bool:
        return self.connected

    def send_raw_command(self, cmd: str) -> None:
        self.commands.append(cmd)

    def send_raw_bytes(self, data: bytes) -> bool:
        self.frames_bytes.append(data)
        return True


class DummySubController(BaseSubController):
    '''
        Concrete dummy sub-controller testing BaseSubController methods.
    '''

    def test_next_seq(self) -> int:
        return self._next_seq()

    def test_send_cmd(self, cmd: str) -> bool:
        return self._send_command(cmd)

    def test_send_fr(self, frame: BinaryFrame) -> bool:
        return self._send_frame(frame)


class BinaryProtocolTest(TestCase):
    '''
        Unit tests for binary protocol constants, unpackers, frame parser FSM, and sub-controllers.

        It defines:

            :methods:
                | test_binary_delimiter_constants - Tests delimiter byte constants.
                | test_binary_struct_formats - Tests struct format definitions.
                | test_parser_state_enums - Tests parser state machine enum values.
                | test_tool_id_enums - Tests tool identifier enum values.
                | test_payload_unpacker_methods - Tests all BinaryPayloadUnpacker deserializers.
                | test_frame_parser_fsm_parsing - Tests BinaryFrameParser streaming feed FSM.
                | test_frame_parser_fsm_errors - Tests BinaryFrameParser error handling and resets.
                | test_base_sub_controller_lifecycle - Tests BaseSubController channel and sequencing.
    '''

    def test_binary_delimiter_constants(self) -> None:
        '''
            Tests delimiter byte constants and payload limit.
        '''
        self.assertEqual(int(BinaryDelimiter.SOF1), 0xAA)
        self.assertEqual(int(BinaryDelimiter.SOF2), 0x55)
        self.assertEqual(int(BinaryDelimiter.EOF), 0x0D)
        self.assertEqual(int(BinaryDelimiter.MAX_PAYLOAD_LEN), 64)

    def test_binary_struct_formats(self) -> None:
        '''
            Tests struct format string definitions.
        '''
        self.assertEqual(str(BinaryStructFormat.HEADER), '<BBB')
        self.assertEqual(str(BinaryStructFormat.TRAILER), '<HB')
        self.assertEqual(str(BinaryStructFormat.JOINT_STEPS), '<iiiiIH')
        self.assertEqual(str(BinaryStructFormat.TOOL_CMD), '<BB')
        self.assertEqual(str(BinaryStructFormat.STATUS), '<BBBiiii')
        self.assertEqual(str(BinaryStructFormat.MOVE_EVENT), '<BI')
        self.assertEqual(str(BinaryStructFormat.FAULT_EVENT), '<BBI')
        self.assertEqual(str(BinaryStructFormat.ACK), '<BB')
        self.assertEqual(str(BinaryStructFormat.NACK), '<BB')
        self.assertEqual(str(BinaryStructFormat.DIAGNOSTICS), '<IIIIBBIIIIiiiiBBI')

    def test_parser_state_enums(self) -> None:
        '''
            Tests parser state machine enum values.
        '''
        self.assertEqual(int(ParserState.SEARCH_SOF1), 0)
        self.assertEqual(int(ParserState.SEARCH_SOF2), 1)
        self.assertEqual(int(ParserState.READ_MSG_ID), 2)
        self.assertEqual(int(ParserState.READ_SEQ_NUM), 3)
        self.assertEqual(int(ParserState.READ_PAYLOAD_LEN), 4)
        self.assertEqual(int(ParserState.READ_PAYLOAD), 5)
        self.assertEqual(int(ParserState.READ_CRC_LO), 6)
        self.assertEqual(int(ParserState.READ_CRC_HI), 7)
        self.assertEqual(int(ParserState.READ_EOF), 8)

    def test_tool_id_enums(self) -> None:
        '''
            Tests ToolId enumeration values.
        '''
        self.assertEqual(int(ToolId.PUMP), 0)
        self.assertEqual(int(ToolId.VALVE), 1)

    def test_payload_unpacker_methods(self) -> None:
        '''
            Tests all BinaryPayloadUnpacker deserializers.
        '''
        # 1. unpack_joint_steps
        raw_steps = pack(str(BinaryStructFormat.JOINT_STEPS), 100, -200, 300, 400, 50000, 100)
        steps: JointSteps = BinaryPayloadUnpacker.unpack_joint_steps(raw_steps)
        self.assertEqual(steps.target_j1_steps, 100)
        self.assertEqual(steps.target_j2_steps, -200)
        self.assertEqual(steps.target_z_steps, 300)
        self.assertEqual(steps.target_j4_steps, 400)
        self.assertEqual(steps.duration_us, 50000)
        self.assertEqual(steps.feedrate_scale, 100)

        # 2. unpack_tool_cmd
        raw_tool = pack(str(BinaryStructFormat.TOOL_CMD), int(ToolId.VALVE), 1)
        tool_id, tool_state = BinaryPayloadUnpacker.unpack_tool_cmd(raw_tool)
        self.assertEqual(tool_id, int(ToolId.VALVE))
        self.assertTrue(tool_state)

        # 3. unpack_scara_status and unpack_robot_status alias
        raw_status = pack(str(BinaryStructFormat.STATUS), 1, 1, 3, 500, 600, 700, 800)
        status: ScaraStatus = BinaryPayloadUnpacker.unpack_scara_status(raw_status)
        self.assertEqual(status.system_state, 1)
        self.assertTrue(status.is_busy)
        self.assertEqual(status.queue_count, 3)
        self.assertEqual(status.j1_steps, 500)
        self.assertEqual(status.j2_steps, 600)
        self.assertEqual(status.z_steps, 700)
        self.assertEqual(status.j4_steps, 800)
        status_alias = BinaryPayloadUnpacker.unpack_robot_status(raw_status)
        self.assertEqual(status_alias.system_state, status.system_state)

        # 4. unpack_move_event
        raw_move = pack(str(BinaryStructFormat.MOVE_EVENT), 2, 42)
        move_ev: MoveEvent = BinaryPayloadUnpacker.unpack_move_event(raw_move)
        self.assertEqual(move_ev.event_type, 2)
        self.assertEqual(move_ev.segment_id, 42)

        # 5. unpack_fault_event
        raw_fault = pack(str(BinaryStructFormat.FAULT_EVENT), 5, 2, 0x1234)
        fault_ev: FaultEvent = BinaryPayloadUnpacker.unpack_fault_event(raw_fault)
        self.assertEqual(fault_ev.severity, 5)
        self.assertEqual(fault_ev.fault_code, 2)
        self.assertEqual(fault_ev.extra_info, 0x1234)

        # 6. unpack_ack
        raw_ack = pack(str(BinaryStructFormat.ACK), int(MessageId.CMD_HOME), 7)
        ack_cmd, queue_space = BinaryPayloadUnpacker.unpack_ack(raw_ack)
        self.assertEqual(ack_cmd, int(MessageId.CMD_HOME))
        self.assertEqual(queue_space, 7)

        # 7. unpack_nack
        raw_nack = pack(str(BinaryStructFormat.NACK), int(MessageId.CMD_ENABLE), 3)
        nack_cmd, nack_reason = BinaryPayloadUnpacker.unpack_nack(raw_nack)
        self.assertEqual(nack_cmd, int(MessageId.CMD_ENABLE))
        self.assertEqual(nack_reason, 3)

        # 8. unpack_diagnostics
        raw_diag = pack(
            str(BinaryStructFormat.DIAGNOSTICS),
            1000, 5, 2, 0, 4, 12, 100, 200, 300, 400, 1, 2, 3, 4, 0, 0, 5000
        )
        diag_snap: DiagnosticsSnapshot = BinaryPayloadUnpacker.unpack_diagnostics(raw_diag)
        self.assertEqual(diag_snap.uptime_ms, 5000)
        self.assertEqual(diag_snap.crc_errors, 2)

    def test_frame_parser_fsm_parsing(self) -> None:
        '''
            Tests BinaryFrameParser streaming feed FSM.
        '''
        builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        parser: IBinaryFrameParser = BinaryFrameParserFactory.create()

        frame = builder.build_system_cmd(msg_id=MessageId.CMD_HOME, seq_num=10)
        wire_bytes = builder.pack_frame(frame=frame)

        # Feed byte by byte
        frames: list[BinaryFrame] = []
        for b in wire_bytes:
            frames.extend(parser.feed_bytes(bytes([b])))

        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].msg_id, MessageId.CMD_HOME)
        self.assertEqual(frames[0].seq_num, 10)
        self.assertEqual(parser.get_state(), ParserState.SEARCH_SOF1)

    def test_frame_parser_fsm_errors(self) -> None:
        '''
            Tests BinaryFrameParser error handling and resets.
        '''
        builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        parser: BinaryFrameParser = BinaryFrameParser()

        # Send frame with corrupted CRC
        frame = builder.build_system_cmd(msg_id=MessageId.CMD_ENABLE, seq_num=5)
        wire_bytes = bytearray(builder.pack_frame(frame=frame))
        wire_bytes[-3] ^= 0xFF  # Corrupt CRC byte

        parsed = parser.feed_bytes(bytes(wire_bytes))
        self.assertEqual(len(parsed), 0)
        self.assertEqual(parser.get_state(), ParserState.SEARCH_SOF1)

        # Send invalid SOF2
        bad_sof2 = bytes([0xAA, 0x00, 0x01])
        parser.feed_bytes(bad_sof2)
        self.assertEqual(parser.get_state(), ParserState.SEARCH_SOF1)

        # Feed partial SOF1
        parser.feed_byte(0xAA)
        self.assertEqual(parser.get_state(), ParserState.SEARCH_SOF2)

        # Reset parser
        parser.reset()
        self.assertEqual(parser.get_state(), ParserState.SEARCH_SOF1)

    def test_base_sub_controller_lifecycle(self) -> None:
        '''
            Tests BaseSubController channel and sequencing operations.
        '''
        mock_channel = MockRawChannel()
        builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        ctrl = DummySubController(
            raw_channel=mock_channel,
            frame_builder=builder,
            protocol_mode=ProtocolMode.ASCII,
        )

        self.assertTrue(ctrl.is_connected())

        # Sequencing
        s0 = ctrl.test_next_seq()
        s1 = ctrl.test_next_seq()
        self.assertEqual(s0, 0)
        self.assertEqual(s1, 1)

        # Protocol mode switch
        ctrl.set_protocol_mode(ProtocolMode.BINARY)

        # Send command
        self.assertTrue(ctrl.test_send_cmd('<CMD:TEST>'))
        self.assertEqual(mock_channel.commands, ['<CMD:TEST>'])

        # Send frame
        frame = builder.build_system_cmd(msg_id=MessageId.CMD_HOME, seq_num=2)
        self.assertTrue(ctrl.test_send_fr(frame))
        self.assertEqual(len(mock_channel.frames_bytes), 1)

        # Disconnected state
        mock_channel.connected = False
        self.assertFalse(ctrl.is_connected())
        self.assertFalse(ctrl.test_send_cmd('<CMD:TEST>'))
        self.assertFalse(ctrl.test_send_fr(frame))


if __name__ == '__main__':
    main()
