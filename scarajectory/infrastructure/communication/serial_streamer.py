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

from datetime import datetime
from threading import Event, Thread
from time import time, sleep
from typing import ClassVar, Final
from collections.abc import Sequence

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.stream_config import StreamConfig
from scarajectory.core.model.stream_state import StreamState
from scarajectory.core.model.stream_progress import StreamProgress
from scarajectory.core.service.istream_observer import IStreamObserver
from scarajectory.infrastructure.communication.stream_session import StreamSession
from scarajectory.infrastructure.communication.protocol.command_formatter import CommandFormatter
from scarajectory.infrastructure.communication.protocol.protocol_parser import ProtocolParser
from scarajectory.infrastructure.communication.transport.itransport import ITransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialStreamer:
    '''
        Thread-safe background streamer transmitting waypoints to hardware over communication transport.

        It defines:

            :attributes:
                | MAX_PICO_QUEUE_CAPACITY - Maximum waypoint capacity of microcontroller ring buffer.
                | _observer - Progress callback receiver.
                | _transport - Communication transport layer instance.
                | _state - Current StreamState enum value.
                | _session - Mutable streaming session metrics.
                | _worker_thread - Background transmission worker thread.
                | _stop_event - Event signaling stream abort.
                | _pause_event - Event signaling stream pause.
                | _barrier_event - Event signaling synchronization barrier clearance.
            :methods:
                | __init__ - Initializes streamer instance with injected transport.
                | set_observer - Sets or updates progress observer.
                | is_connected - Checks whether serial port is open.
                | connect_with_config - Opens serial port using StreamConfig.
                | disconnect - Stops threads and closes serial connection.
                | send_raw_command - Sends single command packet directly.
                | start_streaming - Launches background streaming of waypoints.
                | pause_streaming - Pauses transmission.
                | resume_streaming - Resumes paused transmission.
                | stop_streaming - Aborts active stream and sends E-STOP.
    '''

    MAX_PICO_QUEUE_CAPACITY: ClassVar[int] = 16

    _observer: IStreamObserver | None
    _transport: ITransport
    _state: StreamState
    _session: StreamSession
    _worker_thread: Thread | None
    _stop_event: Event
    _pause_event: Event
    _barrier_event: Event

    def __init__(self, transport: ITransport) -> None:
        '''
            Initializes streamer instance with injected transport.

            :param transport: ITransport implementation instance.
            :exceptions: None.
        '''
        self._observer = None
        self._transport: ITransport = transport
        self._transport.set_callbacks(on_line=self._handle_serial_line, on_log=self._on_connection_log)
        self._state = StreamState.IDLE
        self._session = StreamSession()
        self._worker_thread = None
        self._stop_event: Final[Event] = Event()
        self._pause_event: Final[Event] = Event()
        self._barrier_event: Final[Event] = Event()
        self._barrier_event.set()

    def set_observer(self, observer: IStreamObserver) -> None:
        '''
            Sets or updates the progress observer.

            :param observer: IStreamObserver instance.
            :exceptions: None.
        '''
        self._observer = observer

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._transport.is_connected()

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
            Opens communication transport using StreamConfig.

            :param config: StreamConfig containing port, baudrate, and timeout.
            :return: True if connected successfully.
            :exceptions: None.
        '''
        if self.is_connected():
            self.disconnect()

        self._stop_event.clear()
        self._pause_event.clear()
        self._barrier_event.set()

        if ':' in config.port:
            from scarajectory.infrastructure.communication.transport.tcp_transport import TcpTransport
            if not isinstance(self._transport, TcpTransport):
                self._transport = TcpTransport()
                self._transport.set_callbacks(on_line=self._handle_serial_line, on_log=self._on_connection_log)
        else:
            from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport
            if not isinstance(self._transport, SerialTransport):
                self._transport = SerialTransport()
                self._transport.set_callbacks(on_line=self._handle_serial_line, on_log=self._on_connection_log)

        return self._transport.connect_with_config(config)

    def disconnect(self) -> None:
        '''
            Stops threads and closes communication transport.

            :exceptions: None.
        '''
        if self._state in (StreamState.STREAMING, StreamState.PAUSED):
            self.stop_streaming()
        self._transport.disconnect()
        self._state = StreamState.IDLE
        self._barrier_event.set()

    def send_raw_command(self, cmd: str) -> None:
        '''
            Sends single command packet directly.

            :param cmd: Formatted command string.
            :exceptions: None.
        '''
        self._transport.send_raw(cmd)

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''
            Launches background streaming of waypoints with flow control.

            :param waypoints: Sequence of waypoints to stream.
            :return: True if stream started, False otherwise.
            :exceptions: None.
        '''
        if not self.is_connected():
            if self._observer:
                self._observer.on_serial_log('[ERR]: Cannot stream - Transport not connected')
            return False

        if not waypoints:
            return False

        self._session = StreamSession(
            waypoints=list(waypoints),
            sent_count=0,
            done_count=0,
            remote_queue_depth=0,
            start_time=time()
        )
        self._state = StreamState.STREAMING
        self._pause_event.clear()
        self._stop_event.clear()
        self._barrier_event.set()

        start_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if self._observer:
            self._observer.on_serial_log(f'[{start_ts}] [STREAM TRIGGERED]: Starting execution of {len(self._session.waypoints)} waypoints...')

        self.send_raw_command(CommandFormatter.format_enable())

        self._worker_thread = Thread(target=self._stream_worker, daemon=True)
        self._worker_thread.start()
        self._notify_progress()
        return True

    def pause_streaming(self) -> None:
        '''
            Pauses transmission.

            :exceptions: None.
        '''
        if self._state == StreamState.STREAMING:
            self._state = StreamState.PAUSED
            self._pause_event.set()
            self._notify_progress()
            self.send_raw_command(CommandFormatter.format_pause())
            if self._observer:
                self._observer.on_serial_log('[HOST]: Streaming PAUSED')

    def resume_streaming(self) -> None:
        '''
            Resumes paused transmission.

            :exceptions: None.
        '''
        if self._state == StreamState.PAUSED:
            self._state = StreamState.STREAMING
            self._pause_event.clear()
            self._notify_progress()
            self.send_raw_command(CommandFormatter.format_resume())
            if self._observer:
                self._observer.on_serial_log('[HOST]: Streaming RESUMED')

    def stop_streaming(self) -> None:
        '''
            Aborts active stream and stops robot immediately.

            :exceptions: None.
        '''
        was_streaming: bool = self._state in (StreamState.STREAMING, StreamState.PAUSED)
        self._state = StreamState.STOPPED
        self._stop_event.set()
        self._pause_event.clear()
        self._barrier_event.set()
        if self.is_connected():
            self.send_raw_command(CommandFormatter.format_estop())
        self._notify_progress()
        if was_streaming and self._observer:
            self._observer.on_serial_log('[HOST]: Streaming ABORTED (E-STOP sent)')

    def _on_connection_log(self, msg: str, is_outgoing: bool) -> None:
        '''
            Forwards low-level transport messages to observer.

            :param msg: Message string.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        if self._observer:
            self._observer.on_serial_log(msg, is_outgoing=is_outgoing)

    def _notify_progress(self, error: str = '') -> None:
        '''
            Emits current streaming metrics and elapsed time to observer.

            :param error: Optional error message.
            :exceptions: None.
        '''
        if not self._observer:
            return
        elapsed: float = (time() - self._session.start_time) if (self._session.start_time > 0.0) else 0.0
        prog: StreamProgress = StreamProgress(
            state=self._state,
            total_waypoints=len(self._session.waypoints),
            sent_waypoints=self._session.sent_count,
            completed_waypoints=self._session.done_count,
            failed_waypoints=self._session.failed_count,
            error_message=error,
            elapsed_seconds=elapsed
        )
        self._observer.on_stream_progress(prog)

    def _stream_worker(self) -> None:
        '''
            Background loop sending packets as remote buffer capacity permits.

            :exceptions: None.
        '''
        session = self._session
        while not self._stop_event.is_set() and session.sent_count < len(session.waypoints):
            if self._pause_event.is_set():
                sleep(0.05)
                continue

            if not self._barrier_event.is_set():
                sleep(0.02)
                continue

            pt: Waypoint = session.waypoints[session.sent_count]
            is_cmd: bool = bool(pt.command)

            if is_cmd and session.remote_queue_depth > 0:
                sleep(0.02)
                continue

            if session.remote_queue_depth < self.MAX_PICO_QUEUE_CAPACITY:
                pkt: str = pt.command if pt.command else CommandFormatter.format_move(pt)
                if is_cmd:
                    self._barrier_event.clear()

                self.send_raw_command(pkt)
                session.sent_count += 1
                if not is_cmd:
                    session.remote_queue_depth += 1
                self._notify_progress()
                sleep(0.01)
            else:
                sleep(0.02)

        while not self._stop_event.is_set() and (session.done_count + session.failed_count) < len(session.waypoints):
            sleep(0.05)

        if not self._stop_event.is_set() and self._state != StreamState.STOPPED:
            self._state = StreamState.COMPLETED
            elapsed: float = time() - session.start_time
            end_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self._notify_progress()
            if self._observer:
                if session.failed_count > 0:
                    self._observer.on_serial_log(
                        f'[{end_ts}] [MOVE FINISHED]: {session.done_count} succeeded, {session.failed_count} failed/rejected!'
                    )
                else:
                    self._observer.on_serial_log(
                        f'[{end_ts}] [MOVE COMPLETED]: All {len(session.waypoints)} waypoints finished!'
                    )
                self._observer.on_serial_log(f'[HOST STATS]: Total Execution Time: {elapsed:.2f} s')

    def _handle_serial_line(self, line: str) -> None:
        '''
            Processes a received packet from microcontroller firmware.

            :param line: Raw line received from transport.
            :exceptions: None.
        '''
        if self._observer:
            self._observer.on_serial_log(line, is_outgoing=False)

        if ProtocolParser.is_homing_failed(line):
            self._barrier_event.set()
            self._session.failed_count = min(len(self._session.waypoints), self._session.failed_count + 1)
            self._notify_progress(error=f'Microcontroller Homing Failed: {line}')
            if self._observer:
                self._observer.on_serial_log(f'[ERR]: Robot homing failed ({line}). Aborting stream.')
            self.stop_streaming()
            return

        if ProtocolParser.is_action_done(line):
            self._barrier_event.set()

        q_depth: int | None = ProtocolParser.parse_queue_depth(line)
        if q_depth is not None:
            self._session.remote_queue_depth = q_depth
        elif ProtocolParser.is_buffer_full(line):
            self._session.remote_queue_depth = self.MAX_PICO_QUEUE_CAPACITY
        elif ProtocolParser.is_complete(line):
            self._session.done_count = min(len(self._session.waypoints), self._session.done_count + 1)
            if self._session.remote_queue_depth > 0:
                self._session.remote_queue_depth -= 1
            self._notify_progress()
        elif ProtocolParser.is_move_failed(line):
            self._barrier_event.set()
            self._session.failed_count = min(len(self._session.waypoints), self._session.failed_count + 1)
            if self._session.remote_queue_depth > 0:
                self._session.remote_queue_depth -= 1
            self._notify_progress(error=line)
        elif ProtocolParser.is_error(line):
            self._barrier_event.set()
            self._session.failed_count = min(len(self._session.waypoints), self._session.failed_count + 1)
            if self._session.remote_queue_depth > 0:
                self._session.remote_queue_depth -= 1
            self._notify_progress(error=line)
