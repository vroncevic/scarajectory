# -*- coding: UTF-8 -*-

'''
Module
    tcp_transport.py
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
    Thread-safe TCP socket transport implementing ITransport protocol.
'''

from __future__ import annotations

from socket import (
    AF_INET,
    SHUT_RDWR,
    SOCK_STREAM,
    socket as Socket,
    timeout as SocketTimeout,
)
from collections.abc import Callable

from scarajectory.core.model.communication.stream_config import StreamConfig
from scarajectory.infrastructure.communication.transport.base_transport import BaseTransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TcpTransport(BaseTransport):
    '''
        Network TCP/IP communication transport communicating with robot controllers over sockets.

        It defines:

            :attributes:
                | _sock - Socket connection instance.
            :methods:
                | __init__ - Initializes transport handle and base synchronization primitives.
    '''

    _sock: Socket | None

    def __init__(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None
    ) -> None:
        '''
            Initializes transport handle and base synchronization primitives.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
        '''
        super().__init__(on_line=on_line, on_log=on_log)
        self._sock = None

    def _open_channel(self, config: StreamConfig) -> None:
        '''
            Connects TCP socket to target host:port.

            :param config: StreamConfig parameters.
        '''
        host: str = config.port
        port_num: int = 8080
        if ':' in config.port:
            parts = config.port.split(':', 1)
            host = parts[0]
            try:
                port_num = int(parts[1])
            except ValueError:
                port_num = 8080

        sock: Socket = Socket(AF_INET, SOCK_STREAM)
        timeout_val: float = config.timeout if config.timeout > 0.0 else 0.5
        sock.settimeout(timeout_val)
        sock.connect((host, port_num))
        self._sock = sock

    def _close_channel(self) -> None:
        '''
            Closes socket connection.
        '''
        if self._sock:
            try:
                self._sock.shutdown(SHUT_RDWR)
            except (OSError, AttributeError):
                pass
            try:
                self._sock.close()
            except (OSError, AttributeError):
                pass
            self._sock = None

    def _read_bytes(self, size: int) -> bytes:
        '''
            Reads bytes from TCP socket.

            :param size: Maximum bytes to read.
            :return: Read byte payload.
        '''
        if not self._sock:
            return b''
        try:
            chunk: bytes = self._sock.recv(size)

            if not chunk:
                raise ConnectionResetError('Remote peer disconnected')

            return chunk

        except SocketTimeout:
            return b''

    def _write_bytes(self, payload: bytes) -> None:
        '''
            Transmits byte payload over TCP socket.

            :param payload: Bytes to write.
        '''
        if self._sock:
            self._sock.sendall(payload)

    def _channel_is_open(self) -> bool:
        '''
            Checks if TCP socket is connected.

            :return: True if socket is active.
        '''
        return self._sock is not None

    def _channel_name(self) -> str:
        '''
            Returns descriptive name of TCP channel.

            :return: Channel name.
        '''
        return 'TCP socket'

    def _connected_log_message(self, config: StreamConfig) -> str:
        '''
            Returns formatted log message upon establishing TCP connection.

            :param config: StreamConfig parameters.
            :return: Formatted connection message.
        '''
        return f'[HOST]: Connected to {config.port} via TCP'
