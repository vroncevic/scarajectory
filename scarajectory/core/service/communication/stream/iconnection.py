# -*- coding: UTF-8 -*-

'''
Module
    iconnection.py
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
    Defines structural protocol IConnection for transport lifecycle management.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.communication.stream.stream_config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IConnection(Protocol):
    '''
        Structural protocol defining transport connection lifecycle management.

        It defines:

            :methods:
                | is_connected - Checks whether transport connection is currently open.
                | connect_with_config - Opens transport connection using configuration DTO.
                | disconnect - Closes active transport connection.
    '''

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently open.

            :return: True if connected, False otherwise.
        '''

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
            Opens transport connection using configuration DTO.

            :param config: StreamConfig parameters.
            :return: True if connected successfully, False otherwise.
        '''

    def disconnect(self) -> None:
        '''
            Closes active transport connection.
        '''
