# -*- coding: UTF-8 -*-

'''
Module
    ibinary_queue_drainer.py
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
    Defines structural protocol for binary stream queue draining and completion.
'''

from __future__ import annotations

from threading import Event
from typing import Protocol, runtime_checkable

from scarajectory.core.model.state.stream_session import StreamSession

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryQueueDrainer(Protocol):
    '''
        Structural protocol defining binary stream queue draining and completion.

        It defines:

            :methods:
                | is_queue_empty - Checks if all in-flight items have completed.
                | drain_queue - Waits for remote queue to drain and marks completion.
    '''

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
