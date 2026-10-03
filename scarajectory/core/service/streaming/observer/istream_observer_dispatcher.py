# -*- coding: UTF-8 -*-

'''
Module
    istream_observer_dispatcher.py
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
    Defines structural protocol IStreamObserverDispatcher for publishing
    progress and log notifications.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamObserverDispatcher(Protocol):
    '''
        Structural protocol defining progress and log notification dispatching
        to observers.

        It defines:

            :methods:
                | notify_log - Dispatches serial log message to all observers.
                | notify_progress - Computes metrics and dispatches progress.
    '''

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''
            Dispatches serial log message to all registered observers.

            :param msg: Message string.
            :param is_outgoing: True if transmitted command, False if received.
            :exceptions: None.
        '''

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
            :exceptions: None.
        '''
