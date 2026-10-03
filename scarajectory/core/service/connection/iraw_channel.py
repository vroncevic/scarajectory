# -*- coding: UTF-8 -*-

'''
Module
    iraw_channel.py
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
    Defines structural protocol IRawChannel for direct command and byte transmission.
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
class IRawChannel(Protocol):
    '''
        Structural protocol defining direct command and byte transmission contracts.

        It defines:

            :methods:
                | is_connected - Checks whether communication channel is active.
                | send_raw_command - Transmits single immediate command string.
                | send_raw_bytes - Transmits raw byte payload over active transport.
    '''

    def is_connected(self) -> bool:
        '''
            Checks whether communication channel is active.

            :return: True if channel is connected, False otherwise.
        '''

    def send_raw_command(self, cmd: str) -> None:
        '''
            Transmits single immediate command string.

            :param cmd: Raw command string to transmit.
        '''

    def send_raw_bytes(self, data: bytes) -> bool:
        '''
            Transmits raw byte payload over active transport.

            :param data: Raw byte payload.
            :return: True if transmission succeeded, False otherwise.
        '''
