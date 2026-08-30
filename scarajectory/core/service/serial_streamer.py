# -*- coding: UTF-8 -*-

'''
Module
    serial_streamer.py
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
    Thread-safe Hardware Serial Streamer with Sliding Window Flow Control.
'''

from __future__ import annotations

import datetime
import threading
import time
from typing import Final, override
from collections.abc import Sequence

import serial
import serial.tools.list_ports

from scarajectory.core.model.studio_waypoint import StudioWaypoint
from scarajectory.core.model.stream_config_dto import StreamConfigDTO
from scarajectory.core.model.stream_state import StreamState
from scarajectory.core.model.stream_progress import StreamProgress
from scarajectory.core.service.iserial_streamer import ISerialStreamer
from scarajectory.core.service.istream_observer import IStreamObserver

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

MAX_PICO_QUEUE_CAPACITY: Final[int] = 30


class SerialStreamer(ISerialStreamer):
    '''
        Thread-safe background streamer transmitting waypoints to hardware over USB serial.

        It defines:

            :attributes:
                | _observer - Progress callback receiver.
                | _serial - PySerial connection handle.
                | _state - Current StreamState enum value.
                | _waypoints - Active waypoints list to transmit.
                | _sent_count - Number of waypoints sent to controller.
                | _done_count - Number of waypoints confirmed completed.
                | _remote_queue_depth - Current buffer level on hardware.
                | _start_time - Timestamp when stream began.
            :methods:
                | __init__ - Initializes streamer instance.
                | set_observer - Sets or updates progress observer.
                | is_connected - Checks whether serial port is open.
                | connect_with_config - Opens serial port using StreamConfigDTO.
                | disconnect - Stops threads and closes serial connection.
                | send_raw_command - Sends single command packet directly.
                | start_streaming - Launches background streaming of waypoints.
                | pause_streaming - Pauses transmission.
                | resume_streaming - Resumes paused transmission.
                | stop_streaming - Aborts active stream and sends E-STOP.
    '''

    _observer: IStreamObserver | None
    _serial: serial.Serial | None
    _state: StreamState
    _waypoints: list[StudioWaypoint]
    _sent_count: int
    _done_count: int
    _remote_queue_depth: int
    _start_time: float
    _lock: Final[threading.Lock]
    _worker_thread: threading.Thread | None
    _reader_thread: threading.Thread | None
    _stop_event: Final[threading.Event]
    _pause_event: Final[threading.Event]

    def __init__(self, observer: IStreamObserver | None = None) -> None:
        '''
            Initializes streamer instance.

            :param observer: Optional IStreamObserver callback receiver.
            :exceptions: None.
        '''
        self._observer = observer
        self._serial = None
        self._state = StreamState.IDLE
        self._waypoints = []
        self._sent_count = 0
        self._done_count = 0
        self._remote_queue_depth = 0
        self._start_time = 0.0
        self._lock = threading.Lock()
        self._worker_thread = None
        self._reader_thread = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

    def set_observer(self, observer: IStreamObserver) -> None:
        '''
            Sets or updates the progress observer.

            :param observer: IStreamObserver instance.
            :exceptions: None.
        '''
        self._observer = observer

    @override
    def is_connected(self) -> bool:
        '''
            Checks whether serial port is currently open.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return bool(self._serial and self._serial.is_open)

    @override
    def connect_with_config(self, config: StreamConfigDTO) -> bool:
        '''
            Opens serial port using StreamConfigDTO and starts reader thread.

            :param config: StreamConfigDTO containing port, baudrate, and timeout.
            :return: True if connected successfully.
            :exceptions: None.
        '''
        self.disconnect()
        try:
            self._serial = serial.Serial(config.port, config.baudrate, timeout=config.timeout)
            self._stop_event.clear()
            self._pause_event.clear()

            self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
            self._reader_thread.start()

            if self._observer:
                self._observer.on_serial_log(f'[HOST]: Connected to {config.port} @ {config.baudrate} bps')

            self.send_raw_command('<CMD:STATUS>')
            return True

        except (OSError, serial.SerialException) as exc:
            if self._observer:
                self._observer.on_serial_log(f'[ERR]: Connection failed: {exc}')
            self.disconnect()
            return False

    @override
    def disconnect(self) -> None:
        '''
            Stops threads and closes serial connection.

            :exceptions: None.
        '''
        self.stop_streaming()
        self._stop_event.set()

        if self._serial:
            try:
                self._serial.close()
            except (OSError, serial.SerialException, TypeError, AttributeError):
                pass
            self._serial = None

        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=0.2)
            self._reader_thread = None

        if self._observer:
            self._observer.on_serial_log('[HOST]: Disconnected from serial port')

    @override
    def send_raw_command(self, cmd: str) -> None:
        '''
            Sends single command packet directly.

            :param cmd: Formatted command string.
            :exceptions: None.
        '''
        if not self.is_connected() or not self._serial:
            return
        with self._lock:
            try:
                payload: bytes = f'{cmd.strip()}\n'.encode('utf-8')
                self._serial.write(payload)
                self._serial.flush()
                if self._observer:
                    self._observer.on_serial_log(cmd.strip(), is_outgoing=True)
            except (OSError, serial.SerialException) as exc:
                if self._observer:
                    self._observer.on_serial_log(f'[TX ERR]: {exc}')

    @override
    def start_streaming(self, waypoints: Sequence[StudioWaypoint]) -> bool:
        '''
            Launches background streaming of waypoints with flow control.

            :param waypoints: Sequence of waypoints to stream.
            :return: True if stream started, False otherwise.
            :exceptions: None.
        '''
        if not self.is_connected():
            if self._observer:
                self._observer.on_serial_log('[ERR]: Cannot stream - Serial not connected')
            return False

        if not waypoints:
            return False

        self._waypoints = list(waypoints)
        self._sent_count = 0
        self._done_count = 0
        self._remote_queue_depth = 0
        self._start_time = time.time()
        self._state = StreamState.STREAMING
        self._pause_event.clear()
        self._stop_event.clear()

        start_ts: str = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if self._observer:
            self._observer.on_serial_log(f'[{start_ts}] [STREAM TRIGGERED]: Starting execution of {len(self._waypoints)} waypoints...')

        self.send_raw_command('<CMD:ENABLE>')

        self._worker_thread = threading.Thread(target=self._stream_worker, daemon=True)
        self._worker_thread.start()
        self._notify_progress()
        return True

    @override
    def pause_streaming(self) -> None:
        '''
            Pauses transmission.

            :exceptions: None.
        '''
        if self._state == StreamState.STREAMING:
            self._state = StreamState.PAUSED
            self._pause_event.set()
            self._notify_progress()
            if self._observer:
                self._observer.on_serial_log('[HOST]: Streaming PAUSED')

    @override
    def resume_streaming(self) -> None:
        '''
            Resumes paused transmission.

            :exceptions: None.
        '''
        if self._state == StreamState.PAUSED:
            self._state = StreamState.STREAMING
            self._pause_event.clear()
            self._notify_progress()
            if self._observer:
                self._observer.on_serial_log('[HOST]: Streaming RESUMED')

    @override
    def stop_streaming(self) -> None:
        '''
            Aborts active stream and stops robot immediately.

            :exceptions: None.
        '''
        self._state = StreamState.STOPPED
        self._stop_event.set()
        self._pause_event.clear()
        self.send_raw_command('<CMD:ESTOP>')
        self._notify_progress()
        if self._observer:
            self._observer.on_serial_log('[HOST]: Streaming ABORTED (E-STOP sent)')

    def _notify_progress(self, error: str = '') -> None:
        '''
            Emits current streaming metrics and elapsed time to observer.

            :param error: Optional error message.
            :exceptions: None.
        '''
        if not self._observer:
            return
        elapsed: float = (time.time() - self._start_time) if (self._start_time > 0.0) else 0.0
        prog: StreamProgress = StreamProgress(
            state=self._state,
            total_waypoints=len(self._waypoints),
            sent_waypoints=self._sent_count,
            completed_waypoints=self._done_count,
            error_message=error,
            elapsed_seconds=elapsed
        )
        self._observer.on_stream_progress(prog)

    def _stream_worker(self) -> None:
        '''
            Background loop sending packets as remote buffer capacity permits.

            :exceptions: None.
        '''
        while not self._stop_event.is_set() and self._sent_count < len(self._waypoints):
            if self._pause_event.is_set():
                time.sleep(0.05)
                continue

            if self._remote_queue_depth < MAX_PICO_QUEUE_CAPACITY:
                pt: StudioWaypoint = self._waypoints[self._sent_count]
                pkt: str = pt.to_ascii_packet()
                self.send_raw_command(pkt)
                self._sent_count += 1
                self._remote_queue_depth += 1
                self._notify_progress()
                time.sleep(0.01)
            else:
                time.sleep(0.02)

        while not self._stop_event.is_set() and self._done_count < len(self._waypoints):
            time.sleep(0.05)

        if not self._stop_event.is_set() and self._state != StreamState.STOPPED:
            self._state = StreamState.COMPLETED
            elapsed: float = time.time() - self._start_time
            end_ts: str = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self._notify_progress()
            if self._observer:
                self._observer.on_serial_log(f'[{end_ts}] [MOVE COMPLETED]: All {len(self._waypoints)} waypoints finished!')
                self._observer.on_serial_log(f'[HOST STATS]: Total Execution Time: {elapsed:.2f} s | Target Reached 🎉')

    def _reader_loop(self) -> None:
        '''
            Reads incoming serial responses and parses flow control signals.

            :exceptions: None.
        '''
        buffer: str = ''
        while not self._stop_event.is_set():
            ser = self._serial
            if not ser or not ser.is_open:
                break
            try:
                data: bytes = ser.read(64)
                if data:
                    buffer += data.decode('utf-8', errors='ignore')
                    while '\n' in buffer:
                        line: str
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if line:
                            self._handle_serial_line(line)
                else:
                    time.sleep(0.01)
            except (OSError, serial.SerialException, TypeError, AttributeError):
                break

    def _handle_serial_line(self, line: str) -> None:
        '''
            Processes a received packet from microcontroller firmware.

            :param line: Raw line received from serial.
            :exceptions: None.
        '''
        if self._observer:
            self._observer.on_serial_log(line, is_outgoing=False)

        if line.startswith('<RESP:ACK#QUEUE='):
            try:
                val: int = int(line.split('=')[1].strip('>'))
                self._remote_queue_depth = val
            except (ValueError, IndexError):
                pass

        elif line.startswith('<RESP:NACK_BUFFER_FULL>'):
            self._remote_queue_depth = MAX_PICO_QUEUE_CAPACITY

        elif line.startswith('<RESP:MOVE_DONE#'):
            self._done_count = min(len(self._waypoints), self._done_count + 1)
            if self._remote_queue_depth > 0:
                self._remote_queue_depth -= 1
            self._notify_progress()
