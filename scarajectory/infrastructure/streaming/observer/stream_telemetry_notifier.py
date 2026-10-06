# -*- coding: UTF-8 -*-

'''
Module
    stream_telemetry_notifier.py
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
    Broadcaster delivering serial logs and telemetry progress to registered observers.
'''

from __future__ import annotations

from time import time
from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.streaming.observer.istream_observer_registry import IStreamObserverRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTelemetryNotifier:
    '''
    Broadcaster delivering serial logs and telemetry progress to registered observers.

    It defines:

        :attributes:
            | _registry - Injected IStreamObserverRegistry holding subscribers.

        :methods:
            | notify_log - Dispatches serial log message to all registered observers.
            | notify_progress - Computes metrics and dispatches progress to all registered observers.
    '''

    _registry: IStreamObserverRegistry

    def __init__(self, registry: IStreamObserverRegistry) -> None:
        '''
        Initializes StreamTelemetryNotifier with injected observer registry.

        :param registry: Injected IStreamObserverRegistry instance.
        '''
        self._registry: Final[IStreamObserverRegistry] = registry

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''
        Dispatches serial log message to all registered observers.

        :param msg: Message string.
        :param is_outgoing: True if transmitted command, False if received.
        '''
        for observer in self._registry.get_observers():
            observer.on_serial_log(msg, is_outgoing=is_outgoing)

    def notify_progress(
        self,
        *,
        state: StreamState,
        session: StreamSession,
        current_line: str = '',
        error: str = '',
    ) -> None:
        '''
        Computes metrics and dispatches progress to all registered observers.

        :param state: Current StreamState.
        :param session: Active StreamSession with metrics.
        :param current_line: Currently executing instruction line.
        :param error: Optional error description.
        '''
        observers = self._registry.get_observers()

        if not observers:
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
        for observer in observers:
            observer.on_stream_progress(prog)
