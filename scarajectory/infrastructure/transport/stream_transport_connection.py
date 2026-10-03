# -*- coding: UTF-8 -*-

'''
Module
    stream_transport_connection.py
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
    Dedicated connection lifecycle manager handling channel opening, closing, and reader thread.
'''

from __future__ import annotations

from threading import Event, Thread
from typing import Final

from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.driver.ichannel import IChannelDriver
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener
from scarajectory.infrastructure.transport.worker.itransport_reader_worker import ITransportReaderWorker
from scarajectory.infrastructure.transport.listener.transport_listener_holder import TransportListenerHolder
from scarajectory.infrastructure.transport.worker.transport_reader_worker_factory import TransportReaderWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportConnection:
    '''
        Connection lifecycle coordinator managing channel driver state and background reader thread.

        It defines:

            :attributes:
                | _driver - Injected IChannelDriver low-level I/O driver.
                | _listener - Injected ITransportListener event sink.
                | _worker_factory - Injected TransportReaderWorkerFactory worker creator class.
                | _stop_event - Event signaling reader thread termination.
                | _reader_thread - Thread handle running the background packet reading loop.
            :methods:
                | __init__ - Initializes connection coordinator with driver, listener, and worker factory.
                | is_connected - Checks if communication link is active.
                | set_listener - Updates the transport event listener.
                | connect_with_config - Opens channel and starts reader thread.
                | disconnect - Terminates reader thread and closes channel.
    '''

    _driver: IChannelDriver
    _listener: ITransportListener
    _worker_factory: type[TransportReaderWorkerFactory]
    _stop_event: Event
    _reader_thread: Thread

    def __init__(
        self,
        *,
        driver: IChannelDriver,
        listener: ITransportListener,
        worker_factory: type[TransportReaderWorkerFactory],
    ) -> None:
        '''
            Initializes connection coordinator with driver, listener, and worker factory.

            :param driver: Injected IChannelDriver low-level driver instance.
            :param listener: Injected ITransportListener event sink instance.
            :param worker_factory: Injected TransportReaderWorkerFactory class.
            :exceptions: None.
        '''
        self._driver: Final[IChannelDriver] = driver
        self._listener = listener
        self._worker_factory: Final[type[TransportReaderWorkerFactory]] = worker_factory
        self._stop_event: Final[Event] = Event()
        self._reader_thread: Thread = Thread(target=bool)

    def is_connected(self) -> bool:
        '''
            Checks if communication link is active.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._driver.is_open()

    def set_listener(self, listener: ITransportListener) -> None:
        '''
            Updates the transport event listener.

            :param listener: ITransportListener instance.
            :exceptions: None.
        '''
        if isinstance(self._listener, TransportListenerHolder):
            self._listener.set_listener(listener)
        else:
            self._listener = listener

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
            Opens channel and starts reader thread.

            :param config: StreamConfig parameters.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()

        try:
            self._driver.open_channel(config)
            self._stop_event.clear()
            worker: ITransportReaderWorker = self._worker_factory.create(
                stop_event=self._stop_event,
                driver=self._driver,
                listener=self._listener,
            )
            self._reader_thread = Thread(target=worker.run, daemon=True)
            self._reader_thread.start()
            self._listener.on_log_emitted(
                f'[HOST]: Connected to {self._driver.channel_name()} ({config.port})',
                False,
            )

            return True

        except Exception as exc:
            self._listener.on_log_emitted(
                f'[ERR]: Failed to connect to {config.port}: {exc}',
                False,
            )
            self._driver.close_channel()

            return False

    def disconnect(self) -> None:
        '''
            Terminates reader thread and closes channel.

            :exceptions: None.
        '''
        self._stop_event.set()

        if self._reader_thread.is_alive():
            self._reader_thread.join(timeout=1.0)

        self._reader_thread = Thread(target=bool)

        if self._driver.is_open():
            try:
                name: str = self._driver.channel_name()
                self._driver.close_channel()
                self._listener.on_log_emitted(
                    f'[HOST]: Disconnected from {name}', False
                )

            except Exception as exc:
                self._listener.on_log_emitted(
                    f'[ERR]: Error closing channel: {exc}', False
                )
