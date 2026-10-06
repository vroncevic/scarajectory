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

from typing import Final

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.infrastructure.streaming.observer.istream_observer_registry import IStreamObserverRegistry
from scarajectory.infrastructure.streaming.observer.istream_telemetry_notifier import IStreamTelemetryNotifier

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
            | _registry - Injected IStreamObserverRegistry holding subscriber list.
            | _notifier - Injected IStreamTelemetryNotifier dispatching notifications.

        :methods:
            | set_observer - Sets primary active observer.
            | attach_observer - Registers observer subscriber.
            | detach_observer - Removes observer subscriber.
            | has_observers - Checks whether any observers are registered.
            | has_observer - Checks whether any observers are registered (alias).
            | notify_log - Dispatches serial log message to all observers.
            | notify_progress - Computes metrics and dispatches progress to all observers.
    '''

    _registry: IStreamObserverRegistry
    _notifier: IStreamTelemetryNotifier

    def __init__(
        self,
        *,
        registry: IStreamObserverRegistry,
        notifier: IStreamTelemetryNotifier,
    ) -> None:
        '''
        Initializes dispatcher with registry and notifier collaborators.

        :param registry: Injected IStreamObserverRegistry instance.
        :param notifier: Injected IStreamTelemetryNotifier instance.
        '''
        self._registry: Final[IStreamObserverRegistry] = registry
        self._notifier: Final[IStreamTelemetryNotifier] = notifier

    def set_observer(self, observer: IObserver) -> None:
        '''
        Sets primary active observer.

        :param observer: Non-null IObserver instance.
        '''
        self._registry.set_observer(observer)

    def attach_observer(self, observer: IObserver) -> None:
        '''
        Registers observer subscriber.

        :param observer: Non-null IObserver instance.
        '''
        self._registry.attach_observer(observer)

    def detach_observer(self, observer: IObserver) -> None:
        '''
        Removes observer subscriber.

        :param observer: Non-null IObserver instance.
        '''
        self._registry.detach_observer(observer)

    def has_observers(self) -> bool:
        '''
        Checks whether any observers are currently registered.

        :return: True if observers exist, False otherwise.
        '''
        return len(self._registry.get_observers()) > 0

    def has_observer(self) -> bool:
        '''
        Checks whether any observers are currently registered (alias for has_observers).

        :return: True if observers exist, False otherwise.
        '''
        return self.has_observers()

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''
        Dispatches serial log message to all observers.

        :param msg: Message string.
        :param is_outgoing: True if transmitted command, False if received.
        '''
        self._notifier.notify_log(msg, is_outgoing=is_outgoing)

    def notify_progress(
        self,
        *,
        state: StreamState,
        session: StreamSession,
        current_line: str = '',
        error: str = '',
    ) -> None:
        '''
        Computes metrics and dispatches progress to all observers.

        :param state: Current StreamState.
        :param session: Active StreamSession with metrics.
        :param current_line: Currently executing instruction line.
        :param error: Optional error description.
        '''
        self._notifier.notify_progress(
            state=state,
            session=session,
            current_line=current_line,
            error=error,
        )
