# -*- coding: UTF-8 -*-

'''
Module
    stream_queue_drainer.py
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
    Drains microcontroller queue post-loop and signals session completion.
'''

from __future__ import annotations

from datetime import datetime
from threading import Event
from time import sleep, time
from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamQueueDrainer:
    '''
        Handles post-transmission remote queue draining and completion.

        It defines:

            :attributes:
                | _state_controller - IStreamStateController managing state.
                | _observer_dispatcher - Telemetry observer dispatcher.
                | _pacing_config - StreamPacingConfig with loop pacing delays.
            :methods:
                | __init__ - Initializes queue drainer with collaborators.
                | is_queue_empty - Checks if all waypoints have completed.
                | drain_queue - Waits for remaining commands to drain.
    '''

    _state_controller: IStreamStateController
    _observer_dispatcher: IStreamObserverDispatcher
    _pacing_config: StreamPacingConfig

    def __init__(
        self,
        *,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> None:
        '''
            Initializes queue drainer with collaborators.

            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher publishing telemetry.
            :param pacing_config: Pacing configuration with poll delay.
            :exceptions: None.
        '''
        self._state_controller: Final[IStreamStateController] = (
            state_controller
        )
        self._observer_dispatcher: Final[IStreamObserverDispatcher] = (
            observer_dispatcher
        )
        self._pacing_config: Final[StreamPacingConfig] = pacing_config

    def is_queue_empty(self, session: StreamSession) -> bool:
        '''
            Checks if all waypoints have completed or failed.

            :param session: Active StreamSession model.
            :return: True if remote queue is completely drained.
            :exceptions: None.
        '''
        return (
            session.done_count + session.failed_count
        ) >= len(session.waypoints)

    def drain_queue(self, session: StreamSession, stop_event: Event) -> None:
        '''
            Waits for remote queue to drain and marks stream completed.

            :param session: Active StreamSession model.
            :param stop_event: Thread stop signal event.
            :exceptions: None.
        '''
        while not stop_event.is_set() and not self.is_queue_empty(session):
            sleep(self._pacing_config.poll_delay)

        if not stop_event.is_set():
            self._state_controller.set_state(StreamState.COMPLETED)
            elapsed: float = time() - session.start_time
            end_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self._observer_dispatcher.notify_progress(
                state=self._state_controller.state,
                session=session,
                error='',
            )
            if session.failed_count > 0:
                self._observer_dispatcher.notify_log(
                    f'[{end_ts}] [MOVE FINISHED]: {session.done_count} '
                    f'succeeded, {session.failed_count} failed/rejected!',
                    False,
                )
            else:
                self._observer_dispatcher.notify_log(
                    f'[{end_ts}] [MOVE COMPLETED]: All '
                    f'{len(session.waypoints)} waypoints finished!',
                    False,
                )
            self._observer_dispatcher.notify_log(
                f'[HOST STATS]: Total Execution Time: {elapsed:.2f} s',
                False,
            )
