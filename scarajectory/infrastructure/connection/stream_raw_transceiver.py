# -*- coding: UTF-8 -*-

'''
Module
    stream_raw_transceiver.py
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
    Transceiver managing raw string command and byte payload transmission over transport.
'''

from __future__ import annotations

from typing import Final

from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.istream_transport_transceiver import IStreamTransportTransceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamRawTransceiver:
    '''
    Transceiver managing raw string command and byte payload transmission.

    It defines:

        :attributes:
            | _connection - Injected IStreamTransportConnection lifecycle instance.
            | _transceiver - Injected IStreamTransportTransceiver wire I/O instance.

        :methods:
            | is_connected - Checks whether transport connection is currently open.
            | send_raw_command - Transmits raw string command packet over channel.
            | send_raw_bytes - Transmits raw byte payload over active transport.
    '''

    _connection: IStreamTransportConnection
    _transceiver: IStreamTransportTransceiver

    def __init__(
        self,
        *,
        connection: IStreamTransportConnection,
        transceiver: IStreamTransportTransceiver,
    ) -> None:
        '''
        Initializes StreamRawTransceiver with connection and transceiver.

        :param connection: Injected IStreamTransportConnection instance.
        :param transceiver: Injected IStreamTransportTransceiver instance.
        :exceptions: None.
        '''
        self._connection: Final[IStreamTransportConnection] = connection
        self._transceiver: Final[IStreamTransportTransceiver] = transceiver

    def is_connected(self) -> bool:
        '''
        Checks whether transport connection is currently open.

        :return: True if transport is connected, False otherwise.
        :exceptions: None.
        '''
        return self._connection.is_connected()

    def send_raw_command(self, cmd: str) -> bool:
        '''
        Transmits raw string command packet over communication channel.

        :param cmd: Raw command string to transmit.
        :return: True if transmission succeeded, False otherwise.
        :exceptions: None.
        '''
        if not self._connection.is_connected():
            return False

        return self._transceiver.send_raw(cmd)

    def send_raw_bytes(self, data: bytes) -> bool:
        '''
        Transmits raw byte payload over active transport.

        :param data: Raw byte payload.
        :return: True if transmission succeeded, False otherwise.
        :exceptions: None.
        '''
        if not self._connection.is_connected():
            return False

        return self._transceiver.send_bytes(data)
