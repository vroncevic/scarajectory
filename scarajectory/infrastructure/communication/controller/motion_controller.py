# -*- coding: UTF-8 -*-

'''
Module
    motion_controller.py
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
    Dedicated controller adapter for robot homing, power, and fault recovery.
'''

from __future__ import annotations

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.communication.stream.iraw_channel import IRawChannel
from scarajectory.infrastructure.communication.controller.base_sub_controller import BaseSubController
from scarajectory.infrastructure.communication.protocol.ascii.formatter.command_formatter import CommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionController(BaseSubController):
    '''
        Dedicated controller adapter for robot homing, power, and fault recovery.

        It defines:

            :methods:
                | home - Executes robot homing routine.
                | enable - Energizes joint stepper motors.
                | disable - De-energizes joint stepper motors.
                | clear_fault - Clears latched hardware fault state.
    '''

    def __init__(
        self,
        raw_channel: IRawChannel,
        frame_builder: IBinaryFrameBuilder,
        protocol_mode: ProtocolMode,
    ) -> None:
        '''
            Initializes MotionController with transport and protocol dependencies.

            :param raw_channel: IRawChannel transport instance.
            :param frame_builder: IBinaryFrameBuilder builder instance.
            :param protocol_mode: Active ProtocolMode enum value.
        '''
        super().__init__(raw_channel, frame_builder, protocol_mode)

    def home(self) -> bool:
        '''
            Executes robot homing routine.

            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_HOME,
                seq_num=self._next_seq(),
            )

            return self._send_frame(frame)

        return self._send_command(CommandFormatter.format_home())

    def enable(self) -> bool:
        '''
            Energizes joint stepper motors.

            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_ENABLE,
                seq_num=self._next_seq(),
            )

            return self._send_frame(frame)

        return self._send_command(CommandFormatter.format_enable())

    def disable(self) -> bool:
        '''
            De-energizes joint stepper motors.

            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_DISABLE,
                seq_num=self._next_seq(),
            )

            return self._send_frame(frame)

        return self._send_command(CommandFormatter.format_disable())

    def clear_fault(self) -> bool:
        '''
            Clears latched hardware fault state.

            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_CLEAR_FAULT,
                seq_num=self._next_seq(),
            )

            return self._send_frame(frame)

        return True
