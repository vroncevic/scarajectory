# -*- coding: UTF-8 -*-

"""
Module
    flow_controller.py
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
    Sliding window flow controller managing microcontroller queue depth and synchronization barriers.
"""

from __future__ import annotations

from threading import Event
from typing import ClassVar, Final

from scarajectory.core.model.communication.stream.stream_session import StreamSession
from scarajectory.core.service.communication.protocol.iprotocol_parser import IProtocolParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowController:
    """
        Manages sliding window queue pacing, buffer occupancy, and command synchronization barriers.

        It defines:

            :attributes:
                | DEFAULT_QUEUE_CAPACITY - Default capacity of microcontroller ring buffer.
                | capacity - Maximum allowed queue depth before throttling.
                | _parser - Protocol parser decoding firmware response packets.
                | _barrier_event - Thread synchronization barrier for synchronous commands.
            :methods:
                | __init__ - Initializes flow controller with specified queue capacity and parser.
                | reset - Clears flow control state and unlocks barrier.
                | set_barrier - Locks barrier event until confirmation is received.
                | clear_barrier - Unlocks barrier event.
                | is_barrier_clear - Checks whether synchronization barrier is cleared.
                | can_send - Checks whether next packet or command is permitted to be transmitted.
                | process_response - Processes response line from firmware and updates session.
                | handle_binary_ack - Updates queue depth from firmware ACK free slot count.
                | handle_binary_move_event - Updates progress from firmware move event.
    """

    DEFAULT_QUEUE_CAPACITY: ClassVar[int] = 16
    capacity: int
    _parser: Final[IProtocolParser]
    _barrier_event: Final[Event]

    def __init__(
        self,
        *,
        capacity: int = DEFAULT_QUEUE_CAPACITY,
        parser: IProtocolParser,
    ) -> None:
        """
            Initializes flow controller with specified queue capacity and protocol parser.

            :param capacity: Microcontroller ring buffer capacity.
            :param parser: IProtocolParser instance for decoding response packets.
        """
        self.capacity = capacity
        self._parser: Final[IProtocolParser] = parser
        self._barrier_event = Event()
        self._barrier_event.set()

    def reset(self) -> None:
        """
            Clears flow control state and unlocks barrier.
        """
        self._barrier_event.set()

    def set_barrier(self) -> None:
        """
            Locks barrier event until confirmation is received.
        """
        self._barrier_event.clear()

    def clear_barrier(self) -> None:
        """
            Unlocks barrier event.
        """
        self._barrier_event.set()

    def is_barrier_clear(self) -> bool:
        """
            Checks whether synchronization barrier is cleared.

            :return: True if barrier is clear.
        """
        return self._barrier_event.is_set()

    def can_send(self, session: StreamSession, is_command: bool = False) -> bool:
        """
            Checks whether next packet or command is permitted to be transmitted.

            :param session: Active StreamSession model.
            :param is_command: True if next item is a synchronous command (default False).
            :return: True if transmission is allowed.
        """
        if not self._barrier_event.is_set():
            return False

        if is_command and session.remote_queue_depth > 0:
            return False

        return session.remote_queue_depth < self.capacity

    def process_response(self, line: str, session: StreamSession) -> tuple[bool, str | None]:
        """
            Processes response line from firmware and updates session queue depth.

            :param line: Raw response line from firmware.
            :param session: Active StreamSession instance.
            :return: Tuple of (is_fatal_error, error_message).
        """
        if self._parser.is_homing_failed(line):
            self.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            return True, f'Microcontroller Homing Failed: {line}'

        if self._parser.is_action_done(line):
            self.clear_barrier()

        q_depth: int | None = self._parser.parse_queue_depth(line)
        if q_depth is not None:
            session.remote_queue_depth = q_depth
        elif self._parser.is_buffer_full(line):
            session.remote_queue_depth = self.capacity
        elif self._parser.is_complete(line):
            session.done_count = min(len(session.waypoints), session.done_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
        elif self._parser.is_move_failed(line):
            self.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
            return False, line
        elif self._parser.is_error(line):
            self.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
            return False, line

        return False, None

    def handle_binary_ack(self, session: StreamSession, free_slots: int) -> None:
        """
            Updates queue depth from firmware ACK free slot count.

            :param session: Active StreamSession instance.
            :param free_slots: Number of free ring-buffer slots reported by MCU.
        """
        session.remote_queue_depth = max(0, self.capacity - free_slots)

    def handle_binary_move_event(self, session: StreamSession, event_type: int) -> None:
        """
            Updates progress from firmware move event.

            :param session: Active StreamSession instance.
            :param event_type: 1=START, 2=DONE, 3=FAILED.
        """
        if event_type == 2:
            session.done_count += 1
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
        elif event_type == 3:
            session.failed_count += 1
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
