# -*- coding: UTF-8 -*-

'''
Module
    jog_controller.py
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
    Dedicated controller adapter for manual robot axis jogging and feedrate override.
'''

from __future__ import annotations

from struct import pack
from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.connection.ichannel_dispatcher import IChannelDispatcher
from scarajectory.infrastructure.formatter.command_formatter import CommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogController:
    '''
        Dedicated controller adapter for manual axis jogging and feedrate override.

        It defines:

            :attributes:
                | _dispatcher - Injected IChannelDispatcher communication adapter.
                | _frame_builder - Injected IBinaryFrameBuilder frame encoder.
            :methods:
                | __init__ - Initializes JogController with dispatcher and builder.
                | is_connected - Checks if communication transport is active.
                | set_protocol_mode - Updates protocol mode dynamically.
                | jog - Jogs specific robot axis by relative displacement.
                | set_feedrate_override - Sets execution speed override percentage.
    '''

    _dispatcher: IChannelDispatcher
    _frame_builder: IBinaryFrameBuilder

    def __init__(
        self,
        *,
        dispatcher: IChannelDispatcher,
        frame_builder: IBinaryFrameBuilder,
    ) -> None:
        '''
            Initializes JogController with dispatcher and frame builder.

            :param dispatcher: IChannelDispatcher transport and sequence manager.
            :param frame_builder: IBinaryFrameBuilder builder instance.
        '''
        self._dispatcher: Final[IChannelDispatcher] = dispatcher
        self._frame_builder: Final[IBinaryFrameBuilder] = frame_builder

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
        '''
        return self._dispatcher.is_connected()

    def set_protocol_mode(self, mode: ProtocolMode) -> None:
        '''
            Updates active protocol mode dynamically.

            :param mode: ProtocolMode enum value.
        '''
        self._dispatcher.protocol_mode = mode

    def jog(self, axis: str, step: float) -> bool:
        '''
            Jogs specific robot axis by relative displacement.

            :param axis: Axis identifier string ('X', 'Y', 'Z', 'Phi', etc.).
            :param step: Relative displacement step value.
            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._dispatcher.protocol_mode == ProtocolMode.BINARY:
            joint_map: dict[str, int] = {
                'X': 0, 'J1': 0,
                'Y': 1, 'J2': 1,
                'Z': 2,
                'PHI': 3, 'J4': 3,
            }
            joint_id: int = joint_map.get(axis.upper(), 0)
            payload: bytes = pack('<BiI', joint_id, int(step), 2000)
            frame: BinaryFrame = self._frame_builder.build_frame(
                msg_id=MessageId.CMD_JOG_JOINT,
                seq_num=self._dispatcher.next_seq(),
                payload=payload,
            )

            return self._dispatcher.send_frame(frame)

        return self._dispatcher.send_command(CommandFormatter.format_jog(axis, step))

    def set_feedrate_override(self, pct: int) -> bool:
        '''
            Sets execution speed override percentage.

            :param pct: Speed override percentage between 10 and 200.
            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._dispatcher.protocol_mode == ProtocolMode.BINARY:
            payload: bytes = pack('<B', max(1, min(200, pct)))
            frame: BinaryFrame = self._frame_builder.build_frame(
                msg_id=MessageId.CMD_OVERRIDE,
                seq_num=self._dispatcher.next_seq(),
                payload=payload,
            )

            return self._dispatcher.send_frame(frame)

        return self._dispatcher.send_command(CommandFormatter.format_override(pct))
