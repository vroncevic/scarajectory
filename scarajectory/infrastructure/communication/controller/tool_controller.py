# -*- coding: UTF-8 -*-

'''
Module
    tool_controller.py
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
    Dedicated controller adapter for vacuum pump and purge valve actuation.
'''

from __future__ import annotations

from threading import Thread
from time import sleep

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scaralang.core.model.protocol.tool_id import ToolId
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


class ToolController(BaseSubController):
    '''
        Dedicated controller adapter for end-effector vacuum pump and purge valve actuation.

        It defines:

            :methods:
                | set_vacuum_pump - Sets end-effector vacuum pump state.
                | pulse_purge_valve - Pulses purge valve briefly to release vacuum suction.
                | set_valve - Sets purge valve state.
    '''

    def __init__(
        self,
        raw_channel: IRawChannel,
        frame_builder: IBinaryFrameBuilder,
        protocol_mode: ProtocolMode,
    ) -> None:
        '''
            Initializes ToolController with transport and protocol dependencies.

            :param raw_channel: IRawChannel transport instance.
            :param frame_builder: IBinaryFrameBuilder builder instance.
            :param protocol_mode: Active ProtocolMode enum value.
        '''
        super().__init__(raw_channel, frame_builder, protocol_mode)

    def set_vacuum_pump(self, state: bool) -> bool:
        '''
            Sets end-effector vacuum pump state.

            :param state: True for ON, False for OFF.
            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_tool_cmd(
                seq_num=self._next_seq(),
                tool_id=int(ToolId.PUMP),
                state=state,
            )
            return self._send_frame(frame)

        return self._send_command(CommandFormatter.format_pump(state))

    def pulse_purge_valve(self) -> bool:
        '''
            Pulses purge valve briefly to release vacuum suction.

            :return: True if command transmitted successfully, False otherwise.
        '''
        if not self.is_connected():
            return False

        self.set_valve(True)
        Thread(target=self._delayed_valve_off, daemon=True).start()

        return True

    def _delayed_valve_off(self) -> None:
        '''
            Internal background worker turning purge valve off after brief delay.
        '''
        sleep(0.3)

        if self.is_connected():
            self.set_valve(False)

    def set_valve(self, state: bool) -> bool:
        '''
            Sets purge valve state.

            :param state: True for open, False for closed.
            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_tool_cmd(
                seq_num=self._next_seq(),
                tool_id=int(ToolId.VALVE),
                state=state,
            )

            return self._send_frame(frame)

        return self._send_command(CommandFormatter.format_valve(state))
