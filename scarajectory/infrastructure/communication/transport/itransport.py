# -*- coding: UTF-8 -*-

'''
Module
    itransport.py
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
    Interface protocol defining low-level bidirectional communication transports.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable
from collections.abc import Callable

from scarajectory.core.model.stream_config_dto import StreamConfigDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITransport(Protocol):
    '''
        Structural interface protocol for physical robot communication transports.

        It defines:

            :methods:
                | is_connected - Checks if communication link is active.
                | set_callbacks - Registers packet reception and connection logging hooks.
                | connect_with_config - Establishes communication session using configuration DTO.
                | disconnect - Terminates communication link and frees resources.
                | send_raw - Transmits command string over communication channel.
    '''

    def is_connected(self) -> bool:
        '''
            Checks if communication link is active.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''

    def set_callbacks(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None
    ) -> None:
        '''
            Registers packet reception and connection logging hooks.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''

    def connect_with_config(self, config: StreamConfigDTO) -> bool:
        '''
            Establishes communication session using configuration DTO.

            :param config: StreamConfigDTO parameter bundle.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''

    def disconnect(self) -> None:
        '''
            Terminates communication link and frees resources.

            :exceptions: None.
        '''

    def send_raw(self, cmd: str) -> bool:
        '''
            Transmits command string over communication channel.

            :param cmd: Formatted command payload.
            :return: True if transmission succeeded, False otherwise.
            :exceptions: None.
        '''
