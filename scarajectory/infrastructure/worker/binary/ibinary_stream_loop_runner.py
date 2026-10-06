# -*- coding: UTF-8 -*-

'''
Module
    ibinary_stream_loop_runner.py
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
    Structural protocol defining streaming execution loop and frame ingestion operations.
'''

from __future__ import annotations

from threading import Event
from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.program import BinaryProgram
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
class IBinaryStreamLoopRunner(Protocol):
    '''
        Structural protocol defining streaming execution loop and frame ingestion operations.

        It defines:

            :methods:
                | run_waypoints_loop - Executes loop streaming waypoints sequence.
                | run_program_loop - Executes loop streaming pre-compiled binary steps.
                | handle_incoming_bytes - Feeds raw incoming bytes into parser and dispatches frames.
    '''

    def run_waypoints_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Executes loop streaming waypoints sequence to hardware.

            :param session: Active StreamSession tracking waypoints and progress.
            :param stop_event: Event signaling loop termination.
            :param pause_event: Event signaling transmission pause.
            :exceptions: None.
        '''

    def run_program_loop(
        self,
        *,
        session: StreamSession,
        program: BinaryProgram,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Executes loop streaming pre-compiled binary steps to hardware.

            :param session: Active StreamSession tracking stream metrics.
            :param program: BinaryProgram containing compiled binary steps.
            :param stop_event: Event signaling loop termination.
            :param pause_event: Event signaling transmission pause.
            :exceptions: None.
        '''

    def handle_incoming_bytes(
        self,
        *,
        data: bytes,
        session: StreamSession,
    ) -> bool:
        '''
            Feeds raw incoming bytes into parser and dispatches decoded frames.

            :param data: Byte chunk received from transport.
            :param session: Active StreamSession tracking metrics.
            :return: True if a fault frame occurred requiring immediate stop.
            :exceptions: None.
        '''
