# -*- coding: UTF-8 -*-

'''
Module
    stream_ascii_transport_listener.py
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
    ASCII transport listener adapter routing inbound text lines and logs to injected services.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.istream_line_receiver import IStreamLineReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamAsciiTransportListener:
    '''
    ASCII transport listener adapter routing inbound text lines and logs to injected services.

    It defines:

        :attributes:
            | _line_receiver - Injected IStreamLineReceiver processing response lines.
            | _dispatcher - Injected IStreamObserverDispatcher emitting diagnostic logs.

        :methods:
            | on_line_received - Routes received text response line to worker line receiver.
            | on_bytes_received - No-op for ASCII protocol mode.
            | on_log_emitted - Routes log message to observer dispatcher.
    '''

    _line_receiver: IStreamLineReceiver
    _dispatcher: IStreamObserverDispatcher

    def __init__(
        self,
        *,
        line_receiver: IStreamLineReceiver,
        dispatcher: IStreamObserverDispatcher,
    ) -> None:
        '''
        Initializes StreamAsciiTransportListener with line receiver and dispatcher.

        :param line_receiver: Injected IStreamLineReceiver instance.
        :param dispatcher: Injected IStreamObserverDispatcher instance.
        '''
        self._line_receiver: Final[IStreamLineReceiver] = line_receiver
        self._dispatcher: Final[IStreamObserverDispatcher] = dispatcher

    def on_line_received(self, line: str) -> None:
        '''
        Routes received text response line to worker line receiver.

        :param line: Received line string.
        '''
        self._line_receiver.handle_incoming_line(line)

    def on_bytes_received(self, data: bytes) -> None:
        '''
        No-op handler for ASCII protocol mode.

        :param data: Inbound bytes payload (ignored in ASCII mode).
        '''

    def on_log_emitted(self, message: str, is_tx: bool) -> None:
        '''
        Routes log message to observer dispatcher.

        :param message: Log message string.
        :param is_tx: True if transmission log, False if host/reception log.
        '''
        self._dispatcher.notify_log(message, is_outgoing=is_tx)
