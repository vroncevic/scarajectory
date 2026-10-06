# -*- coding: UTF-8 -*-

'''
Module
    stream_loop_runner.py
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
    Executes ASCII stream transmission loop and response processing.
'''

from __future__ import annotations

from threading import Event
from time import sleep
from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.infrastructure.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.infrastructure.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.worker.ascii.istream_queue_drainer import IStreamQueueDrainer
from scarajectory.infrastructure.worker.ascii.istream_step_dispatcher import IStreamStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamLoopRunner:
    '''
        Executes ASCII stream transmission loop and response processing.

        It defines:

            :attributes:
                | _flow_pacing - IFlowPacingController managing buffer queue.
                | _step_dispatcher - IStreamStepDispatcher for packet send.
                | _queue_drainer - IStreamQueueDrainer for post-loop drain.
                | _state_controller - IStreamStateController managing state.
                | _observer_dispatcher - IStreamObserverDispatcher for events.
                | _pacing_config - StreamPacingConfig with loop pacing delays.
            :methods:
                | __init__ - Initializes loop runner with injected delegates.
                | run_loop - Background loop transmitting waypoints.
                | handle_incoming_line - Evaluates incoming response line.
    '''

    _flow_pacing: IFlowPacingController
    _step_dispatcher: IStreamStepDispatcher
    _queue_drainer: IStreamQueueDrainer
    _state_controller: IStreamStateController
    _observer_dispatcher: IStreamObserverDispatcher
    _pacing_config: StreamPacingConfig

    def __init__(
        self,
        *,
        flow_pacing: IFlowPacingController,
        step_dispatcher: IStreamStepDispatcher,
        queue_drainer: IStreamQueueDrainer,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> None:
        '''
            Initializes ASCII stream loop runner with collaborators.

            :param flow_pacing: IFlowPacingController managing queue pacing.
            :param step_dispatcher: Dispatcher sending single steps.
            :param queue_drainer: Drainer polling remaining in-flight moves.
            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher publishing telemetry.
            :param pacing_config: StreamPacingConfig with loop delays.
            :exceptions: None.
        '''
        self._flow_pacing: Final[IFlowPacingController] = flow_pacing
        self._step_dispatcher: Final[IStreamStepDispatcher] = step_dispatcher
        self._queue_drainer: Final[IStreamQueueDrainer] = queue_drainer
        self._state_controller: Final[IStreamStateController] = (
            state_controller
        )
        self._observer_dispatcher: Final[IStreamObserverDispatcher] = (
            observer_dispatcher
        )
        self._pacing_config: Final[StreamPacingConfig] = pacing_config

    def run_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Transmits waypoints according to flow control buffer capacity.

            :param session: Active StreamSession model.
            :param stop_event: Event signaling termination.
            :param pause_event: Event signaling pause.
            :exceptions: None.
        '''
        total_pts: int = len(session.waypoints)

        while not stop_event.is_set() and session.sent_count < total_pts:
            if pause_event.is_set():
                sleep(self._pacing_config.poll_delay)
                continue

            if self._step_dispatcher.can_dispatch_step(session):
                self._step_dispatcher.dispatch_step(session)
                sleep(self._pacing_config.send_delay)
            else:
                sleep(self._pacing_config.poll_delay)

        if not stop_event.is_set():
            self._queue_drainer.drain_queue(
                session=session,
                stop_event=stop_event,
            )

    def handle_incoming_line(
        self,
        line: str,
        *,
        session: StreamSession,
    ) -> bool:
        '''
            Processes inbound response line and updates session queue depth.

            :param line: Raw response line string from microcontroller.
            :param session: Active StreamSession model.
            :return: True if fatal error occurred, False otherwise.
            :exceptions: None.
        '''
        self._observer_dispatcher.notify_log(line, False)

        fatal_error, error_msg = self._flow_pacing.process_response(
            line, session
        )
        if fatal_error:
            err_text: str = error_msg if error_msg else line
            self._observer_dispatcher.notify_progress(
                state=self._state_controller.state,
                session=session,
                error=err_text,
            )
            self._observer_dispatcher.notify_log(
                f'[ERR]: {err_text}. Aborting stream.', False
            )
            self._state_controller.set_state(StreamState.STOPPED)
            return True

        self._observer_dispatcher.notify_progress(
            state=self._state_controller.state,
            session=session,
            error=error_msg,
        )
        return False
