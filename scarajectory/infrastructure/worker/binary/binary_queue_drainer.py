# -*- coding: UTF-8 -*-

'''
Module
    binary_queue_drainer.py
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
    Drains microcontroller queue post-loop for binary stream sessions.
'''

from __future__ import annotations

from datetime import datetime
from threading import Event
from time import sleep, time
from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.infrastructure.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryQueueDrainer:
    '''
        Handles post-transmission remote queue draining and completion for binary streaming.

        It defines:

            :attributes:
                | _state_controller - IStreamStateController managing stream lifecycle state.
                | _observer_dispatcher - IStreamObserverDispatcher publishing progress and logs.
                | _pacing_config - StreamPacingConfig with loop pacing delays.
            :methods:
                | __init__ - Initializes queue drainer with injected collaborators.
                | is_queue_empty - Checks if all in-flight items have completed.
                | drain_queue - Waits for remote queue to drain and marks completion.
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
            Initializes binary queue drainer with collaborators.

            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher publishing telemetry.
            :param pacing_config: Pacing configuration with poll delay.
            :exceptions: None.
        '''
        self._state_controller: Final[IStreamStateController] = state_controller
        self._observer_dispatcher: Final[IStreamObserverDispatcher] = (
            observer_dispatcher
        )
        self._pacing_config: Final[StreamPacingConfig] = pacing_config

    def is_queue_empty(
        self,
        *,
        session: StreamSession,
        total_items: int,
    ) -> bool:
        '''
            Checks if all queued items have completed or failed.

            :param session: Active StreamSession tracking metrics.
            :param total_items: Total number of items expected.
            :return: True if remote queue is completely drained.
            :exceptions: None.
        '''
        return (session.done_count + session.failed_count) >= total_items

    def drain_queue(
        self,
        *,
        session: StreamSession,
        total_items: int,
        stop_event: Event,
    ) -> None:
        '''
            Waits for remote microcontroller queue to drain and signals completion.

            :param session: Active StreamSession tracking metrics.
            :param total_items: Total number of items expected.
            :param stop_event: Thread stop signal event.
            :exceptions: None.
        '''
        while (
            not stop_event.is_set()
            and not self.is_queue_empty(session=session, total_items=total_items)
        ):
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
            self._observer_dispatcher.notify_log(
                f'[{end_ts}] [BINARY STREAM COMPLETED]: {session.done_count} finished, '
                f'{session.failed_count} failed in {elapsed:.2f}s',
                False,
            )
