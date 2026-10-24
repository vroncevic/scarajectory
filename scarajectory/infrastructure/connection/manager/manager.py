# -*- coding: UTF-8 -*-

'''
Module
    manager.py
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
    Dedicated connection manager handling transport lifecycle and protocol mode.
'''

from __future__ import annotations

from typing import Final

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator

from scarajectory.core.model.streaming.config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionManager:
    '''
        Dedicated connection manager handling transport lifecycle.

        It defines:

            :attributes:
                | _connection_coordinator - Injected IConnectionCoordinator instance.

            :methods:
                | is_connected - Checks whether transport connection is currently open.
                | connect_with_config - Opens transport connection using configuration DTO.
                | disconnect - Closes active transport connection.
    '''

    _connection_coordinator: IConnectionCoordinator

    def __init__(self, connection_coordinator: IConnectionCoordinator) -> None:
        '''
            Initializes ConnectionManager with connection coordinator.

            :param connection_coordinator: Initial IConnectionCoordinator instance.
        '''
        self._connection_coordinator: Final[IConnectionCoordinator] = (
            connection_coordinator
        )

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently open.

            :return: True if transport is connected, False otherwise.
        '''
        return self._connection_coordinator.is_connected()

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
            Opens transport connection using configuration DTO.

            :param config: StreamConfig parameters.
            :return: True if connected successfully, False otherwise.
        '''
        if self.is_connected():
            self.disconnect()

        return self._connection_coordinator.connect(config.port, config.baudrate)

    def disconnect(self) -> None:
        '''
            Closes active transport connection.
        '''
        self._connection_coordinator.disconnect()
