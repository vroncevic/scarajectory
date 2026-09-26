# -*- coding: UTF-8 -*-

'''
Module
    stream_state_machine.py
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
    State machine managing streaming lifecycle states and valid transitions.
'''

from __future__ import annotations

from scarajectory.core.model.communication.stream.stream_state import StreamState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamStateMachine:
    '''
        State machine managing streaming lifecycle states and valid transitions.

        It defines:

            :attributes:
                | _state - Current StreamState enum value.
            :methods:
                | __init__ - Initializes state machine to specified initial state.
                | state - Returns current StreamState.
                | set_state - Directly sets the current stream state.
                | transition_to - Transitions to a new state and returns whether changed.
                | is_active - Returns True if stream is currently streaming or paused.
                | reset - Resets state back to IDLE.
    '''

    _state: StreamState

    def __init__(self, initial_state: StreamState = StreamState.IDLE) -> None:
        '''
            Initializes state machine to specified initial state.

            :param initial_state: Initial StreamState enum value.
            :exceptions: None.
        '''
        self._state = initial_state

    @property
    def state(self) -> StreamState:
        '''
            Returns the current StreamState enum value.

            :return: Current StreamState.
            :exceptions: None.
        '''
        return self._state

    def set_state(self, state: StreamState) -> None:
        '''
            Directly sets current stream state.

            :param state: New StreamState enum value.
            :exceptions: None.
        '''
        self._state = state

    def transition_to(self, new_state: StreamState) -> bool:
        '''
            Transitions to a new state and returns whether the state changed.

            :param new_state: Target StreamState.
            :return: True if transitioned, False if state was already identical.
            :exceptions: None.
        '''
        if self._state == new_state:
            return False
        self._state = new_state
        return True

    def is_active(self) -> bool:
        '''
            Checks if stream is currently actively streaming or paused.

            :return: True if in STREAMING or PAUSED state.
            :exceptions: None.
        '''
        return self._state in (StreamState.STREAMING, StreamState.PAUSED)

    def reset(self) -> None:
        '''
            Resets state back to IDLE.

            :exceptions: None.
        '''
        self._state = StreamState.IDLE
