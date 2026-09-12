# -*- coding: UTF-8 -*-

'''
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
'''

from __future__ import annotations

from threading import Event
from typing import ClassVar, Final

from scarajectory.core.model.communication.stream_session import StreamSession
from scarajectory.infrastructure.communication.protocol.protocol_parser import ProtocolParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowController:
    '''
        Manages sliding window queue pacing, buffer occupancy, and command synchronization barriers.

        It defines:

            :attributes:
                | DEFAULT_QUEUE_CAPACITY - Default capacity of microcontroller ring buffer.
                | capacity - Maximum allowed queue depth before throttling.
                | _barrier_event - Thread synchronization barrier for synchronous commands.
            :methods:
                | __init__ - Initializes flow controller with specified queue capacity.
                | reset - Clears flow control state and unlocks barrier.
                | set_barrier - Locks barrier event until confirmation is received.
                | clear_barrier - Unlocks barrier event.
                | is_barrier_clear - Checks whether synchronization barrier is cleared.
                | can_send - Checks whether next packet or command is permitted to be transmitted.
                | process_response - Processes response line from firmware and updates session.
    '''

    DEFAULT_QUEUE_CAPACITY: ClassVar[int] = 16
    capacity: int
    _barrier_event: Final[Event]

    def __init__(self, capacity: int = DEFAULT_QUEUE_CAPACITY) -> None:
        '''
            Initializes flow controller with specified queue capacity.

            :param capacity: Microcontroller ring buffer capacity.
        '''
        self.capacity = capacity
        self._barrier_event = Event()
        self._barrier_event.set()

    def reset(self) -> None:
        '''
            Clears flow control state and unlocks barrier.
        '''
        self._barrier_event.set()

    def set_barrier(self) -> None:
        '''
            Locks barrier event until confirmation is received.
        '''
        self._barrier_event.clear()

    def clear_barrier(self) -> None:
        '''
            Unlocks barrier event.
        '''
        self._barrier_event.set()

    def is_barrier_clear(self) -> bool:
        '''
            Checks whether synchronization barrier is cleared.

            :return: True if barrier is clear.
        '''
        return self._barrier_event.is_set()

    def can_send(self, session: StreamSession, is_command: bool = False) -> bool:
        '''
            Checks whether next packet or command is permitted to be transmitted.

            :param session: Active StreamSession model.
            :param is_command: True if next item is a synchronous command (default False).
            :return: True if transmission is allowed.
        '''
        if not self._barrier_event.is_set():
            return False

        if is_command and session.remote_queue_depth > 0:
            return False

        return session.remote_queue_depth < self.capacity

    def process_response(self, line: str, session: StreamSession) -> tuple[bool, str | None]:
        '''
            Processes response line from firmware and updates session queue depth.

            :param line: Raw response line from firmware.
            :param session: Active StreamSession instance.
            :return: Tuple of (is_fatal_error, error_message).
        '''
        if ProtocolParser.is_homing_failed(line):
            self.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            return True, f'Microcontroller Homing Failed: {line}'

        if ProtocolParser.is_action_done(line):
            self.clear_barrier()

        q_depth: int | None = ProtocolParser.parse_queue_depth(line)
        if q_depth is not None:
            session.remote_queue_depth = q_depth
        elif ProtocolParser.is_buffer_full(line):
            session.remote_queue_depth = self.capacity
        elif ProtocolParser.is_complete(line):
            session.done_count = min(len(session.waypoints), session.done_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
        elif ProtocolParser.is_move_failed(line):
            self.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
            return False, line
        elif ProtocolParser.is_error(line):
            self.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
            return False, line

        return False, None
