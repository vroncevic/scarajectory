# -*- coding: UTF-8 -*-

'''
Module
    listener.py
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
    Transport listener adapter routing inbound bytes and logs to injected services.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.connection.receiver.ibytes_receiver import IStreamBytesReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportListener:
    '''
        Transport listener adapter routing inbound bytes and logs to injected services.

        It defines:

            :attributes:
                | _bytes_receiver - Injected IStreamBytesReceiver processing raw bytes.
                | _dispatcher - Injected IStreamObserverDispatcher emitting diagnostic logs.
            :methods:
                | __init__ - Initializes listener with observer dispatcher and byte receiver.
                | on_bytes_received - Routes received raw byte chunk to worker byte receiver.
                | on_log_emitted - Routes log message to observer dispatcher.
                | get_version - Returns listener version string.
    '''

    def __init__(
        self,
        *,
        dispatcher: IStreamObserverDispatcher,
        bytes_receiver: IStreamBytesReceiver,
    ) -> None:
        '''
            Initializes listener with observer dispatcher and byte receiver.

            :param dispatcher: Injected IStreamObserverDispatcher publishing logs.
            :param bytes_receiver: Injected IStreamBytesReceiver processing raw bytes.
            :exceptions: None.
        '''
        self._dispatcher: Final[IStreamObserverDispatcher] = dispatcher
        self._bytes_receiver: Final[IStreamBytesReceiver] = bytes_receiver

    def on_bytes_received(self, data: bytes) -> None:
        '''
            Routes received raw byte chunk to worker byte receiver.

            :param data: Inbound bytes payload.
            :exceptions: None.
        '''
        self._bytes_receiver.handle_incoming_bytes(data)

    def on_log_emitted(self, message: str, is_tx: bool) -> None:
        '''
            Routes log message to observer dispatcher.

            :param message: Log message string.
            :param is_tx: Transmission direction flag.
            :exceptions: None.
        '''
        self._dispatcher.notify_log(message, is_outgoing=is_tx)

    def get_version(self) -> str:
        '''
            Returns listener version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
