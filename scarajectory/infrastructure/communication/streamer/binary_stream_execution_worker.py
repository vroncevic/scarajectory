# -*- coding: UTF-8 -*-

"""
Module
    binary_stream_execution_worker.py
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
    Background worker thread executing binary packet streaming and handling inbound frames.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from threading import Event, Thread
from time import sleep, time
from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.telemetry.diagnostics_snapshot import DiagnosticsSnapshot
from scarajectory.core.model.communication.event.fault_event import FaultEvent
from scaralang.core.model.protocol.message_id import MessageId
from scarajectory.core.model.communication.event.move_event import MoveEvent
from scarajectory.core.model.communication.telemetry.scara_status import ScaraStatus
from scarajectory.core.model.communication.stream.stream_session import StreamSession
from scarajectory.core.model.communication.stream.stream_state import StreamState
from scaralang.core.model.dsl.binary.program import Program
from scaralang.core.model.dsl.binary.step import Step
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker
from scarajectory.infrastructure.communication.streamer.binary_packet_strategy import BinaryPacketStrategy
from scarajectory.infrastructure.communication.streamer.flow_controller import FlowController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamExecutionWorker:
    """
        Background worker thread executing binary packet streaming and handling inbound frames.
    """

    _flow_controller: FlowController
    _packet_strategy: Final[BinaryPacketStrategy]
    _frame_parser: Final[BinaryFrameParser]
    _send_bytes: Callable[[bytes], bool]
    _notify_progress: Callable[[str], None]
    _notify_log: Callable[[str, bool], None]
    _on_state_change: Callable[[StreamState], None]
    _send_delay: Final[float]
    _throttle_delay: Final[float]
    _poll_delay: Final[float]
    _worker_thread: Thread | None
    _stop_event: Final[Event]
    _pause_event: Final[Event]
    _session: StreamSession | None
    _program: Program | None

    def __init__(
        self,
        *,
        flow_controller: FlowController,
        packet_strategy: BinaryPacketStrategy,
        frame_parser: BinaryFrameParser,
        send_bytes: Callable[[bytes], bool],
        notify_progress: Callable[[str], None],
        notify_log: Callable[[str, bool], None],
        on_state_change: Callable[[StreamState], None],
        send_delay: float = 0.005,
        throttle_delay: float = 0.01,
        poll_delay: float = 0.02,
    ) -> None:
        """
            Initializes binary stream worker with injected collaborators and callbacks.
        """
        self._flow_controller = flow_controller
        self._packet_strategy = packet_strategy
        self._frame_parser = frame_parser
        self._send_bytes = send_bytes
        self._notify_progress = notify_progress
        self._notify_log = notify_log
        self._on_state_change = on_state_change
        self._send_delay = send_delay
        self._throttle_delay = throttle_delay
        self._poll_delay = poll_delay
        self._worker_thread = None
        self._stop_event = Event()
        self._pause_event = Event()
        self._session = None
        self._program = None

    def start(self, *, session: StreamSession) -> None:
        """
            Starts background transmission of session waypoints.

            :param session: Active StreamSession instance.
        """
        self._session = session
        self._program = None
        self._stop_event.clear()
        self._pause_event.clear()
        self._worker_thread = Thread(target=self.run_loop, daemon=True)
        self._worker_thread.start()

    def start_program(self, *, session: StreamSession, program: Program) -> None:
        """
            Starts background transmission of pre-compiled binary program.

            :param session: Active StreamSession instance.
            :param program: Pre-compiled Program instance.
        """
        self._session = session
        self._program = program
        self._stop_event.clear()
        self._pause_event.clear()
        self._worker_thread = Thread(target=self.run_loop, daemon=True)
        self._worker_thread.start()

    def pause(self) -> None:
        """
            Temporarily halts packet transmission.
        """
        self._pause_event.set()

    def resume(self) -> None:
        """
            Resumes suspended packet transmission.
        """
        self._pause_event.clear()

    def stop(self) -> None:
        """
            Aborts active transmission and resets queue flow state.
        """
        self._stop_event.set()
        self._pause_event.clear()
        if self._worker_thread is not None and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=0.2)
        self._worker_thread = None
        self._flow_controller.reset()

    def is_running(self) -> bool:
        """
            Checks whether the background worker thread is alive.

            :return: True if alive, False otherwise.
        """
        return self._worker_thread is not None and self._worker_thread.is_alive()

    def run_loop(self) -> None:
        """
            Main background execution loop transmitting binary frames.
        """
        if self._session is None:
            return

        session: StreamSession = self._session
        flow: FlowController = self._flow_controller
        total_items: int = (
            len(self._program.steps) if self._program is not None else len(session.waypoints)
        )

        while not self._stop_event.is_set() and session.sent_count < total_items:
            if self._pause_event.is_set():
                sleep(self._poll_delay)
                continue

            if flow.can_send(session):
                frame_bytes: bytes
                if self._program is not None:
                    step: Step = self._program.steps[session.sent_count]
                    frame_bytes = step.raw_bytes
                else:
                    pt: Waypoint = session.waypoints[session.sent_count]
                    frame_bytes = self._packet_strategy.format_waypoint_packet(
                        waypoint=pt,
                        seq_num=session.sent_count & 0xFF,
                    )

                self._send_bytes(frame_bytes)
                session.sent_count += 1
                session.remote_queue_depth += 1
                self._notify_progress('')
                sleep(self._send_delay)
            else:
                sleep(self._throttle_delay)

        while (
            not self._stop_event.is_set()
            and (session.done_count + session.failed_count) < total_items
        ):
            sleep(self._poll_delay)

        if not self._stop_event.is_set():
            self._on_state_change(StreamState.COMPLETED)
            elapsed: float = time() - session.start_time
            end_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self._notify_progress('')
            self._notify_log(
                f'[{end_ts}] [BINARY STREAM COMPLETED]: {session.done_count} finished, '
                f'{session.failed_count} failed in {elapsed:.2f}s',
                False,
            )

    def handle_incoming_bytes(self, data: bytes) -> None:
        """
            Feeds raw incoming bytes into parser state machine.

            :param data: Byte chunk received from transport.
        """
        frames: tuple[BinaryFrame, ...] = self._frame_parser.feed_bytes(data)
        for frame in frames:
            self.handle_frame(frame)

    def handle_frame(self, frame: BinaryFrame) -> None:
        """
            Dispatches inbound binary frame to flow controller and handlers.

            :param frame: Decoded BinaryFrame.
        """
        session: StreamSession | None = self._session
        if frame.msg_id == MessageId.RESP_ACK:
            acked_id, q_count = BinaryPayloadUnpacker.unpack_ack(frame.payload)
            if session is not None:
                self._flow_controller.handle_binary_ack(session, q_count)
        elif frame.msg_id == MessageId.RESP_NACK:
            if session is not None:
                session.failed_count += 1
                if session.remote_queue_depth > 0:
                    session.remote_queue_depth -= 1
        elif frame.msg_id == MessageId.RESP_MOVE_EVENT:
            evt: MoveEvent = BinaryPayloadUnpacker.unpack_move_event(frame.payload)
            if session is not None:
                self._flow_controller.handle_binary_move_event(session, evt.event_type)
        elif frame.msg_id == MessageId.RESP_FAULT_EVENT:
            fault: FaultEvent = BinaryPayloadUnpacker.unpack_fault_event(frame.payload)
            self._notify_log(
                f'[FIRMWARE FAULT]: code={fault.fault_code} severity={fault.severity}',
                False,
            )
            if fault.severity >= 2:
                self.stop()
                self._on_state_change(StreamState.STOPPED)
        elif frame.msg_id == MessageId.RESP_DIAGNOSTICS:
            diag: DiagnosticsSnapshot = BinaryPayloadUnpacker.unpack_diagnostics(frame.payload)
            self._notify_log(
                f'[FIRMWARE DIAG]: uptime={diag.uptime_ms}ms heap_free={diag.heap_free_bytes}B step_buf={diag.step_buffer_free}',
                False,
            )
        elif frame.msg_id == MessageId.RESP_STATUS:
            status: ScaraStatus = BinaryPayloadUnpacker.unpack_scara_status(frame.payload)
            self._notify_log(
                f'[FIRMWARE STATUS]: state={status.state} x={status.x:.2f} y={status.y:.2f} z={status.z:.2f}',
                False,
            )

