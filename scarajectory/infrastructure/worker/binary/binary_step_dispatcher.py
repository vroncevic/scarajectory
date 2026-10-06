# -*- coding: UTF-8 -*-

'''
Module
    binary_step_dispatcher.py
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
    Dispatches single binary step or waypoint to hardware transport.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.step import Step

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.worker.binary.binary_step_bundle import BinaryStepBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStepDispatcher:
    '''
        Dispatches single binary step or waypoint to hardware transport.

        It defines:

            :attributes:
                | _bundle - Injected BinaryStepBundle holding collaborators.
            :methods:
                | __init__ - Initializes step dispatcher with injected bundle.
                | can_dispatch_step - Checks if next item can be transmitted based on buffer.
                | dispatch_waypoint - Encodes and transmits next waypoint.
                | dispatch_binary_step - Transmits pre-compiled binary step.
    '''

    _bundle: BinaryStepBundle

    def __init__(self, bundle: BinaryStepBundle) -> None:
        '''
            Initializes binary step dispatcher with collaborators bundle.

            :param bundle: BinaryStepBundle containing collaborators.
            :exceptions: None.
        '''
        self._bundle: Final[BinaryStepBundle] = bundle

    def can_dispatch_step(self, session: StreamSession) -> bool:
        '''
            Checks whether next waypoint or step can be transmitted based on buffer.

            :param session: Active StreamSession tracking metrics.
            :return: True if ready to transmit, False if flow throttled.
            :exceptions: None.
        '''
        return self._bundle.flow_pacing.can_send(session)

    def dispatch_waypoint(self, session: StreamSession) -> None:
        '''
            Encodes and transmits next waypoint from session and updates counters.

            :param session: Active StreamSession tracking metrics.
            :exceptions: None.
        '''
        pt: Waypoint = session.waypoints[session.sent_count]
        frame_bytes: bytes = self._bundle.packet_strategy.format_waypoint_packet(
            waypoint=pt, seq_num=(session.sent_count + 1) & 0xFFFF
        )
        self._bundle.byte_sender.send_raw_bytes(frame_bytes)
        session.sent_count += 1
        session.remote_queue_depth += 1
        self._bundle.observer_dispatcher.notify_progress(
            state=self._bundle.state_controller.state,
            session=session,
            error='',
        )

    def dispatch_binary_step(
        self,
        *,
        session: StreamSession,
        step: Step,
    ) -> None:
        '''
            Transmits pre-compiled binary step and updates session counters.

            :param session: Active StreamSession tracking metrics.
            :param step: Pre-compiled Step with raw frame bytes.
            :exceptions: None.
        '''
        self._bundle.byte_sender.send_raw_bytes(step.raw_bytes)
        session.sent_count += 1
        session.remote_queue_depth += 1
        self._bundle.observer_dispatcher.notify_progress(
            state=self._bundle.state_controller.state,
            session=session,
            error='',
        )
