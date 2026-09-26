# -*- coding: UTF-8 -*-

'''
Module
    stream_observer_dispatcher.py
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
    Dispatches serial logging and progress updates to registered stream observers.
'''

from __future__ import annotations

from time import time

from scarajectory.core.model.communication.stream.stream_progress import StreamProgress
from scarajectory.core.model.communication.stream.stream_session import StreamSession
from scarajectory.core.model.communication.stream.stream_state import StreamState
from scarajectory.core.service.communication.stream.iobserver import IObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamObserverDispatcher:
    '''
        Dispatches serial logging and progress updates to registered stream observers.

        It defines:

            :attributes:
                | _observer - Registered IObserver or None.
            :methods:
                | __init__ - Initializes dispatcher with optional observer.
                | set_observer - Sets or clears active observer.
                | has_observer - Checks if an observer is registered.
                | notify_log - Dispatches serial log message to observer.
                | notify_progress - Computes metrics and dispatches progress to observer.
    '''

    _observer: IObserver | None

    def __init__(self, observer: IObserver | None = None) -> None:
        '''
            Initializes dispatcher with optional observer.

            :param observer: Optional IObserver instance.
            :exceptions: None.
        '''
        self._observer = observer

    def set_observer(self, observer: IObserver | None) -> None:
        '''
            Sets or clears the active observer.

            :param observer: IObserver instance or None.
            :exceptions: None.
        '''
        self._observer = observer

    def has_observer(self) -> bool:
        '''
            Checks whether an observer is currently registered.

            :return: True if registered, False otherwise.
            :exceptions: None.
        '''
        return self._observer is not None

    def notify_log(self, msg: str, *, is_outgoing: bool = False) -> None:
        '''
            Dispatches serial log message to observer if registered.

            :param msg: Message string.
            :param is_outgoing: True if transmitted command, False if received.
            :exceptions: None.
        '''
        if self._observer is not None:
            self._observer.on_serial_log(msg, is_outgoing=is_outgoing)

    def notify_progress(
        self,
        *,
        state: StreamState,
        session: StreamSession,
        current_line: str = '',
        error: str = '',
    ) -> None:
        '''
            Computes metrics and dispatches progress to observer if registered.

            :param state: Current StreamState.
            :param session: Active StreamSession with metrics.
            :param current_line: Currently executing instruction line.
            :param error: Optional error description.
            :exceptions: None.
        '''
        if self._observer is None:
            return

        elapsed: float = (
            (time() - session.start_time)
            if (session.start_time > 0.0)
            else 0.0
        )
        total: int = len(session.waypoints)
        done: int = session.done_count + session.failed_count
        pct: float = (done / total * 100.0) if total > 0 else 0.0

        prog: StreamProgress = StreamProgress(
            state=state,
            total_waypoints=total,
            sent_waypoints=session.sent_count,
            completed_waypoints=session.done_count,
            failed_waypoints=session.failed_count,
            current_line=current_line,
            error_message=error,
            elapsed_seconds=elapsed,
            percentage=pct,
        )
        self._observer.on_stream_progress(prog)
