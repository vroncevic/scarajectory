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
    Dedicated connection manager handling transport resolution, callbacks, and raw I/O.
'''

from __future__ import annotations

from collections.abc import Callable

from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.communication.stream.stream_config import StreamConfig
from scarajectory.infrastructure.communication.transport.itransport import ITransport
from scarajectory.infrastructure.communication.transport.transport_factory import TransportFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamConnectionManager:
    '''
    Dedicated connection manager handling transport resolution, callbacks, and raw I/O.

    It defines:

        :attributes:
            | _transport - Injected or resolved ITransport implementation instance.
            | _protocol_mode - Active wire protocol mode enum value.
            | _on_line - Registered handler callback for incoming text response lines.
            | _on_bytes - Registered handler callback for incoming raw byte streams.
            | _on_log - Registered handler callback for connection and debug log entries.

        :methods:
            | is_connected - Checks whether transport connection is currently open.
            | connect_with_config - Opens transport connection using configuration DTO.
            | disconnect - Closes active transport connection.
            | send_raw_command - Transmits single immediate command string directly.
            | send_raw_bytes - Transmits raw byte payload over active transport.
            | bind_callbacks - Registers or updates transport event callbacks.
            | set_protocol_mode - Updates protocol mode dynamically.
            | get_transport - Returns active ITransport instance.
    '''

    _transport: ITransport
    _protocol_mode: ProtocolMode
    _on_line: Callable[[str], None] | None
    _on_bytes: Callable[[bytes], None] | None
    _on_log: Callable[[str, bool], None] | None

    def __init__(
        self,
        transport: ITransport,
        protocol_mode: ProtocolMode,
    ) -> None:
        '''
        Initializes StreamConnectionManager with transport and protocol dependencies.

        :param transport: Initial ITransport instance.
        :param protocol_mode: Active ProtocolMode enum value.
        '''
        self._transport = transport
        self._protocol_mode = protocol_mode
        self._on_line = None
        self._on_bytes = None
        self._on_log = None

    def is_connected(self) -> bool:
        '''
        Checks whether transport connection is currently open.

        :return: True if transport is connected, False otherwise.
        '''
        return self._transport.is_connected()

    def bind_callbacks(
        self,
        *,
        on_line: Callable[[str], None] | None = None,
        on_bytes: Callable[[bytes], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None,
    ) -> None:
        '''
        Registers or updates transport event callbacks.

        :param on_line: Optional line callback.
        :param on_bytes: Optional bytes callback.
        :param on_log: Optional log callback.
        '''
        if on_line is not None:
            self._on_line = on_line
        if on_bytes is not None:
            self._on_bytes = on_bytes
        if on_log is not None:
            self._on_log = on_log

        if self._protocol_mode == ProtocolMode.BINARY and self._on_bytes is not None:
            self._transport.set_callbacks(
                on_bytes=self._on_bytes,
                on_log=self._on_log,
            )
        elif self._on_line is not None:
            self._transport.set_callbacks(
                on_line=self._on_line,
                on_log=self._on_log,
            )

    def set_protocol_mode(self, mode: ProtocolMode) -> None:
        '''
        Updates protocol mode dynamically.

        :param mode: ProtocolMode enum value.
        '''
        self._protocol_mode = mode
        self.bind_callbacks()

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
        Opens transport connection using configuration DTO.

        :param config: StreamConfig parameters.
        :return: True if connected successfully, False otherwise.
        '''
        if self.is_connected():
            self.disconnect()

        self._protocol_mode = config.protocol_mode
        resolved_transport: ITransport = TransportFactory.create_transport(config.port)
        if type(self._transport) is not type(resolved_transport):
            self._transport = resolved_transport

        self.bind_callbacks()
        return self._transport.connect_with_config(config)

    def disconnect(self) -> None:
        '''
        Closes active transport connection.
        '''
        self._transport.disconnect()

    def send_raw_command(self, cmd: str) -> None:
        '''
        Transmits single immediate command string directly.

        :param cmd: Formatted command string.
        '''
        self._transport.send_raw(cmd)

    def send_raw_bytes(self, data: bytes) -> bool:
        '''
        Transmits raw byte payload over active transport.

        :param data: Raw byte payload.
        :return: True if transmitted successfully, False otherwise.
        '''
        if not self.is_connected():
            return False
        return self._transport.send_bytes(data)

    def get_transport(self) -> ITransport:
        '''
        Returns active ITransport instance.

        :return: ITransport instance.
        '''
        return self._transport
