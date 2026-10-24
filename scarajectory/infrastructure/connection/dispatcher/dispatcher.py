# -*- coding: UTF-8 -*-

'''
Module
    dispatcher.py
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

from typing import ClassVar, Final

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ChannelDispatcher:
    '''
        Dispatches binary frames over communication channel.

        It defines:

            :attributes:
                | SEQ_NUM_MASK - Sequence counter 8-bit wrap mask (0xFF).
                | _raw_channel - Injected IRawChannel communication transport interface.
                | _frame_packer - Injected IBinaryFramePacker frame assembler interface.
                | _seq_num - Monotonic cyclic packet sequence counter (0 - 255).

            :methods:
                | __init__ - Initializes dispatcher with transport channel and frame packer.
                | is_connected - Checks if communication transport is active.
                | next_seq - Increments and returns next cyclic sequence counter.
                | send_frame - Serializes and transmits binary frame over transport.
    '''

    SEQ_NUM_MASK: ClassVar[int] = 0xFF

    _raw_channel: IRawChannel
    _frame_packer: IBinaryFramePacker
    _seq_num: int

    def __init__(
        self,
        *,
        raw_channel: IRawChannel,
        frame_packer: IBinaryFramePacker,
    ) -> None:
        '''
            Initializes dispatcher with transport channel and frame packer.

            :param raw_channel: IRawChannel transport channel instance.
            :param frame_packer: IBinaryFramePacker builder instance.
        '''
        self._raw_channel: Final[IRawChannel] = raw_channel
        self._frame_packer: Final[IBinaryFramePacker] = frame_packer
        self._seq_num = 0

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
        self._seq_num = (self._seq_num + 1) & self.SEQ_NUM_MASK

        return seq

    def send_frame(self, frame: BinaryFrame) -> bool:
        '''
            Packs and transmits binary frame if streamer transport is connected.

            :param frame: BinaryFrame instance.
            :return: True if frame transmitted, False otherwise.
        '''
        if not self._raw_channel.is_connected():
            return False

        payload_bytes: bytes = self._frame_packer.pack_frame(frame=frame)

        return self._raw_channel.send_raw_bytes(payload_bytes)
