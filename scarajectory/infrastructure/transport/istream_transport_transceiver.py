# -*- coding: UTF-8 -*-

'''
Module
    istream_transport_transceiver.py
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
    Interface protocol defining low-level byte and command transceiver operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamTransportTransceiver(Protocol):
    '''
        Structural interface protocol for transport data transmission and reception operations.

        It defines:

            :methods:
                | send_raw - Transmits command string over communication channel.
                | send_bytes - Transmits raw bytes over communication channel.
                | read_bytes - Reads raw byte chunk from communication channel.
                | channel_name - Returns readable channel endpoint descriptor name.
    '''

    def send_raw(self, cmd: str) -> bool:
        '''
            Transmits command string over communication channel.

            :param cmd: Formatted command payload.
            :return: True if transmission succeeded, False otherwise.
        '''

    def send_bytes(self, payload: bytes) -> bool:
        '''
            Transmits raw bytes over communication channel.

            :param payload: Binary byte payload.
            :return: True if transmission succeeded, False otherwise.
        '''

    def read_bytes(self, size: int) -> bytes:
        '''
            Reads raw byte chunk from communication channel.

            :param size: Maximum bytes to read.
            :return: Received bytes.
        '''

    def channel_name(self) -> str:
        '''
            Returns readable channel endpoint descriptor name.

            :return: Channel name string.
        '''
