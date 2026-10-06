# -*- coding: UTF-8 -*-

'''
Module
    ibinary_step_dispatcher.py
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
    Defines structural protocol for binary step and waypoint dispatching.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.step import Step

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
class IBinaryStepDispatcher(Protocol):
    '''
        Structural protocol defining binary step and waypoint dispatching operations.

        It defines:

            :methods:
                | can_dispatch_step - Checks if next item can be transmitted.
                | dispatch_waypoint - Encodes and transmits next waypoint.
                | dispatch_binary_step - Transmits pre-compiled binary step.
    '''

    def can_dispatch_step(self, session: StreamSession) -> bool:
        '''
            Checks whether next waypoint or step can be transmitted based on buffer.

            :param session: Active StreamSession tracking metrics.
            :return: True if ready to transmit, False if flow throttled.
            :exceptions: None.
        '''

    def dispatch_waypoint(self, session: StreamSession) -> None:
        '''
            Encodes and transmits next waypoint from session and updates counters.

            :param session: Active StreamSession tracking metrics.
            :exceptions: None.
        '''

    def dispatch_binary_step(
        self,
        *,
        session: StreamSession,
        step: Step,
    ) -> None:
        '''
            Transmits pre-compiled binary step and updates session counters.

            :param session: Active StreamSession tracking metrics.
            :param step: Pre-compiled Step with raw frame bytes.
            :exceptions: None.
        '''
