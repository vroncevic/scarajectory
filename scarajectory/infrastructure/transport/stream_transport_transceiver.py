# -*- coding: UTF-8 -*-

'''
Module
    stream_transport_transceiver.py
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
    Dedicated raw command and byte payload transceiver guarded by mutex synchronization.
'''

from __future__ import annotations

from threading import Lock
from typing import Final

from scarajectory.infrastructure.transport.driver.ichannel import IChannelDriver
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportTransceiver:
    '''
        Transceiver coordinator transmitting commands and reading raw byte streams.

        It defines:

            :attributes:
                | _driver - Injected IChannelDriver low-level I/O driver.
                | _listener - Injected ITransportListener event sink.
                | _connection - Injected IStreamTransportConnection link state inspector.
                | _lock - Mutex guarding concurrent write access to the communication channel.
            :methods:
                | __init__ - Initializes transceiver with driver, listener, and connection.
                | send_raw - Transmits command string over communication channel.
                | send_bytes - Transmits raw bytes over communication channel.
                | read_bytes - Reads raw byte chunk from communication channel.
                | channel_name - Returns readable channel endpoint descriptor name.
    '''

    _driver: IChannelDriver
    _listener: ITransportListener
    _connection: IStreamTransportConnection
    _lock: Lock

    def __init__(
        self,
        *,
        driver: IChannelDriver,
        listener: ITransportListener,
        connection: IStreamTransportConnection,
    ) -> None:
        '''
            Initializes transceiver with driver, listener, and connection state.

            :param driver: Injected IChannelDriver low-level driver instance.
            :param listener: Injected ITransportListener event sink instance.
            :param connection: Injected IStreamTransportConnection link inspector.
            :exceptions: None.
        '''
        self._driver: Final[IChannelDriver] = driver
        self._listener: Final[ITransportListener] = listener
        self._connection: Final[IStreamTransportConnection] = connection
        self._lock: Final[Lock] = Lock()

    def send_raw(self, cmd: str) -> bool:
        '''
            Transmits command string over communication channel.

            :param cmd: Formatted command payload.
            :return: True if transmission succeeded, False otherwise.
            :exceptions: None.
        '''
        if not self._connection.is_connected():
            self._listener.on_log_emitted(
                '[ERR]: Cannot send command - Not connected', False
            )
            return False

        try:
            payload: bytes = (
                cmd if cmd.endswith('\n') else f'{cmd}\n'
            ).encode('utf-8')

            with self._lock:
                self._driver.write_bytes(payload)

            self._listener.on_log_emitted(cmd.strip(), True)

            return True

        except Exception as exc:
            self._listener.on_log_emitted(f'[ERR]: Send error: {exc}', False)
            return False

    def send_bytes(self, payload: bytes) -> bool:
        '''
            Transmits raw bytes over communication channel.

            :param payload: Binary byte payload.
            :return: True if transmission succeeded, False otherwise.
            :exceptions: None.
        '''
        if not self._connection.is_connected():
            self._listener.on_log_emitted(
                '[ERR]: Cannot send binary frame - Not connected', False
            )
            return False

        try:
            with self._lock:
                self._driver.write_bytes(payload)

            return True

        except Exception as exc:
            self._listener.on_log_emitted(
                f'[ERR]: Binary send error: {exc}', False
            )
            return False

    def read_bytes(self, size: int) -> bytes:
        '''
            Reads raw byte chunk from communication channel.

            :param size: Maximum bytes to read.
            :return: Received bytes buffer.
            :exceptions: None.
        '''
        if not self._connection.is_connected():
            return b''

        return self._driver.read_bytes(size)

    def channel_name(self) -> str:
        '''
            Returns readable channel endpoint descriptor name.

            :return: Channel name string.
            :exceptions: None.
        '''
        return self._driver.channel_name()
