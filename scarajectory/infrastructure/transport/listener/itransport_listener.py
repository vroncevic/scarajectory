# -*- coding: UTF-8 -*-

'''
Module
    itransport_listener.py
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
    Structural protocol for transport event listeners.
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
class ITransportListener(Protocol):
    '''
        Structural protocol defining callbacks for inbound transport packets and logs.

        It defines:

            :methods:
                | on_line_received - Handler invoked when text line is received.
                | on_bytes_received - Handler invoked when raw byte chunk is received.
                | on_log_emitted - Handler invoked when connection or I/O log message is generated.
    '''

    def on_line_received(self, line: str) -> None:
        '''
            Handles received text response line.

            :param line: Inbound line payload string.
        '''

    def on_bytes_received(self, data: bytes) -> None:
        '''
            Handles received raw byte chunk.

            :param data: Inbound bytes payload.
        '''

    def on_log_emitted(self, message: str, is_tx: bool) -> None:
        '''
            Handles generated transport log entry.

            :param message: Log message string.
            :param is_tx: True if transmission log, False if host/reception log.
        '''
