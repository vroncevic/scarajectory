# -*- coding: UTF-8 -*-

'''
Module
    serial_transport.py
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
    Thread-safe PySerial transport implementing ITransport protocol.
'''

from __future__ import annotations

from collections.abc import Callable

from serial import Serial, SerialException

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


class SerialTransport(BaseTransport):
    '''
        Hardware serial communication transport communicating with microcontroller over UART/USB.

        It defines:

            :attributes:
                | _serial - PySerial connection instance.
            :methods:
                | __init__ - Initializes transport handle and base synchronization primitives.
    '''

    _serial: Serial | None

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
        self._serial = None

    def _open_channel(self, config: StreamConfig) -> None:
        '''
            Opens serial port with configuration.

            :param config: StreamConfig parameters.
        '''
        self._serial = Serial(config.port, config.baudrate, timeout=config.timeout)

    def _close_channel(self) -> None:
        '''
            Closes serial port connection if open.
        '''
        if self._serial:
            try:
                self._serial.close()
            except (OSError, SerialException, TypeError, AttributeError):
                pass
            self._serial = None

    def _read_bytes(self, size: int) -> bytes:
        '''
            Reads bytes from serial connection.

            :param size: Number of bytes to read.
            :return: Read byte payload.
        '''
        if self._serial and self._serial.is_open:
            return self._serial.read(size)
        return b''

    def _write_bytes(self, payload: bytes) -> None:
        '''
            Transmits byte payload over serial.

            :param payload: Bytes to write.
        '''
        if self._serial and self._serial.is_open:
            self._serial.write(payload)
            self._serial.flush()

    def _channel_is_open(self) -> bool:
        '''
            Checks if serial port is open.

            :return: True if port is open.
        '''
        return bool(self._serial and self._serial.is_open)

    def _channel_name(self) -> str:
        '''
            Returns descriptive name of serial channel.

            :return: Channel name.
        '''
        return 'serial port'

    def _connected_log_message(self, config: StreamConfig) -> str:
        '''
            Returns formatted log message upon connecting to serial device.

            :param config: StreamConfig parameters.
            :return: Formatted connection message.
        '''
        return f'[HOST]: Connected to {config.port} @ {config.baudrate} bps'
