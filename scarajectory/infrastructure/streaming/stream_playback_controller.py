# -*- coding: UTF-8 -*-

'''
Module
    stream_playback_controller.py
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
    Coordinates playback lifecycle and execution controls for streaming.
'''

from __future__ import annotations

from datetime import datetime
from time import time
from typing import Final, Sequence

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.barrier.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.core.service.connection.iconnection import IConnection
from scarajectory.core.service.state.istream_state_machine import IStreamStateMachine
from scarajectory.core.service.streaming.istream_control_transmitter import IStreamControlTransmitter
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPlaybackController:
    '''
        Coordinates playback lifecycle and execution controls for streaming.

        It defines:

            :attributes:
                | _connection - Injected IConnection instance.
                | _state_machine - Injected IStreamStateMachine tracking lifecycle.
                | _dispatcher - Injected IStreamObserverDispatcher publishing telemetry.
                | _barrier_coordinator - Injected IFlowBarrierCoordinator managing synchronization.
                | _worker - Injected IExecutionWorker running playback loop.
                | _session - Active StreamSession instance.
                | _control_transmitter - Injected IStreamControlTransmitter for control frames.
                | _protocol_mode - ProtocolMode specifying wire format.
            :methods:
                | start_streaming - Starts background streaming worker with sequence of waypoints.
                | pause_streaming - Pauses background streaming transmission.
                | resume_streaming - Resumes paused background streaming transmission.
                | stop_streaming - Aborts active streaming session and triggers E-STOP.
    '''

    _connection: IConnection
    _state_machine: IStreamStateMachine
    _dispatcher: IStreamObserverDispatcher
    _barrier_coordinator: IFlowBarrierCoordinator
    _worker: IExecutionWorker
    _session: StreamSession
    _control_transmitter: IStreamControlTransmitter
    _protocol_mode: ProtocolMode

    def __init__(
        self,
        *,
        connection: IConnection,
        barrier_coordinator: IFlowBarrierCoordinator,
        state_machine: IStreamStateMachine,
        dispatcher: IStreamObserverDispatcher,
        worker: IExecutionWorker,
        control_transmitter: IStreamControlTransmitter,
        session: StreamSession,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> None:
        '''
            Initializes playback controller with injected abstract interfaces.

            :param connection: Injected IConnection instance.
            :param barrier_coordinator: Injected IFlowBarrierCoordinator instance.
            :param state_machine: Injected IStreamStateMachine instance.
            :param dispatcher: Injected IStreamObserverDispatcher instance.
            :param worker: Injected IExecutionWorker instance.
            :param control_transmitter: Injected IStreamControlTransmitter instance.
            :param session: Injected StreamSession instance.
            :param protocol_mode: Active wire protocol mode enum value.
        '''
        self._connection: Final[IConnection] = connection
        self._barrier_coordinator: Final[IFlowBarrierCoordinator] = (
            barrier_coordinator
        )
        self._state_machine: Final[IStreamStateMachine] = state_machine
        self._dispatcher: Final[IStreamObserverDispatcher] = dispatcher
        self._worker: Final[IExecutionWorker] = worker
        self._control_transmitter: Final[IStreamControlTransmitter] = (
            control_transmitter
        )
        self._session: Final[StreamSession] = session
        self._protocol_mode = protocol_mode

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''
            Starts background streaming worker with sequence of waypoints.

            :param waypoints: Sequence of Waypoint instances.
            :return: True if streaming started, False otherwise.
        '''
        if not self._connection.is_connected():
            self._dispatcher.notify_log(
                '[ERR]: Cannot stream - Transport not connected'
            )
            return False

        if not waypoints:
            return False

        self._session = StreamSession(
            waypoints=list(waypoints),
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=time(),
        )
        self._state_machine.transition_to(StreamState.STREAMING)
        self._barrier_coordinator.reset()

        start_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        self._dispatcher.notify_log(
            f'[{start_ts}] [STREAM TRIGGERED]: Starting execution of '
            f'{len(self._session.waypoints)} waypoints...'
        )
        self._control_transmitter.send_enable(self._protocol_mode)
        self._worker.start(session=self._session)
        self._dispatcher.notify_progress(
            state=self._state_machine.state,
            session=self._session,
        )

        return True

    def pause_streaming(self) -> None:
        '''
            Pauses background streaming transmission.
        '''
        if self._state_machine.state == StreamState.STREAMING:
            self._state_machine.transition_to(StreamState.PAUSED)
            self._worker.pause()
            self._dispatcher.notify_progress(
                state=self._state_machine.state,
                session=self._session,
            )
            self._control_transmitter.send_hold(self._protocol_mode)
            self._dispatcher.notify_log('[HOST]: Streaming PAUSED')

    def resume_streaming(self) -> None:
        '''
            Resumes paused background streaming transmission.
        '''
        if self._state_machine.state == StreamState.PAUSED:
            self._state_machine.transition_to(StreamState.STREAMING)
            self._worker.resume()
            self._dispatcher.notify_progress(
                state=self._state_machine.state,
                session=self._session,
            )
            self._control_transmitter.send_resume(self._protocol_mode)
            self._dispatcher.notify_log('[HOST]: Streaming RESUMED')

    def stop_streaming(self) -> None:
        '''
            Aborts active streaming session and triggers E-STOP.
        '''
        was_streaming: bool = self._state_machine.is_active()
        self._state_machine.transition_to(StreamState.STOPPED)
        self._worker.stop()

        if self._connection.is_connected():
            self._control_transmitter.send_estop(self._protocol_mode)

        self._dispatcher.notify_progress(
            state=self._state_machine.state,
            session=self._session,
        )

        if was_streaming:
            self._dispatcher.notify_log(
                '[HOST]: Streaming ABORTED (E-STOP sent)'
            )
