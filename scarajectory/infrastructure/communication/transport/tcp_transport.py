# -*- coding: UTF-8 -*-

'''
Module
    tcp_transport.py
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
    Thread-safe TCP socket transport implementing ITransport protocol.
'''

from __future__ import annotations

import socket
from threading import Lock, Event, Thread
from time import sleep
from typing import Callable, Final

from scarajectory.core.model.stream_config_dto import StreamConfigDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TcpTransport:
    '''
        Network TCP/IP communication transport communicating with robot controllers over sockets.

        It defines:

            :attributes:
                | _sock - Socket connection instance.
                | _lock - Mutex protecting socket TX write operations.
                | _stop_event - Event signaling reader thread termination.
                | _reader_thread - Background RX polling thread.
                | _on_line - Callback invoked when a complete line is received.
                | _on_log - Callback for communication logging.
            :methods:
                | __init__ - Initializes transport handle and sync primitives.
                | is_connected - Checks if TCP socket is connected.
                | set_callbacks - Registers packet reception and connection logging hooks.
                | connect_with_config - Connects to host:port target using StreamConfigDTO.
                | disconnect - Closes TCP connection and stops RX thread.
                | send_raw - Transmits formatted command string over socket.
    '''

    _sock: socket.socket | None
    _lock: Lock
    _stop_event: Event
    _reader_thread: Thread | None
    _on_line: Callable[[str], None] | None
    _on_log: Callable[[str, bool], None] | None

    def __init__(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str, bool], None] | None = None
    ) -> None:
        '''
            Initializes transport handle and sync primitives.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''
        self._sock = None
        self._lock: Final[Lock] = Lock()
        self._stop_event: Final[Event] = Event()
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
            :exceptions: None.
        '''
        self._on_line = on_line
        self._on_log = on_log

    def is_connected(self) -> bool:
        '''
            Checks if TCP socket is connected.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._sock is not None

    def connect_with_config(self, config: StreamConfigDTO) -> bool:
        '''
            Connects to host:port target using StreamConfigDTO.

            :param config: StreamConfigDTO containing host:port target and timeout.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()
        host: str = config.port
        port_num: int = 8080
        if ':' in config.port:
            parts = config.port.split(':', 1)
            host = parts[0]
            try:
                port_num = int(parts[1])
            except ValueError:
                port_num = 8080

        try:
            sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(config.timeout)
            sock.connect((host, port_num))
            self._sock = sock
            self._stop_event.clear()
            self._reader_thread = Thread(target=self._reader_loop, daemon=True)
            self._reader_thread.start()

            if self._on_log:
                self._on_log(f'[HOST]: Connected to TCP {host}:{port_num}', False)

            return True
        except (OSError, socket.error) as exc:
            if self._on_log:
                self._on_log(f'[ERR]: TCP Connection failed: {exc}', False)
            self.disconnect()
            return False

    def disconnect(self) -> None:
        '''
            Closes TCP connection and stops RX thread.

            :exceptions: None.
        '''
        self._stop_event.set()
        if self._sock:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
                self._sock.close()
            except (OSError, socket.error):
                pass
            self._sock = None

        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=0.2)
            self._reader_thread = None

        if self._on_log:
            self._on_log('[HOST]: Disconnected from TCP transport', False)

    def send_raw(self, cmd: str) -> bool:
        '''
            Transmits formatted command string over socket.

            :param cmd: Formatted command string.
            :return: True if written successfully, False otherwise.
            :exceptions: None.
        '''
        if not self.is_connected() or not self._sock:
            return False
        with self._lock:
            try:
                payload: bytes = f'{cmd.strip()}\n'.encode('utf-8')
                self._sock.sendall(payload)
                if self._on_log:
                    self._on_log(cmd.strip(), True)
                return True
            except (OSError, socket.error) as exc:
                if self._on_log:
                    self._on_log(f'[TX ERR]: {exc}', False)
                return False

    def _cleanup_abnormal_disconnect(self) -> None:
        '''
            Cleans up socket resources and notifies observers on abnormal network termination.

            :exceptions: None.
        '''
        if self._sock:
            try:
                self._sock.close()
            except (OSError, socket.error):
                pass
            self._sock = None
        if self._on_log:
            self._on_log('[HOST]: Connection lost (remote socket closed)', False)

    def _reader_loop(self) -> None:
        '''
            Background thread polling and assembling incoming newline-terminated lines over TCP socket.

            :exceptions: None.
        '''
        buffer: str = ''
        abnormal_disconnect: bool = False
        while not self._stop_event.is_set():
            sock = self._sock
            if not sock:
                break
            try:
                data: bytes = sock.recv(128)

                if not data:
                    abnormal_disconnect = not self._stop_event.is_set()
                    break
                buffer += data.decode('utf-8', errors='ignore')

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if line and self._on_line:
                        self._on_line(line)

            except socket.timeout:
                sleep(0.01)
            except (OSError, socket.error):
                abnormal_disconnect = not self._stop_event.is_set()
                break

        if abnormal_disconnect:
            self._cleanup_abnormal_disconnect()
