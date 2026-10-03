# -*- coding: UTF-8 -*-

'''
Module
    stream_connection_manager.py
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
    Dedicated connection manager handling transport lifecycle and protocol mode.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamConnectionManager:
    '''
    Dedicated connection manager handling transport lifecycle and protocol mode.

    It defines:

        :attributes:
            | _connection - Injected IStreamTransportConnection instance.
            | _protocol_mode - Active wire protocol mode enum value.

        :methods:
            | is_connected - Checks whether transport connection is currently open.
            | connect_with_config - Opens transport connection using configuration DTO.
            | disconnect - Closes active transport connection.
            | set_protocol_mode - Updates protocol mode dynamically.
    '''

    _connection: IStreamTransportConnection
    _protocol_mode: ProtocolMode

    def __init__(
        self,
        connection: IStreamTransportConnection,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> None:
        '''
        Initializes StreamConnectionManager with connection and protocol dependencies.

        :param connection: Initial IStreamTransportConnection instance.
        :param protocol_mode: Active ProtocolMode enum value.
        '''
        self._connection: Final[IStreamTransportConnection] = connection
        self._protocol_mode = protocol_mode

    def is_connected(self) -> bool:
        '''
        Checks whether transport connection is currently open.

        :return: True if transport is connected, False otherwise.
        '''
        return self._connection.is_connected()

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
        Opens transport connection using configuration DTO.

        :param config: StreamConfig parameters.
        :return: True if connected successfully, False otherwise.
        '''
        if self.is_connected():
            self.disconnect()

        self._protocol_mode = config.protocol_mode

        return self._connection.connect_with_config(config)

    def disconnect(self) -> None:
        '''
        Closes active transport connection.
        '''
        self._connection.disconnect()

    def set_protocol_mode(self, mode: ProtocolMode) -> None:
        '''
        Updates protocol mode dynamically.

        :param mode: ProtocolMode enum value.
        '''
        self._protocol_mode = mode
