# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_loop_runner.py
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
    Executes binary transmission loops for waypoints or binary programs and handles frames.
'''

from __future__ import annotations

from datetime import datetime
from threading import Event
from time import sleep, time
from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.core.service.packet.ipacket_strategy import IPacketStrategy
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.ibyte_sender import IByteSender
from scarajectory.infrastructure.worker.binary.ibinary_stream_frame_handler import IBinaryStreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamLoopRunner:
    '''
        Executes binary transmission loops for waypoints or binary programs and handles frames.

        It defines:

            :attributes:
                | _flow_pacing - IFlowPacingController managing buffer queue.
                | _packet_strategy - IPacketStrategy encoding waypoints.
                | _frame_parser - BinaryFrameParser decoding inbound frames.
                | _frame_handler - IBinaryStreamFrameHandler handling responses.
                | _byte_sender - IByteSender transmitting raw byte stream.
                | _state_controller - IStreamStateController managing stream lifecycle.
                | _observer_dispatcher - IStreamObserverDispatcher emitting progress and logs.
                | _pacing_config - StreamPacingConfig with loop pacing delays.
            :methods:
                | __init__ - Initializes loop runner with injected collaborators.
                | run_waypoints_loop - Background loop streaming sequence of waypoints.
                | run_program_loop - Background loop streaming pre-compiled binary steps.
                | handle_incoming_bytes - Feeds raw incoming bytes and dispatches frames.
    '''

    _flow_pacing: IFlowPacingController
    _packet_strategy: IPacketStrategy
    _frame_parser: BinaryFrameParser
    _frame_handler: IBinaryStreamFrameHandler
    _byte_sender: IByteSender
    _state_controller: IStreamStateController
    _observer_dispatcher: IStreamObserverDispatcher
    _pacing_config: StreamPacingConfig

    def __init__(
        self,
        *,
        flow_pacing: IFlowPacingController,
        packet_strategy: IPacketStrategy,
        frame_parser: BinaryFrameParser,
        frame_handler: IBinaryStreamFrameHandler,
        byte_sender: IByteSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> None:
        '''
            Initializes binary stream loop runner with collaborators and configuration.

            :param flow_pacing: IFlowPacingController managing buffer queue.
            :param packet_strategy: IPacketStrategy encoding waypoints.
            :param frame_parser: BinaryFrameParser decoding inbound frames.
            :param frame_handler: IBinaryStreamFrameHandler handling responses.
            :param byte_sender: IByteSender transmitting raw byte stream.
            :param state_controller: IStreamStateController managing stream lifecycle.
            :param observer_dispatcher: IStreamObserverDispatcher emitting progress and logs.
            :param pacing_config: StreamPacingConfig with loop pacing delays.
            :exceptions: None.
        '''
        self._flow_pacing: Final[IFlowPacingController] = flow_pacing
        self._packet_strategy: Final[IPacketStrategy] = packet_strategy
        self._frame_parser: Final[BinaryFrameParser] = frame_parser
        self._frame_handler: Final[IBinaryStreamFrameHandler] = frame_handler
        self._byte_sender: Final[IByteSender] = byte_sender
        self._state_controller: Final[IStreamStateController] = state_controller
        self._observer_dispatcher: Final[IStreamObserverDispatcher] = observer_dispatcher
        self._pacing_config: Final[StreamPacingConfig] = pacing_config

    def run_waypoints_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Streams sequence of raw waypoints converted to binary frames.

            :param session: Active StreamSession tracking waypoints and progress.
            :param stop_event: Event signaling loop termination.
            :param pause_event: Event signaling transmission pause.
            :exceptions: None.
        '''
        total_pts: int = len(session.waypoints)

        while not stop_event.is_set() and session.sent_count < total_pts:
            if pause_event.is_set():
                sleep(self._pacing_config.poll_delay)
                continue

            if self._flow_pacing.can_send(session):
                pt: Waypoint = session.waypoints[session.sent_count]
                frame_bytes: bytes = self._packet_strategy.format_waypoint_packet(
                    waypoint=pt, seq_num=(session.sent_count + 1) & 0xFFFF
                )
                self._byte_sender.send_raw_bytes(frame_bytes)
                session.sent_count += 1
                session.remote_queue_depth += 1
                self._observer_dispatcher.notify_progress(
                    state=self._state_controller.state,
                    session=session,
                    error='',
                )
                sleep(self._pacing_config.send_delay)
            else:
                sleep(self._pacing_config.throttle_delay)

        while (
            not stop_event.is_set()
            and (session.done_count + session.failed_count) < total_pts
        ):
            sleep(self._pacing_config.poll_delay)

        if not stop_event.is_set():
            self._state_controller.set_state(StreamState.COMPLETED)
            elapsed: float = time() - session.start_time
            end_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self._observer_dispatcher.notify_progress(
                state=self._state_controller.state,
                session=session,
                error='',
            )
            self._observer_dispatcher.notify_log(
                f'[{end_ts}] [BINARY STREAM COMPLETED]: {session.done_count} finished, '
                f'{session.failed_count} failed in {elapsed:.2f}s',
                False,
            )

    def run_program_loop(
        self,
        *,
        session: StreamSession,
        program: BinaryProgram,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Streams pre-compiled binary steps directly to hardware.

            :param session: Active StreamSession tracking stream metrics.
            :param program: BinaryProgram containing compiled binary steps.
            :param stop_event: Event signaling loop termination.
            :param pause_event: Event signaling transmission pause.
            :exceptions: None.
        '''
        steps: tuple[Step, ...] = program.steps
        total_items: int = len(steps)

        while not stop_event.is_set() and session.sent_count < total_items:
            if pause_event.is_set():
                sleep(self._pacing_config.poll_delay)
                continue

            if self._flow_pacing.can_send(session):
                step: Step = steps[session.sent_count]
                self._byte_sender.send_raw_bytes(step.raw_bytes)
                session.sent_count += 1
                session.remote_queue_depth += 1
                self._observer_dispatcher.notify_progress(
                    state=self._state_controller.state,
                    session=session,
                    error='',
                )
                sleep(self._pacing_config.send_delay)
            else:
                sleep(self._pacing_config.throttle_delay)

        while (
            not stop_event.is_set()
            and (session.done_count + session.failed_count) < total_items
        ):
            sleep(self._pacing_config.poll_delay)

        if not stop_event.is_set():
            self._state_controller.set_state(StreamState.COMPLETED)
            elapsed: float = time() - session.start_time
            end_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self._observer_dispatcher.notify_progress(
                state=self._state_controller.state,
                session=session,
                error='',
            )
            self._observer_dispatcher.notify_log(
                f'[{end_ts}] [BINARY STREAM COMPLETED]: {session.done_count} finished, '
                f'{session.failed_count} failed in {elapsed:.2f}s',
                False,
            )

    def handle_incoming_bytes(
        self,
        *,
        data: bytes,
        session: StreamSession,
    ) -> bool:
        '''
            Feeds raw incoming bytes into parser and dispatches inbound frames.

            :param data: Byte chunk received from transport.
            :param session: Active StreamSession tracking metrics.
            :return: True if a fault occurred requiring immediate stop, False otherwise.
            :exceptions: None.
        '''
        frames: tuple[BinaryFrame, ...] = self._frame_parser.feed_bytes(data)
        should_stop: bool = False

        for frame in frames:
            if self._frame_handler.handle_frame(frame, session):
                should_stop = True

        return should_stop
