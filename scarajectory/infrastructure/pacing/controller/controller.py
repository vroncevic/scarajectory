# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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
    Manages microcontroller queue pacing, window occupancy, and binary response decoding.
'''

from __future__ import annotations

from typing import Final

from scaracom.flow.pacing.window import FlowWindow

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.infrastructure.pacing.controller.dependencies import ControllerDependencies
from scarajectory.infrastructure.pacing.coordinator.icoordinator import IFlowBarrierCoordinator

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
        Manages microcontroller queue pacing, window occupancy, and binary response decoding.

        It defines:

            :attributes:
                | capacity - Maximum allowed queue depth before throttling.
                | _flow_window - Flow control window tracking slot capacity.
                | _flow_barrier_coordinator - Injected IFlowBarrierCoordinator managing gating.
            :methods:
                | __init__ - Initializes pacing controller with injected dependencies.
                | can_send - Checks whether next packet or command is permitted to be transmitted.
                | handle_binary_ack - Updates queue depth from firmware ACK free slot count.
                | handle_binary_move_event - Updates progress from firmware move event.
    '''

    capacity: int
    _flow_window: FlowWindow
    _flow_barrier_coordinator: IFlowBarrierCoordinator

    def __init__(self, dependencies: ControllerDependencies) -> None:
        '''
            Initializes flow pacing controller with specified dependencies bundle.

            :param dependencies: Injected ControllerDependencies parameter bundle.
            :exceptions: None.
        '''
        self.capacity: Final[int] = dependencies.capacity
        self._flow_window: Final[FlowWindow] = FlowWindow(
            max_in_flight=dependencies.capacity
        )
        self._flow_barrier_coordinator: Final[IFlowBarrierCoordinator] = (
            dependencies.flow_barrier_coordinator
        )

    def can_send(self, session: StreamSession, is_command: bool = False) -> bool:
        '''
            Checks whether next packet or command is permitted to be transmitted.

            :param session: Active StreamSession model.
            :param is_command: True if next item is a synchronous command (default False).
            :return: True if transmission is allowed, False otherwise.
            :exceptions: None.
        '''
        if not self._flow_barrier_coordinator.is_barrier_clear():
            return False

        if is_command and session.remote_queue_depth > 0:
            return False

        return session.remote_queue_depth < self.capacity

    def handle_binary_ack(self, session: StreamSession, free_slots: int) -> None:
        '''
            Updates queue depth from firmware ACK free slot count.

            :param session: Active StreamSession instance.
            :param free_slots: Number of free ring-buffer slots reported by MCU.
            :exceptions: None.
        '''
        self._flow_window.update_from_slots(free_slots)
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
