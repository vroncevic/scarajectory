# -*- coding: UTF-8 -*-

'''
Module
    ichannel.py
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
    Interface protocol for physical and network communication channel drivers.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.streaming.stream_config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IChannelDriver(Protocol):
    '''
        Structural interface protocol for low-level transport channel drivers.

        It defines:

            :methods:
                | open_channel - Opens low-level physical or network connection.
                | close_channel - Closes active connection.
                | read_bytes - Reads raw byte chunk from connection.
                | write_bytes - Transmits raw bytes over connection.
                | is_open - Checks whether connection is active.
                | channel_name - Returns readable channel endpoint descriptor.
    '''

    def open_channel(self, config: StreamConfig) -> None:
        '''
            Opens low-level physical or network connection with configuration.

            :param config: StreamConfig connection parameters.
        '''

    def close_channel(self) -> None:
        '''
            Closes active connection and frees underlying resources.
        '''

    def read_bytes(self, size: int) -> bytes:
        '''
            Reads raw byte chunk from connection.

            :param size: Maximum bytes to read.
            :return: Read bytes buffer.
        '''

    def write_bytes(self, payload: bytes) -> None:
        '''
            Transmits raw bytes over connection.

            :param payload: Byte payload to transmit.
        '''

    def is_open(self) -> bool:
        '''
            Checks whether connection is active and open.

            :return: True if open, False otherwise.
        '''

    def channel_name(self) -> str:
        '''
            Returns readable channel endpoint descriptor.

            :return: Channel name string.
        '''
