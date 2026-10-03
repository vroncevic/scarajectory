# -*- coding: UTF-8 -*-

'''
Module
    stream_control_transmitter.py
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
    Transmits system lifecycle commands across ASCII or Binary wire protocols.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.istream_raw_transceiver import IStreamRawTransceiver
from scarajectory.infrastructure.formatter.command_formatter import CommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamControlTransmitter:
    '''
    Transmits system lifecycle commands across ASCII or Binary wire protocols.

    It defines:

        :attributes:
            | _raw_transceiver - IStreamRawTransceiver for raw transport I/O.
            | _frame_builder - IBinaryFrameBuilder for binary frame packing.

        :methods:
            | send_enable - Transmits motion enable command.
            | send_hold - Transmits feed hold or pause command.
            | send_resume - Transmits motion resume command.
            | send_estop - Transmits emergency stop command.
    '''

    _raw_transceiver: IStreamRawTransceiver
    _frame_builder: IBinaryFrameBuilder

    def __init__(
        self,
        *,
        raw_transceiver: IStreamRawTransceiver,
        frame_builder: IBinaryFrameBuilder,
    ) -> None:
        '''
        Initializes transmitter with raw transceiver and frame builder.

        :param raw_transceiver: IStreamRawTransceiver instance.
        :param frame_builder: Injected IBinaryFrameBuilder instance.
        '''
        self._raw_transceiver: Final[IStreamRawTransceiver] = raw_transceiver
        self._frame_builder: Final[IBinaryFrameBuilder] = frame_builder

    def send_enable(self, mode: ProtocolMode) -> None:
        '''
        Transmits motion enable command according to active protocol mode.

        :param mode: Active ProtocolMode enum value.
        '''
        if mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_ENABLE,
                seq_num=0,
            )
            self._raw_transceiver.send_raw_bytes(
                self._frame_builder.pack_frame(frame=frame)
            )
        else:
            self._raw_transceiver.send_raw_command(CommandFormatter.format_enable())

    def send_hold(self, mode: ProtocolMode) -> None:
        '''
        Transmits feed hold or pause command according to active protocol mode.

        :param mode: Active ProtocolMode enum value.
        '''
        if mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_HOLD,
                seq_num=0,
            )
            self._raw_transceiver.send_raw_bytes(
                self._frame_builder.pack_frame(frame=frame)
            )
        else:
            self._raw_transceiver.send_raw_command(CommandFormatter.format_pause())

    def send_resume(self, mode: ProtocolMode) -> None:
        '''
        Transmits motion resume command according to active protocol mode.

        :param mode: Active ProtocolMode enum value.
        '''
        if mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_RESUME,
                seq_num=0,
            )
            self._raw_transceiver.send_raw_bytes(
                self._frame_builder.pack_frame(frame=frame)
            )
        else:
            self._raw_transceiver.send_raw_command(CommandFormatter.format_resume())

    def send_estop(self, mode: ProtocolMode) -> None:
        '''
        Transmits emergency stop command according to active protocol mode.

        :param mode: Active ProtocolMode enum value.
        '''
        if mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_ESTOP,
                seq_num=0,
            )
            self._raw_transceiver.send_raw_bytes(
                self._frame_builder.pack_frame(frame=frame)
            )
        else:
            self._raw_transceiver.send_raw_command(CommandFormatter.format_estop())
