# -*- coding: UTF-8 -*-

'''
Module
    itransport_listener_holder.py
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
    Interface protocol defining mutable transport listener holders.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITransportListenerHolder(Protocol):
    '''
        Structural interface protocol for mutable transport listener containers.

        It defines:

            :methods:
                | set_listener - Updates active listener target.
                | on_line_received - Dispatches text line event to active listener.
                | on_bytes_received - Dispatches raw bytes event to active listener.
                | on_log_emitted - Dispatches log event to active listener.
    '''

    def set_listener(self, listener: ITransportListener) -> None:
        '''
            Updates active listener target.

            :param listener: New ITransportListener instance.
        '''

    def on_line_received(self, line: str) -> None:
        '''
            Dispatches text line event to active listener.

            :param line: Received text line.
        '''

    def on_bytes_received(self, data: bytes) -> None:
        '''
            Dispatches raw bytes event to active listener.

            :param data: Received byte buffer.
        '''

    def on_log_emitted(self, message: str, is_sent: bool) -> None:
        '''
            Dispatches log event to active listener.

            :param message: Formatted log message text.
            :param is_sent: True if emitted after transmission, False otherwise.
        '''
