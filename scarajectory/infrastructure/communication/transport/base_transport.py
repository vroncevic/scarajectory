# -*- coding: UTF-8 -*-

'''
Module
    base_transport.py
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
    Base communication transport handling thread lifecycle, synchronization, and line parsing.
'''

from __future__ import annotations

from threading import Lock, Event, Thread
from time import sleep
from typing import Final
from collections.abc import Callable

from scarajectory.core.model.communication.stream_config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BaseTransport:
    '''
        Base transport coordinating thread-safe communication, background reading, and event logging.

        It defines:

            :attributes:
                | _lock - Mutex protecting write operations.
                | _stop_event - Event signaling reader thread termination.
                | _reader_thread - Background RX polling thread.
                | _on_line - Callback invoked when a complete line is received.
                | _on_log - Callback for communication logging.
            :methods:
                | __init__ - Initializes synchronization primitives and callbacks.
                | set_callbacks - Registers packet reception and connection logging hooks.
                | is_connected - Checks if communication link is active.
                | connect_with_config - Opens channel and starts reader thread.
                | disconnect - Terminates reader thread and closes channel.
                | send_raw - Transmits command string over communication channel.
    '''

    _lock: Final[Lock]
    _stop_event: Final[Event]
    _reader_thread: Thread | None
    _on_line: Callable[[str], None] | None
    _on_log: Callable[[str, bool], None] | None

    def __init__(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None
    ) -> None:
        '''
            Initializes synchronization primitives and callbacks.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
        '''
        self._lock = Lock()
        self._stop_event = Event()
        self._reader_thread = None
        self._on_line = on_line
        self._on_log = on_log

    def set_callbacks(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None
    ) -> None:
        '''
            Registers packet reception and connection logging hooks.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
        '''
        self._on_line = on_line
        self._on_log = on_log

    def is_connected(self) -> bool:
        '''
            Checks if communication link is active.

            :return: True if connected, False otherwise.
        '''
        return self._channel_is_open()

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
            Establishes communication session using configuration DTO.

            :param config: StreamConfig parameters.
            :return: True if connected successfully, False otherwise.
        '''
        self.disconnect()
        try:
            self._open_channel(config)
            self._stop_event.clear()
            self._reader_thread = Thread(target=self._reader_loop, daemon=True)
            self._reader_thread.start()

            if self._on_log:
                self._on_log(self._connected_log_message(config), False)

            return True
        except Exception as exc:
            if self._on_log:
                self._on_log(f'[ERR]: Connection failed: {exc}', False)
            self.disconnect()
            return False

    def disconnect(self) -> None:
        '''
            Terminates communication link and frees resources.
        '''
        self._stop_event.set()
        self._close_channel()

        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=0.2)
            self._reader_thread = None

        if self._on_log:
            self._on_log(f'[HOST]: Disconnected from {self._channel_name()}', False)

    def send_raw(self, cmd: str) -> bool:
        '''
            Transmits command string over communication channel.

            :param cmd: Formatted command payload.
            :return: True if transmission succeeded, False otherwise.
        '''
        if not self.is_connected():
            return False

        with self._lock:
            try:
                payload: bytes = f'{cmd.strip()}\n'.encode('utf-8')
                self._write_bytes(payload)
                if self._on_log:
                    self._on_log(cmd.strip(), True)
                return True
            except Exception as exc:
                if self._on_log:
                    self._on_log(f'[TX ERR]: {exc}', False)
                return False

    def _reader_loop(self) -> None:
        '''
            Background thread polling and assembling incoming newline-terminated lines.
        '''
        buffer: str = ''
        abnormal_disconnect: bool = False

        while not self._stop_event.is_set():
            if not self._channel_is_open():
                break

            try:
                data: bytes = self._read_bytes(64)
                if data:
                    buffer += data.decode('utf-8', errors='ignore')
                    while '\n' in buffer:
                        line: str
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if line and self._on_line:
                            self._on_line(line)
                else:
                    sleep(0.01)
            except Exception:
                if not self._stop_event.is_set():
                    abnormal_disconnect = True
                break

        if abnormal_disconnect:
            self._close_channel()
            if self._on_log:
                self._on_log('[HOST]: Connection lost (device disconnected / unplugged)', False)

    def _open_channel(self, config: StreamConfig) -> None:
        '''
            Subclass hook to open channel.

            :param config: StreamConfig parameters.
        '''
        raise NotImplementedError

    def _close_channel(self) -> None:
        '''
            Subclass hook to close channel.
        '''
        raise NotImplementedError

    def _read_bytes(self, size: int) -> bytes:
        '''
            Subclass hook to read byte chunk.

            :param size: Maximum bytes to read.
            :return: Read bytes.
        '''
        raise NotImplementedError

    def _write_bytes(self, payload: bytes) -> None:
        '''
            Subclass hook to write byte payload.

            :param payload: Bytes to transmit.
        '''
        raise NotImplementedError

    def _channel_is_open(self) -> bool:
        '''
            Subclass hook to check if channel is open.

            :return: True if open.
        '''
        raise NotImplementedError

    def _channel_name(self) -> str:
        '''
            Returns descriptive name of communication channel.

            :return: Channel name string.
        '''
        return 'device'

    def _connected_log_message(self, config: StreamConfig) -> str:
        '''
            Returns log message upon successful connection.

            :param config: StreamConfig parameters.
            :return: Formatted log string.
        '''
        return f'[HOST]: Connected to {config.port}'
