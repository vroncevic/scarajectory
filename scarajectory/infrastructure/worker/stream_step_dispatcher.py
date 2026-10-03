# -*- coding: UTF-8 -*-

'''
Module
    stream_step_dispatcher.py
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
    Dispatches single waypoint or command step to hardware transport.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.barrier.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.core.service.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.icommand_formatter import ICommandFormatter
from scarajectory.core.service.worker.icommand_sender import ICommandSender
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamStepDispatcher:
    '''
        Dispatches single waypoint or command step to hardware transport.

        It defines:

            :attributes:
                | _flow_pacing - IFlowPacingController managing buffer queue.
                | _barrier_coordinator - IFlowBarrierCoordinator managing synchronization barriers.
                | _formatter - ICommandFormatter encoding waypoints.
                | _command_sender - ICommandSender transmitting packets.
                | _state_controller - IStreamStateController managing state.
                | _observer_dispatcher - Observer dispatcher for telemetry.
            :methods:
                | __init__ - Initializes step dispatcher with collaborators.
                | can_dispatch_step - Checks if next step can be transmitted.
                | dispatch_step - Transmits next step and updates counters.
    '''

    _flow_pacing: IFlowPacingController
    _barrier_coordinator: IFlowBarrierCoordinator
    _formatter: ICommandFormatter
    _command_sender: ICommandSender
    _state_controller: IStreamStateController
    _observer_dispatcher: IStreamObserverDispatcher

    def __init__(
        self,
        *,
        pacing_bundle: FlowPacingBundle,
        formatter: ICommandFormatter,
        command_sender: ICommandSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
    ) -> None:
        '''
            Initializes step dispatcher with collaborators.

            :param pacing_bundle: FlowPacingBundle managing pacing and barrier.
            :param formatter: Formatter converting waypoints to commands.
            :param command_sender: Sender transmitting raw command strings.
            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher publishing telemetry.
            :exceptions: None.
        '''
        self._flow_pacing: Final[IFlowPacingController] = (
            pacing_bundle.pacing_controller
        )
        self._barrier_coordinator: Final[IFlowBarrierCoordinator] = (
            pacing_bundle.barrier_coordinator
        )
        self._formatter: Final[ICommandFormatter] = formatter
        self._command_sender: Final[ICommandSender] = command_sender
        self._state_controller: Final[IStreamStateController] = (
            state_controller
        )
        self._observer_dispatcher: Final[IStreamObserverDispatcher] = (
            observer_dispatcher
        )

    def can_dispatch_step(self, session: StreamSession) -> bool:
        '''
            Checks whether next waypoint or command can be transmitted.

            :param session: Active StreamSession model.
            :return: True if ready to transmit, False if flow throttled.
            :exceptions: None.
        '''
        if session.sent_count >= len(session.waypoints):
            return False

        pt: Waypoint = session.waypoints[session.sent_count]

        return self._flow_pacing.can_send(
            session, is_command=bool(pt.command)
        )

    def dispatch_step(self, session: StreamSession) -> None:
        '''
            Transmits next waypoint or command packet and updates session.

            :param session: Active StreamSession model.
            :exceptions: None.
        '''
        pt: Waypoint = session.waypoints[session.sent_count]
        is_cmd: bool = bool(pt.command)
        pkt: str = (
            pt.command if pt.command else self._formatter.format_move(pt)
        )

        if is_cmd:
            self._barrier_coordinator.set_barrier()

        self._command_sender.send_raw_command(pkt)
        session.sent_count += 1

        if not is_cmd:
            session.remote_queue_depth += 1

        self._observer_dispatcher.notify_progress(
            state=self._state_controller.state,
            session=session,
            error='',
        )
