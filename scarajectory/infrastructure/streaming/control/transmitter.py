# -*- coding: UTF-8 -*-

'''
Module
    transmitter.py
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
    Transmits system lifecycle commands across binary wire protocol.
'''

from __future__ import annotations

from typing import Final

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlTransmitter:
    '''
    Transmits system lifecycle commands across binary wire protocol.

    It defines:

        :attributes:
            | _raw_transceiver - IRawChannel for raw transport I/O.
            | _system_builder - IBinarySystemFrameBuilder for binary system frame building.
            | _frame_packer - IBinaryFramePacker for binary frame packing.

        :methods:
            | __init__ - Initializes transmitter with raw transceiver, system builder, and frame packer.
            | send_enable - Transmits motion enable command.
            | send_hold - Transmits feed hold or pause command.
            | send_resume - Transmits motion resume command.
            | send_estop - Transmits emergency stop command.
    '''

    _raw_transceiver: IRawChannel
    _system_builder: IBinarySystemFrameBuilder
    _frame_packer: IBinaryFramePacker

    def __init__(
        self,
        *,
        raw_transceiver: IRawChannel,
        system_builder: IBinarySystemFrameBuilder,
        frame_packer: IBinaryFramePacker,
    ) -> None:
        '''
        Initializes transmitter with raw transceiver, system builder, and frame packer.

        :param raw_transceiver: IRawChannel instance.
        :param system_builder: Injected IBinarySystemFrameBuilder instance.
        :param frame_packer: Injected IBinaryFramePacker instance.
        '''
        self._raw_transceiver: Final[IRawChannel] = raw_transceiver
        self._system_builder: Final[IBinarySystemFrameBuilder] = system_builder
        self._frame_packer: Final[IBinaryFramePacker] = frame_packer

    def send_enable(self) -> None:
        '''
        Transmits motion enable command.
        '''
        frame: BinaryFrame = self._system_builder.build_system_cmd(
            msg_id=MessageId.CMD_ENABLE,
            seq_num=0,
        )
        self._raw_transceiver.send_raw_bytes(
            self._frame_packer.pack_frame(frame=frame)
        )

    def send_hold(self) -> None:
        '''
        Transmits feed hold or pause command.
        '''
        frame: BinaryFrame = self._system_builder.build_system_cmd(
            msg_id=MessageId.CMD_HOLD,
            seq_num=0,
        )
        self._raw_transceiver.send_raw_bytes(
            self._frame_packer.pack_frame(frame=frame)
        )

    def send_resume(self) -> None:
        '''
        Transmits motion resume command.
        '''
        frame: BinaryFrame = self._system_builder.build_system_cmd(
            msg_id=MessageId.CMD_RESUME,
            seq_num=0,
        )
        self._raw_transceiver.send_raw_bytes(
            self._frame_packer.pack_frame(frame=frame)
        )

    def send_estop(self) -> None:
        '''
        Transmits emergency stop command.
        '''
        frame: BinaryFrame = self._system_builder.build_system_cmd(
            msg_id=MessageId.CMD_ESTOP,
            seq_num=0,
        )
        self._raw_transceiver.send_raw_bytes(
            self._frame_packer.pack_frame(frame=frame)
        )
