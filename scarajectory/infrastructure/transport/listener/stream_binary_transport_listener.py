# -*- coding: UTF-8 -*-

'''
Module
    stream_binary_transport_listener.py
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
    Binary transport listener adapter routing inbound byte packets and logs to injected services.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.istream_bytes_receiver import IStreamBytesReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamBinaryTransportListener:
    '''
    Binary transport listener adapter routing inbound byte packets and logs to injected services.

    It defines:

        :attributes:
            | _bytes_receiver - Injected IStreamBytesReceiver processing raw bytes.
            | _dispatcher - Injected IStreamObserverDispatcher emitting diagnostic logs.

        :methods:
            | on_line_received - No-op for binary protocol mode.
            | on_bytes_received - Routes received raw byte payload to worker bytes receiver.
            | on_log_emitted - Routes log message to observer dispatcher.
    '''

    _bytes_receiver: IStreamBytesReceiver
    _dispatcher: IStreamObserverDispatcher

    def __init__(
        self,
        *,
        bytes_receiver: IStreamBytesReceiver,
        dispatcher: IStreamObserverDispatcher,
    ) -> None:
        '''
        Initializes StreamBinaryTransportListener with bytes receiver and dispatcher.

        :param bytes_receiver: Injected IStreamBytesReceiver instance.
        :param dispatcher: Injected IStreamObserverDispatcher instance.
        '''
        self._bytes_receiver: Final[IStreamBytesReceiver] = bytes_receiver
        self._dispatcher: Final[IStreamObserverDispatcher] = dispatcher

    def on_line_received(self, line: str) -> None:
        '''
        No-op handler for binary protocol mode.

        :param line: Inbound line payload string (ignored in binary mode).
        '''

    def on_bytes_received(self, data: bytes) -> None:
        '''
        Routes received raw byte payload to worker bytes receiver.

        :param data: Inbound bytes payload.
        '''
        self._bytes_receiver.handle_incoming_bytes(data)

    def on_log_emitted(self, message: str, is_tx: bool) -> None:
        '''
        Routes log message to observer dispatcher.

        :param message: Log message string.
        :param is_tx: True if transmission log, False if host/reception log.
        '''
        self._dispatcher.notify_log(message, is_outgoing=is_tx)
