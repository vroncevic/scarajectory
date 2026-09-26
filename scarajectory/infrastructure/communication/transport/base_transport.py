# -*- coding: UTF-8 -*-

"""
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
    Thread-safe abstract base transport handling reader thread lifecycle and line buffering.
"""

from __future__ import annotations

from collections.abc import Callable
from threading import Event, Lock, Thread
from time import sleep
from typing import Final

from scarajectory.core.model.communication.stream.stream_config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BaseTransport:
    """
        Thread-safe base communication transport managing background reader thread and callback dispatch.

        It defines:

            :attributes:
                | _lock - Mutex guarding concurrent write access to the communication channel.
                | _stop_event - Event signaling reader thread termination.
                | _reader_thread - Thread handle running the background packet reading loop.
                | _on_line - Callback invoked when a complete line is received.
                | _on_log - Callback for communication logging.
                | _on_bytes - Callback for raw received byte chunks.
            :methods:
                | __init__ - Initializes synchronization primitives and callbacks.
                | set_callbacks - Registers packet reception and connection logging hooks.
                | is_connected - Checks if communication link is active.
                | connect_with_config - Opens channel and starts reader thread.
                | disconnect - Terminates reader thread and closes channel.
                | send_raw - Transmits command string over communication channel.
                | send_bytes - Transmits binary bytes over channel.
                | read_bytes - Reads raw byte chunk from channel.
    """

    _lock: Final[Lock]
    _stop_event: Final[Event]
    _reader_thread: Thread | None
    _on_line: Callable[[str], None] | None
    _on_log: Callable[[str, bool], None] | None
    _on_bytes: Callable[[bytes], None] | None

    def __init__(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None,
        on_bytes: Callable[[bytes], None] | None = None,
    ) -> None:
        """
            Initializes synchronization primitives and callbacks.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
            :param on_bytes: Optional raw byte chunk callback.
        """
        self._lock = Lock()
        self._stop_event = Event()
        self._reader_thread = None
        self._on_line = on_line
        self._on_log = on_log
        self._on_bytes = on_bytes

    def set_callbacks(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None,
        on_bytes: Callable[[bytes], None] | None = None,
    ) -> None:
        """
            Registers packet reception and connection logging hooks.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
            :param on_bytes: Optional raw bytes received callback.
        """
        self._on_line = on_line
        self._on_log = on_log
        self._on_bytes = on_bytes

    def is_connected(self) -> bool:
        """
            Checks if communication link is active.

            :return: True if connected, False otherwise.
        """
        return self._channel_is_open()

    def connect_with_config(self, config: StreamConfig) -> bool:
        """
            Establishes communication session using configuration DTO.

            :param config: StreamConfig parameters.
            :return: True if connected successfully, False otherwise.
        """
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
                self._on_log(f'[ERR]: Failed to connect to {config.port}: {exc}', False)
            self._close_channel()
            return False

    def disconnect(self) -> None:
        """
            Terminates background reader thread and closes communication channel.
        """
        self._stop_event.set()
        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=1.0)
        self._reader_thread = None

        if self._channel_is_open():
            try:
                self._close_channel()
                if self._on_log:
                    self._on_log(f'[HOST]: Disconnected from {self._channel_name()}', False)
            except Exception as exc:
                if self._on_log:
                    self._on_log(f'[ERR]: Error closing {self._channel_name()}: {exc}', False)

    def send_raw(self, cmd: str) -> bool:
        """
            Transmits command string over communication channel.

            :param cmd: Formatted command string.
            :return: True if successfully sent, False otherwise.
        """
        if not self.is_connected():
            if self._on_log:
                self._on_log('[ERR]: Cannot send command - Not connected', False)
            return False

        try:
            payload: bytes = (cmd if cmd.endswith('\n') else f'{cmd}\n').encode('utf-8')
            with self._lock:
                self._write_bytes(payload)

            if self._on_log:
                self._on_log(cmd.strip(), True)

            return True

        except Exception as exc:
            if self._on_log:
                self._on_log(f'[ERR]: Send error: {exc}', False)
            return False

    def send_bytes(self, payload: bytes) -> bool:
        """
            Transmits binary byte payload over channel.

            :param payload: Binary byte payload to write.
            :return: True if successfully transmitted, False otherwise.
        """
        if not self.is_connected():
            if self._on_log:
                self._on_log('[ERR]: Cannot send binary frame - Not connected', False)
            return False

        try:
            with self._lock:
                self._write_bytes(payload)
            return True

        except Exception as exc:
            if self._on_log:
                self._on_log(f'[ERR]: Binary send error: {exc}', False)
            return False

    def read_bytes(self, size: int) -> bytes:
        """
            Reads raw byte chunk from the channel.

            :param size: Maximum bytes to read.
            :return: Read bytes buffer.
        """
        if not self.is_connected():
            return b''
        return self._read_bytes(size)

    def _reader_loop(self) -> None:
        """
            Background thread polling and assembling incoming newline-terminated lines.
        """
        buffer: str = ''
        abnormal_disconnect: bool = False

        while not self._stop_event.is_set():
            if not self._channel_is_open():
                break

            try:
                data: bytes = self._read_bytes(64)
                if data:
                    if self._on_bytes:
                        try:
                            self._on_bytes(data)
                        except Exception as b_exc:
                            if self._on_log:
                                self._on_log(f'[ERR]: Byte callback error: {b_exc}', False)

                    if self._on_line:
                        buffer += data.decode('utf-8', errors='ignore')

                        while '\n' in buffer:
                            line: str
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()

                            if line:
                                try:
                                    self._on_line(line)
                                except Exception as cb_exc:
                                    if self._on_log:
                                        self._on_log(f'[ERR]: Packet callback error: {cb_exc}', False)
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
        raise NotImplementedError

    def _close_channel(self) -> None:
        raise NotImplementedError

    def _read_bytes(self, size: int) -> bytes:
        raise NotImplementedError

    def _write_bytes(self, payload: bytes) -> None:
        raise NotImplementedError

    def _channel_is_open(self) -> bool:
        raise NotImplementedError

    def _channel_name(self) -> str:
        raise NotImplementedError

    def _connected_log_message(self, config: StreamConfig) -> str:
        raise NotImplementedError
