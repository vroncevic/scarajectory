# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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
    Dedicated controller adapter for robot hardware telemetry and position queries.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueryController:
    '''
        Dedicated controller adapter for robot hardware telemetry and position queries.

        It defines:

            :attributes:
                | _dispatcher - Injected IChannelDispatcher communication adapter.
                | _system_builder - Injected IBinarySystemFrameBuilder frame encoder.
            :methods:
                | __init__ - Initializes QueryController with dispatcher and builder.
                | is_connected - Checks if communication transport is active.
                | query_status - Queries microcontroller runtime status.
                | query_position - Queries current end-effector position coordinates.
    '''

    _dispatcher: IChannelDispatcher
    _system_builder: IBinarySystemFrameBuilder

    def __init__(
        self,
        *,
        dispatcher: IChannelDispatcher,
        system_builder: IBinarySystemFrameBuilder,
    ) -> None:
        '''
            Initializes QueryController with dispatcher and system frame builder.

            :param dispatcher: IChannelDispatcher transport and sequence manager.
            :param system_builder: IBinarySystemFrameBuilder builder instance.
        '''
        self._dispatcher: Final[IChannelDispatcher] = dispatcher
        self._system_builder: Final[IBinarySystemFrameBuilder] = system_builder

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
        '''
        return self._dispatcher.is_connected()

    def query_status(self) -> bool:
        '''
            Queries microcontroller runtime status.

            :return: True if command transmitted successfully, False otherwise.
        '''
        frame: BinaryFrame = self._system_builder.build_system_cmd(
            msg_id=MessageId.CMD_GET_STATUS,
            seq_num=self._dispatcher.next_seq(),
        )

        return self._dispatcher.send_frame(frame)

    def query_position(self) -> bool:
        '''
            Queries current end-effector coordinates.

            :return: True if command transmitted successfully, False otherwise.
        '''
        frame: BinaryFrame = self._system_builder.build_system_cmd(
            msg_id=MessageId.CMD_GET_STEPS,
            seq_num=self._dispatcher.next_seq(),
        )

        return self._dispatcher.send_frame(frame)
