# -*- coding: UTF-8 -*-

'''
Module
    iflow_pacing_controller.py
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
    Defines structural protocol IFlowPacingController for stream queue pacing and response handling.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.state.stream_session import StreamSession

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFlowPacingController(Protocol):
    '''
        Structural protocol defining queue pacing and response processing operations.

        It defines:

            :attributes:
                | capacity - Maximum queue capacity.

            :methods:
                | can_send - Checks whether next packet or command is permitted.
                | process_response - Processes response line from firmware.
                | handle_binary_ack - Handles binary ACK packet.
                | handle_binary_move_event - Handles binary move event packet.
    '''

    capacity: int

    def can_send(self, session: StreamSession, is_command: bool = False) -> bool:
        '''
            Checks whether next packet or command is permitted to be transmitted.

            :param session: Active stream session.
            :param is_command: True if packet represents a command, False for motion.
            :return: True if queue has space to send, False otherwise.
        '''

    def process_response(self, line: str, session: StreamSession) -> tuple[bool, str]:
        '''
            Processes response line from firmware and updates session queue depth.

            :param line: Raw response line string.
            :param session: Active stream session.
            :return: Tuple of (is_fatal_error, error_message string).
        '''

    def handle_binary_ack(self, session: StreamSession, free_slots: int) -> None:
        '''
            Handles binary ACK packet and updates session remote queue depth.

            :param session: Active stream session.
            :param free_slots: Number of available queue slots reported by firmware.
        '''

    def handle_binary_move_event(self, session: StreamSession, event_type: int) -> None:
        '''
            Handles binary move event packet and updates session counters.

            :param session: Active stream session.
            :param event_type: Binary move event identifier code.
        '''
