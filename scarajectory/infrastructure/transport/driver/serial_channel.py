# -*- coding: UTF-8 -*-

'''
Module
    serial_channel.py
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
    Hardware serial communication channel driver interacting with UART/USB ports via PySerial.
'''

from __future__ import annotations

from serial import Serial, SerialException

from scarajectory.core.model.streaming.stream_config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialChannelDriver:
    '''
        Hardware serial channel driver communicating with microcontroller over UART/USB.

        It defines:

            :attributes:
                | _serial - PySerial connection handle or None.
            :methods:
                | __init__ - Initializes driver handle.
                | open_channel - Opens serial port with configuration.
                | close_channel - Closes active serial port connection.
                | read_bytes - Reads bytes from serial connection.
                | write_bytes - Transmits bytes to serial connection.
                | is_open - Checks whether serial port is active and open.
                | channel_name - Returns readable channel name.
    '''

    _serial: Serial | None

    def __init__(self) -> None:
        '''
            Initializes serial channel driver instance.
        '''
        self._serial = None

    def open_channel(self, config: StreamConfig) -> None:
        '''
            Opens serial port with configuration.

            :param config: StreamConfig parameters.
        '''
        self._serial = Serial(config.port, config.baudrate, timeout=config.timeout)

    def close_channel(self) -> None:
        '''
            Closes serial port connection if open.
        '''
        if self._serial:
            try:
                self._serial.close()

            except (OSError, SerialException, TypeError, AttributeError):
                pass

            self._serial = None

    def read_bytes(self, size: int) -> bytes:
        '''
            Reads bytes from serial connection.

            :param size: Number of bytes to read.
            :return: Read byte payload.
        '''
        if self._serial and self._serial.is_open:
            return self._serial.read(size)

        return b''

    def write_bytes(self, payload: bytes) -> None:
        '''
            Transmits byte payload over serial connection.

            :param payload: Bytes to write.
        '''
        if self._serial:
            self._serial.write(payload)
            self._serial.flush()

    def is_open(self) -> bool:
        '''
            Checks whether serial port is active and open.

            :return: True if serial port is open, False otherwise.
        '''
        return bool(self._serial and self._serial.is_open)

    def channel_name(self) -> str:
        '''
            Returns readable channel name.

            :return: Port name string.
        '''
        if self._serial and hasattr(self._serial, 'port'):
            return str(self._serial.port)

        return 'Serial'
