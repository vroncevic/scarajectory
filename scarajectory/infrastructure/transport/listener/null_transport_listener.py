# -*- coding: UTF-8 -*-

'''
Module
    null_transport_listener.py
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
    Null Object pattern implementation for transport event listeners.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NullTransportListener:
    '''
        Null object pattern implementation for transport event listeners.

        It defines:

            :methods:
                | on_line_received - No-op handler for text line reception.
                | on_bytes_received - No-op handler for raw byte streaming.
                | on_log_emitted - No-op handler for transport logging.
    '''

    def on_line_received(self, line: str) -> None:
        '''
            No-op handler for received text line.

            :param line: Inbound line payload string.
        '''

    def on_bytes_received(self, data: bytes) -> None:
        '''
            No-op handler for received raw byte chunk.

            :param data: Inbound bytes payload.
        '''

    def on_log_emitted(self, message: str, is_tx: bool) -> None:
        '''
            No-op handler for generated transport log entry.

            :param message: Log message string.
            :param is_tx: True if transmission log, False if host/reception log.
        '''
