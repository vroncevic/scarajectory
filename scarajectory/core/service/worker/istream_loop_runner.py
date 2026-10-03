# -*- coding: UTF-8 -*-

'''
Module
    istream_loop_runner.py
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
    Defines structural protocol IStreamLoopRunner for ASCII streaming execution loop operations.
'''

from __future__ import annotations

from threading import Event
from typing import Protocol, runtime_checkable

from scarajectory.core.model.state.stream_session import StreamSession

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamLoopRunner(Protocol):
    '''
        Structural protocol defining ASCII streaming loop execution and response ingestion.

        It defines:

            :methods:
                | run_loop - Background execution loop transmitting waypoints according to flow control.
                | handle_incoming_line - Evaluates incoming response line and updates metrics.
    '''

    def run_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Background execution loop transmitting waypoints according to flow control.

            :param session: Active StreamSession model.
            :param stop_event: Thread stop signal event.
            :param pause_event: Thread pause signal event.
        '''

    def handle_incoming_line(
        self,
        line: str,
        *,
        session: StreamSession,
    ) -> bool:
        '''
            Evaluates incoming microcontroller response string.

            :param line: Raw response line string.
            :param session: Active StreamSession model.
            :return: True if a fatal error occurred requiring stream abort, False otherwise.
        '''
