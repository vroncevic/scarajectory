# -*- coding: UTF-8 -*-

'''
Module
    istream_raw_transceiver.py
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
    Defines structural protocol IStreamRawTransceiver for raw command and byte transmission.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.service.worker.ibyte_sender import IByteSender
from scarajectory.core.service.worker.icommand_sender import ICommandSender

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamRawTransceiver(ICommandSender, IByteSender, Protocol):
    '''
    Composite structural protocol combining raw command and byte sending operations.

    It defines:

        :methods:
            | send_raw_command - Transmits raw string command packet over communication channel.
            | send_raw_bytes - Transmits raw byte sequence over active communication transport.
    '''

    def send_raw_command(self, cmd: str) -> bool:
        '''
        Transmits raw string command packet over communication channel.

        :param cmd: Raw command string to transmit.
        :return: True if transmission succeeded, False otherwise.
        '''

    def send_raw_bytes(self, data: bytes) -> bool:
        '''
        Transmits raw byte payload over active transport.

        :param data: Raw byte payload.
        :return: True if transmission succeeded, False otherwise.
        '''
