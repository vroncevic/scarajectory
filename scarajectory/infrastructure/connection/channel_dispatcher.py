# -*- coding: UTF-8 -*-

'''
Module
    channel_dispatcher.py
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
    Dispatcher managing communication channel, frame serialization, and cyclic packet sequence counter.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.connection.iraw_channel import IRawChannel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ChannelDispatcher:
    '''
        Dispatches ASCII command strings and binary frames over communication channel.

        It defines:

            :attributes:
                | _raw_channel - Injected IRawChannel communication transport interface.
                | _frame_builder - Injected IBinaryFrameBuilder frame assembler interface.
                | _protocol_mode - Active wire protocol mode enum value.
                | _seq_num - Monotonic cyclic packet sequence counter (0 - 255).
            :methods:
                | __init__ - Initializes dispatcher with channel, builder, and protocol mode.
                | is_connected - Checks if communication transport is active.
                | next_seq - Increments and returns next cyclic sequence counter.
                | send_command - Transmits ASCII formatted command string over transport.
                | send_frame - Serializes and transmits binary frame over transport.
    '''

    _raw_channel: IRawChannel
    _frame_builder: IBinaryFrameBuilder
    _protocol_mode: ProtocolMode
    _seq_num: int

    def __init__(
        self,
        *,
        raw_channel: IRawChannel,
        frame_builder: IBinaryFrameBuilder,
        protocol_mode: ProtocolMode,
    ) -> None:
        '''
            Initializes dispatcher with transport channel, frame builder, and protocol mode.

            :param raw_channel: IRawChannel transport channel instance.
            :param frame_builder: IBinaryFrameBuilder builder instance.
            :param protocol_mode: Active ProtocolMode enum value.
        '''
        self._raw_channel: Final[IRawChannel] = raw_channel
        self._frame_builder: Final[IBinaryFrameBuilder] = frame_builder
        self._protocol_mode = protocol_mode
        self._seq_num = 0

    @property
    def protocol_mode(self) -> ProtocolMode:
        '''
            Returns active wire protocol mode.

            :return: ProtocolMode enum value.
        '''
        return self._protocol_mode

    @protocol_mode.setter
    def protocol_mode(self, mode: ProtocolMode) -> None:
        '''
            Updates active wire protocol mode dynamically.

            :param mode: ProtocolMode enum value.
        '''
        self._protocol_mode = mode

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
        '''
        return self._raw_channel.is_connected()

    def next_seq(self) -> int:
        '''
            Increments and returns next cyclic sequence counter.

            :return: Cyclic sequence counter value (0-255).
        '''
        seq: int = self._seq_num
        self._seq_num = (self._seq_num + 1) & 0xFF
        return seq

    def send_command(self, cmd: str) -> bool:
        '''
            Transmits raw command string if streamer transport is connected.

            :param cmd: Formatted command string.
            :return: True if command transmitted, False otherwise.
        '''
        if not self._raw_channel.is_connected():
            return False

        self._raw_channel.send_raw_command(cmd)
        return True

    def send_frame(self, frame: BinaryFrame) -> bool:
        '''
            Packs and transmits binary frame if streamer transport is connected.

            :param frame: BinaryFrame instance.
            :return: True if frame transmitted, False otherwise.
        '''
        if not self._raw_channel.is_connected():
            return False

        payload_bytes: bytes = self._frame_builder.pack_frame(frame=frame)
        return self._raw_channel.send_raw_bytes(payload_bytes)
