# -*- coding: UTF-8 -*-

'''
Module
    flow_pacing_controller.py
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
    Manages microcontroller queue pacing, window occupancy, and response decoding.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.pacing.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.classifier.status.iflow_status_classifier import IFlowStatusClassifier
from scarajectory.infrastructure.classifier.status.ihoming_status_classifier import IHomingStatusClassifier
from scarajectory.infrastructure.classifier.status.imotion_status_classifier import IMotionStatusClassifier
from scarajectory.infrastructure.classifier.iresponse_parser import IResponseParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowPacingController:
    '''
        Manages microcontroller queue pacing, window occupancy, and response decoding.

        It defines:

            :attributes:
                | capacity - Maximum allowed queue depth before throttling.
                | _response_parser - Response decoder extracting queue depth metrics.
                | _flow_classifier - Classifier detecting buffer saturation and channel faults.
                | _motion_classifier - Classifier tracking waypoint moves and action completions.
                | _homing_classifier - Classifier verifying homing routine lifecycle events.
                | _barrier_coordinator - Injected IFlowBarrierCoordinator managing gating.
            :methods:
                | __init__ - Initializes pacing controller with capacity and classifiers.
                | can_send - Checks whether next packet or command is permitted to be transmitted.
                | process_response - Processes response line from firmware and updates session.
                | handle_binary_ack - Updates queue depth from firmware ACK free slot count.
                | handle_binary_move_event - Updates progress from firmware move event.
    '''

    capacity: int
    _response_parser: IResponseParser
    _flow_classifier: IFlowStatusClassifier
    _motion_classifier: IMotionStatusClassifier
    _homing_classifier: IHomingStatusClassifier
    _barrier_coordinator: IFlowBarrierCoordinator

    def __init__(
        self,
        *,
        capacity: int,
        response_parser: IResponseParser,
        flow_classifier: IFlowStatusClassifier,
        motion_classifier: IMotionStatusClassifier,
        homing_classifier: IHomingStatusClassifier,
        barrier_coordinator: IFlowBarrierCoordinator,
    ) -> None:
        '''
            Initializes flow pacing controller with specified queue capacity and classifiers.

            :param capacity: Microcontroller ring buffer capacity.
            :param response_parser: IResponseParser instance for queue depth decoding.
            :param flow_classifier: IFlowStatusClassifier instance for buffer/error tracking.
            :param motion_classifier: IMotionStatusClassifier instance for move/action tracking.
            :param homing_classifier: IHomingStatusClassifier instance for homing events.
            :param barrier_coordinator: IFlowBarrierCoordinator instance for barrier gating.
            :exceptions: None.
        '''
        self.capacity: Final[int] = capacity
        self._response_parser: Final[IResponseParser] = response_parser
        self._flow_classifier: Final[IFlowStatusClassifier] = flow_classifier
        self._motion_classifier: Final[IMotionStatusClassifier] = motion_classifier
        self._homing_classifier: Final[IHomingStatusClassifier] = homing_classifier
        self._barrier_coordinator: Final[IFlowBarrierCoordinator] = barrier_coordinator

    def can_send(self, session: StreamSession, is_command: bool = False) -> bool:
        '''
            Checks whether next packet or command is permitted to be transmitted.

            :param session: Active StreamSession model.
            :param is_command: True if next item is a synchronous command (default False).
            :return: True if transmission is allowed, False otherwise.
            :exceptions: None.
        '''
        if not self._barrier_coordinator.is_barrier_clear():
            return False

        if is_command and session.remote_queue_depth > 0:
            return False

        return session.remote_queue_depth < self.capacity

    def process_response(self, line: str, session: StreamSession) -> tuple[bool, str]:
        '''
            Processes response line from firmware and updates session queue depth.

            :param line: Raw response line from firmware.
            :param session: Active StreamSession instance.
            :return: Tuple of (is_fatal_error, error_message).
            :exceptions: None.
        '''
        if self._homing_classifier.is_homing_failed(line):
            self._barrier_coordinator.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            return True, f'Microcontroller Homing Failed: {line}'

        if self._motion_classifier.is_action_done(line):
            self._barrier_coordinator.clear_barrier()

        if self._response_parser.has_queue_depth(line):
            session.remote_queue_depth = self._response_parser.parse_queue_depth(line)
        elif self._flow_classifier.is_buffer_full(line):
            session.remote_queue_depth = self.capacity
        elif self._motion_classifier.is_complete(line):
            session.done_count = min(len(session.waypoints), session.done_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
        elif self._motion_classifier.is_move_failed(line):
            self._barrier_coordinator.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
            return False, line
        elif self._flow_classifier.is_error(line):
            self._barrier_coordinator.clear_barrier()
            session.failed_count = min(len(session.waypoints), session.failed_count + 1)
            if session.remote_queue_depth > 0:
                session.remote_queue_depth -= 1
            return False, line

        return False, ''

    def handle_binary_ack(self, session: StreamSession, free_slots: int) -> None:
        '''
            Updates queue depth from firmware ACK free slot count.

            :param session: Active StreamSession instance.
            :param free_slots: Number of free ring-buffer slots reported by MCU.
            :exceptions: None.
        '''
        session.remote_queue_depth = max(0, self.capacity - free_slots)

    def handle_binary_move_event(self, session: StreamSession, event_type: int) -> None:
        '''
            Updates progress from firmware move event.

            :param session: Active StreamSession instance.
            :param event_type: 1=START, 2=DONE, 3=FAILED.
            :exceptions: None.
        '''
        match event_type:
            case 2:
                session.done_count += 1
                if session.remote_queue_depth > 0:
                    session.remote_queue_depth -= 1
            case 3:
                session.failed_count += 1
                if session.remote_queue_depth > 0:
                    session.remote_queue_depth -= 1
            case _:
                pass
