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
    Concrete facade orchestrating transport connection, flow control, and streaming workers.
'''

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from time import time

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.message_id import MessageId
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.communication.stream.stream_config import StreamConfig
from scarajectory.core.model.communication.stream.stream_session import StreamSession
from scarajectory.core.model.communication.stream.stream_state import StreamState
from scarajectory.core.model.dsl.binary.program import Program
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.communication.stream.iexecution_worker import IExecutionWorker
from scarajectory.core.service.communication.stream.iobserver import IObserver
from scarajectory.core.service.communication.stream.session_factory import SessionFactory
from scarajectory.infrastructure.communication.controller.robot_controller import RobotController
from scarajectory.infrastructure.communication.protocol.ascii.formatter.command_formatter import CommandFormatter
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.communication.streamer.flow_controller import FlowController
from scarajectory.infrastructure.communication.streamer.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.communication.streamer.stream_observer_dispatcher import StreamObserverDispatcher
from scarajectory.infrastructure.communication.streamer.stream_state_machine import StreamStateMachine

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
    Concrete facade orchestrating transport connection, flow control, and streaming workers.

    It defines:

        :attributes:
            | _connection_manager - StreamConnectionManager handling transport lifecycle.
            | _state_machine - StreamStateMachine tracking active state transitions.
            | _dispatcher - StreamObserverDispatcher dispatching events to observers.
            | _flow_controller - FlowController managing buffer capacity and synchronization.
            | _worker - Dedicated background thread streaming packets.
            | _robot_controller - Dedicated manual actuation controller.
            | _session - Current streaming session model tracking progress.
            | _frame_builder - Injected binary frame builder interface.
            | _protocol_mode - Active wire protocol mode enum value.

        :methods:
            | is_connected - Checks whether communication channel is active.
            | connect_with_config - Opens transport connection using configuration DTO.
            | disconnect - Terminates active stream and closes transport connection.
            | send_raw_command - Transmits single immediate command string directly.
            | send_raw_bytes - Transmits raw byte payload directly over transport.
            | send_semantic_command - Transmits semantic command if connected.
            | start_streaming - Launches background streaming worker thread with waypoints.
            | stream_binary_program - Streams pre-compiled Program directly to hardware.
            | pause_streaming - Pauses background streaming transmission.
            | resume_streaming - Resumes paused background streaming transmission.
            | stop_streaming - Aborts active streaming session and triggers E-STOP.
            | set_observer - Sets or updates the streaming progress observer.
            | set_worker - Sets dedicated background execution worker.
            | set_robot_controller - Sets semantic robot controller adapter.
            | get_robot_controller - Returns dedicated RobotController instance.
            | get_connection_manager - Returns internal StreamConnectionManager instance.
            | on_connection_log - Forwards low-level transport messages to dispatcher.
            | notify_progress - Emits current streaming metrics via dispatcher.
            | on_worker_state_change - Receives state transitions from execution worker.
    '''

    _connection_manager: StreamConnectionManager
    _state_machine: StreamStateMachine
    _dispatcher: StreamObserverDispatcher
    _flow_controller: FlowController
    _worker: IExecutionWorker | None
    _robot_controller: RobotController | None
    _session: StreamSession
    _frame_builder: IBinaryFrameBuilder
    _protocol_mode: ProtocolMode

    def __init__(
        self,
        connection_manager: StreamConnectionManager,
        flow_controller: FlowController,
        state_machine: StreamStateMachine,
        dispatcher: StreamObserverDispatcher,
        worker: IExecutionWorker | None = None,
        robot_controller: RobotController | None = None,
        frame_builder: IBinaryFrameBuilder | None = None,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> None:
        '''
        Initializes TrajectoryStreamer with connection manager and collaborators.

        :param connection_manager: StreamConnectionManager instance.
        :param flow_controller: FlowController instance.
        :param state_machine: StreamStateMachine instance.
        :param dispatcher: StreamObserverDispatcher instance.
        :param worker: Optional IExecutionWorker instance.
        :param robot_controller: Optional RobotController instance.
        :param frame_builder: Optional IBinaryFrameBuilder instance.
        :param protocol_mode: Active ProtocolMode enum value.
        '''
        self._connection_manager = connection_manager
        self._flow_controller = flow_controller
        self._state_machine = state_machine
        self._dispatcher = dispatcher
        self._protocol_mode = protocol_mode
        self._frame_builder = (
            frame_builder
            if frame_builder is not None
            else BinaryFrameBuilderFactory.create()
        )
        self._session = SessionFactory.create()
        self._worker = worker
        self._robot_controller = robot_controller

        if self._worker is not None:
            self._bind_worker_callbacks()

    def _bind_worker_callbacks(self) -> None:
        '''
        Binds transport callbacks from execution worker to connection manager.
        '''
        if self._worker is None:
            return
        if self._protocol_mode == ProtocolMode.BINARY and hasattr(self._worker, 'handle_incoming_bytes'):
            self._connection_manager.bind_callbacks(
                on_bytes=getattr(self._worker, 'handle_incoming_bytes'),
                on_log=self.on_connection_log,
            )
        elif hasattr(self._worker, 'handle_incoming_line'):
            self._connection_manager.bind_callbacks(
                on_line=getattr(self._worker, 'handle_incoming_line'),
                on_log=self.on_connection_log,
            )

    def set_worker(self, worker: IExecutionWorker) -> None:
        '''
        Sets dedicated background execution worker and binds transport callbacks.

        :param worker: IExecutionWorker instance.
        '''
        self._worker = worker
        self._bind_worker_callbacks()

    def set_robot_controller(self, robot_controller: RobotController) -> None:
        '''
        Sets dedicated semantic robot controller adapter.

        :param robot_controller: RobotController instance.
        '''
        self._robot_controller = robot_controller

    def set_observer(self, observer: IObserver) -> None:
        '''
        Sets or updates the progress observer.

        :param observer: IObserver instance.
        '''
        self._dispatcher.set_observer(observer)

    def is_connected(self) -> bool:
        '''
        Checks whether communication channel is active.

        :return: True if connected, False otherwise.
        '''
        return self._connection_manager.is_connected()

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
        Opens transport connection using configuration DTO.

        :param config: StreamConfig parameters.
        :return: True if connected successfully, False otherwise.
        '''
        if self.is_connected():
            self.disconnect()

        self._flow_controller.reset()
        self._protocol_mode = config.protocol_mode
        if self._robot_controller is not None:
            self._robot_controller.set_protocol_mode(config.protocol_mode)

        self._bind_worker_callbacks()
        return self._connection_manager.connect_with_config(config)

    def disconnect(self) -> None:
        '''
        Terminates active stream and closes transport connection.
        '''
        if self._state_machine.is_active():
            self.stop_streaming()
        self._connection_manager.disconnect()
        self._state_machine.reset()
        self._flow_controller.reset()

    def send_raw_command(self, cmd: str) -> None:
        '''
        Transmits single raw command string directly.

        :param cmd: Formatted command string.
        '''
        self._connection_manager.send_raw_command(cmd)

    def send_raw_bytes(self, data: bytes) -> bool:
        '''
        Transmits raw byte payload directly over transport.

        :param data: Raw byte payload.
        :return: True if transmitted successfully, False otherwise.
        '''
        if not self.is_connected():
            self._dispatcher.notify_log(
                '[ERR]: Cannot send binary frame - Hardware offline'
            )
            return False
        return self._connection_manager.send_raw_bytes(data)

    def send_semantic_command(self, cmd: str) -> bool:
        '''
        Transmits semantic command if connected.

        :param cmd: Formatted protocol command string.
        :return: True if transmitted successfully, False otherwise.
        '''
        if not self.is_connected():
            self._dispatcher.notify_log(
                '[ERR]: Cannot send command - Hardware offline'
            )
            return False
        self.send_raw_command(cmd)
        return True

    def get_robot_controller(self) -> RobotController:
        '''
        Returns dedicated RobotController instance.

        :return: RobotController instance.
        '''
        return self._robot_controller

    def get_connection_manager(self) -> StreamConnectionManager:
        '''
        Returns internal StreamConnectionManager instance.

        :return: StreamConnectionManager instance.
        '''
        return self._connection_manager

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''
        Launches background streaming worker thread with waypoints.

        :param waypoints: Sequence of waypoints to stream.
        :return: True if streaming started, False otherwise.
        '''
        if not self.is_connected():
            self._dispatcher.notify_log(
                '[ERR]: Cannot stream - Transport not connected'
            )
            return False

        if not waypoints or self._worker is None:
            return False

        self._session = SessionFactory.create(
            waypoints=list(waypoints),
            start_time=time(),
        )
        self._state_machine.transition_to(StreamState.STREAMING)
        self._flow_controller.reset()

        start_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        self._dispatcher.notify_log(
            f'[{start_ts}] [STREAM TRIGGERED]: Starting execution of '
            f'{len(self._session.waypoints)} waypoints...'
        )

        if self._protocol_mode == ProtocolMode.BINARY:
            enable_frame: BinaryFrame = self._frame_builder.build_system_cmd(
                msg_id=MessageId.CMD_ENABLE,
                seq_num=0,
            )
            self.send_raw_bytes(self._frame_builder.pack_frame(frame=enable_frame))
        else:
            self.send_raw_command(CommandFormatter.format_enable())

        self._worker.start(session=self._session)
        self.notify_progress()
        return True

    def stream_binary_program(self, program: Program) -> bool:
        '''
        Streams pre-compiled Program directly to hardware.

        :param program: Program containing steps and raw frames.
        :return: True if streaming started, False otherwise.
        '''
        if not self.is_connected():
            self._dispatcher.notify_log(
                '[ERR]: Cannot stream - Transport not connected'
            )
            return False

        if not program.steps or self._worker is None:
            return False

        self._session = SessionFactory.create(
            waypoints=(),
            start_time=time(),
        )
        self._state_machine.transition_to(StreamState.STREAMING)
        self._flow_controller.reset()

        start_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        self._dispatcher.notify_log(
            f'[{start_ts}] [BINARY PROGRAM STREAM TRIGGERED]: Executing '
            f'{len(program.steps)} binary steps...'
        )

        enable_frame: BinaryFrame = self._frame_builder.build_system_cmd(
            msg_id=MessageId.CMD_ENABLE,
            seq_num=0,
        )
        self.send_raw_bytes(self._frame_builder.pack_frame(frame=enable_frame))

        if hasattr(self._worker, 'start_program'):
            getattr(self._worker, 'start_program')(session=self._session, program=program)
        else:
            self._worker.start(session=self._session)

        self.notify_progress()
        return True

    def pause_streaming(self) -> None:
        '''
        Pauses background streaming transmission.
        '''
        if self._state_machine.state == StreamState.STREAMING and self._worker is not None:
            self._state_machine.transition_to(StreamState.PAUSED)
            self._worker.pause()
            self.notify_progress()
            if self._protocol_mode == ProtocolMode.BINARY:
                hold_frame: BinaryFrame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_HOLD,
                    seq_num=0,
                )
                self.send_raw_bytes(self._frame_builder.pack_frame(frame=hold_frame))
            else:
                self.send_raw_command(CommandFormatter.format_pause())
            self._dispatcher.notify_log('[HOST]: Streaming PAUSED')

    def resume_streaming(self) -> None:
        '''
        Resumes paused background streaming transmission.
        '''
        if self._state_machine.state == StreamState.PAUSED and self._worker is not None:
            self._state_machine.transition_to(StreamState.STREAMING)
            self._worker.resume()
            self.notify_progress()
            if self._protocol_mode == ProtocolMode.BINARY:
                resume_frame: BinaryFrame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_RESUME,
                    seq_num=0,
                )
                self.send_raw_bytes(self._frame_builder.pack_frame(frame=resume_frame))
            else:
                self.send_raw_command(CommandFormatter.format_resume())
            self._dispatcher.notify_log('[HOST]: Streaming RESUMED')

    def stop_streaming(self) -> None:
        '''
        Aborts active streaming session and triggers E-STOP.
        '''
        was_streaming: bool = self._state_machine.is_active()
        self._state_machine.transition_to(StreamState.STOPPED)
        if self._worker is not None:
            self._worker.stop()
        if self.is_connected():
            if self._protocol_mode == ProtocolMode.BINARY:
                estop_frame: BinaryFrame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_ESTOP,
                    seq_num=0,
                )
                self.send_raw_bytes(self._frame_builder.pack_frame(frame=estop_frame))
            else:
                self.send_raw_command(CommandFormatter.format_estop())
        self.notify_progress()
        if was_streaming:
            self._dispatcher.notify_log(
                '[HOST]: Streaming ABORTED (E-STOP sent)'
            )

    def on_connection_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''
        Forwards low-level transport messages to dispatcher.

        :param msg: Message string.
        :param is_outgoing: True if transmitted command, False otherwise.
        '''
        self._dispatcher.notify_log(msg, is_outgoing=is_outgoing)

    def notify_progress(self, error: str = '') -> None:
        '''
        Emits current streaming metrics and elapsed time via dispatcher.

        :param error: Optional error message.
        '''
        self._dispatcher.notify_progress(
            state=self._state_machine.state,
            session=self._session,
            error=error,
        )

    def on_worker_state_change(self, new_state: StreamState) -> None:
        '''
        Receives state transition signals from the background execution worker.

        :param new_state: Newly transitioned StreamState enum value.
        '''
        self._state_machine.set_state(new_state)
