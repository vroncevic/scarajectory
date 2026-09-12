# -*- coding: UTF-8 -*-

'''
Module
    trajectory_streamer.py
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
    Thread-safe Hardware Trajectory Streamer coordinating transports and execution workers.
'''

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from time import time
from typing import ClassVar, Final

from scarajectory.core.model.communication.stream_config import StreamConfig
from scarajectory.core.model.communication.stream_progress import StreamProgress
from scarajectory.core.model.communication.stream_session import StreamSession
from scarajectory.core.model.communication.stream_state import StreamState
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.communication.istream_observer import (
    IStreamObserver,
)
from scarajectory.infrastructure.communication.protocol.command_formatter import (
    CommandFormatter,
)
from scarajectory.infrastructure.communication.streamer.flow_controller import (
    FlowController,
)
from scarajectory.infrastructure.communication.streamer.robot_controller import (
    RobotController,
)
from scarajectory.infrastructure.communication.streamer.stream_execution_worker import (
    StreamExecutionWorker,
)
from scarajectory.infrastructure.communication.transport.itransport import (
    ITransport,
)
from scarajectory.infrastructure.communication.transport.transport_factory import (
    TransportFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryStreamer:
    '''
        Thread-safe background streamer coordinating hardware communication and robot actuation.

        It defines:

            :attributes:
                | MAX_PICO_QUEUE_CAPACITY - Microcontroller buffer queue capacity.
                | _observer - Progress and logging callback receiver.
                | _transport - Communication transport layer instance.
                | _state - Current streaming state enum value.
                | _session - Active streaming session metrics.
                | _flow_controller - Queue flow controller.
                | _worker - Dedicated background transmission worker.
                | _robot_controller - Dedicated manual actuation controller.
            :methods:
                | __init__ - Initializes streamer instance with transport, controller, and worker.
                | set_observer - Sets or updates progress observer.
                | is_connected - Checks whether transport connection is active.
                | connect_with_config - Opens transport connection using configuration DTO.
                | disconnect - Terminates active stream and closes transport connection.
                | send_raw_command - Transmits single raw command string directly.
                | send_semantic_command - Transmits semantic command if connected.
                | get_robot_controller - Returns the dedicated RobotController instance.
                | start_streaming - Launches background streaming worker.
                | pause_streaming - Pauses background streaming transmission.
                | resume_streaming - Resumes paused background streaming transmission.
                | stop_streaming - Aborts active streaming session and triggers E-STOP.
    '''

    MAX_PICO_QUEUE_CAPACITY: ClassVar[int] = 16

    _observer: IStreamObserver | None
    _transport: ITransport
    _state: StreamState
    _session: StreamSession
    _flow_controller: FlowController
    _worker: StreamExecutionWorker
    _robot_controller: Final[RobotController]

    def __init__(
        self,
        transport: ITransport | None = None,
        flow_controller: FlowController | None = None,
        worker: StreamExecutionWorker | None = None,
    ) -> None:
        '''
            Initializes streamer instance with transport, flow controller, and execution worker.

            :param transport: Optional ITransport implementation instance.
            :param flow_controller: Optional FlowController instance.
            :param worker: Optional StreamExecutionWorker instance.
            :exceptions: None.
        '''
        self._observer = None
        self._transport = (
            transport
            if transport is not None
            else TransportFactory.create_default_transport()
        )
        self._state = StreamState.IDLE
        self._session = StreamSession()
        self._flow_controller = (
            flow_controller
            if flow_controller is not None
            else FlowController()
        )
        self._worker = (
            worker
            if worker is not None
            else StreamExecutionWorker(
                flow_controller=self._flow_controller,
                send_command=self.send_raw_command,
                notify_progress=self._notify_progress,
                notify_log=self._on_connection_log,
                on_state_change=self._on_worker_state_change,
            )
        )
        self._transport.set_callbacks(
            on_line=self._worker.handle_incoming_line,
            on_log=self._on_connection_log,
        )
        self._robot_controller = RobotController(self)

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
            Opens transport connection using configuration DTO.

            :param config: StreamConfig parameters.
            :return: True if connected successfully.
            :exceptions: None.
        '''
        if self.is_connected():
            self.disconnect()

        self._flow_controller.reset()

        resolved_transport: ITransport = TransportFactory.create_transport(
            config.port
        )
        if type(self._transport) is not type(resolved_transport):
            self._transport = resolved_transport
            self._transport.set_callbacks(
                on_line=self._worker.handle_incoming_line,
                on_log=self._on_connection_log,
            )

        return self._transport.connect_with_config(config)

    def disconnect(self) -> None:
        '''
            Terminates active stream and closes transport connection.

            :exceptions: None.
        '''
        if self._state in (StreamState.STREAMING, StreamState.PAUSED):
            self.stop_streaming()
        self._transport.disconnect()
        self._state = StreamState.IDLE
        self._flow_controller.reset()

    def send_raw_command(self, cmd: str) -> None:
        '''
            Transmits single raw command string directly.

            :param cmd: Formatted command string.
            :exceptions: None.
        '''
        self._transport.send_raw(cmd)

    def send_semantic_command(self, cmd: str) -> bool:
        '''
            Transmits semantic command if connected.

            :param cmd: Formatted protocol command string.
            :return: True if transmitted successfully.
            :exceptions: None.
        '''
        if not self.is_connected():
            if self._observer:
                self._observer.on_serial_log(
                    '[ERR]: Cannot send command - Hardware offline'
                )
            return False
        self.send_raw_command(cmd)
        return True

    def get_robot_controller(self) -> RobotController:
        '''
            Returns the dedicated RobotController instance.

            :return: RobotController instance.
            :exceptions: None.
        '''
        return self._robot_controller

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''
            Launches background streaming worker thread.

            :param waypoints: Sequence of waypoints to stream.
            :return: True if streaming started, False otherwise.
            :exceptions: None.
        '''
        if not self.is_connected():
            if self._observer:
                self._observer.on_serial_log(
                    '[ERR]: Cannot stream - Transport not connected'
                )
            return False

        if not waypoints:
            return False

        self._session = StreamSession(
            waypoints=list(waypoints),
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=time(),
        )
        self._state = StreamState.STREAMING
        self._flow_controller.reset()

        start_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if self._observer:
            self._observer.on_serial_log(
                f'[{start_ts}] [STREAM TRIGGERED]: Starting execution of '
                f'{len(self._session.waypoints)} waypoints...'
            )

        self.send_raw_command(CommandFormatter.format_enable())
        self._worker.start(session=self._session)
        self._notify_progress()
        return True

    def pause_streaming(self) -> None:
        '''
            Pauses background streaming transmission.

            :exceptions: None.
        '''
        if self._state == StreamState.STREAMING:
            self._state = StreamState.PAUSED
            self._worker.pause()
            self._notify_progress()
            self.send_raw_command(CommandFormatter.format_pause())
            if self._observer:
                self._observer.on_serial_log('[HOST]: Streaming PAUSED')

    def resume_streaming(self) -> None:
        '''
            Resumes paused background streaming transmission.

            :exceptions: None.
        '''
        if self._state == StreamState.PAUSED:
            self._state = StreamState.STREAMING
            self._worker.resume()
            self._notify_progress()
            self.send_raw_command(CommandFormatter.format_resume())
            if self._observer:
                self._observer.on_serial_log('[HOST]: Streaming RESUMED')

    def stop_streaming(self) -> None:
        '''
            Aborts active streaming session and triggers E-STOP.

            :exceptions: None.
        '''
        was_streaming: bool = self._state in (
            StreamState.STREAMING,
            StreamState.PAUSED,
        )
        self._state = StreamState.STOPPED
        self._worker.stop()
        if self.is_connected():
            self.send_raw_command(CommandFormatter.format_estop())
        self._notify_progress()
        if was_streaming and self._observer:
            self._observer.on_serial_log(
                '[HOST]: Streaming ABORTED (E-STOP sent)'
            )

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
        elapsed: float = (
            (time() - self._session.start_time)
            if (self._session.start_time > 0.0)
            else 0.0
        )
        prog: StreamProgress = StreamProgress(
            state=self._state,
            total_waypoints=len(self._session.waypoints),
            sent_waypoints=self._session.sent_count,
            completed_waypoints=self._session.done_count,
            failed_waypoints=self._session.failed_count,
            error_message=error,
            elapsed_seconds=elapsed,
        )
        self._observer.on_stream_progress(prog)

    def _on_worker_state_change(self, new_state: StreamState) -> None:
        '''
            Receives state transition signals from the background execution worker.

            :param new_state: Newly transitioned StreamState enum value.
            :exceptions: None.
        '''
        self._state = new_state
