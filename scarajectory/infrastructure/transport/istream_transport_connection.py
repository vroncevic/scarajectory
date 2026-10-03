# -*- coding: UTF-8 -*-

'''
Module
    istream_transport_connection.py
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
    Interface protocol defining transport connection lifecycle and event routing.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamTransportConnection(Protocol):
    '''
        Structural interface protocol for transport connection lifecycle operations.

        It defines:

            :methods:
                | is_connected - Checks if communication link is active.
                | set_listener - Updates the transport event listener.
                | connect_with_config - Opens channel and starts reader thread.
                | disconnect - Terminates reader thread and closes channel.
    '''

    def is_connected(self) -> bool:
        '''
            Checks if communication link is active.

            :return: True if connected, False otherwise.
        '''

    def set_listener(self, listener: ITransportListener) -> None:
        '''
            Updates the transport event listener.

            :param listener: ITransportListener instance.
        '''

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
            Opens channel and starts reader thread.

            :param config: StreamConfig parameter bundle.
            :return: True if connected successfully, False otherwise.
        '''

    def disconnect(self) -> None:
        '''
            Terminates reader thread and closes channel.
        '''
