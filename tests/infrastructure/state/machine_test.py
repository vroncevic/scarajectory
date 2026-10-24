# -*- coding: UTF-8 -*-

'''
Module
    machine_test.py
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
    Unit tests for StreamStateMachine component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.infrastructure.state.machine import StreamStateMachine

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamStateMachine(TestCase):
    '''
        Tests for StreamStateMachine lifecycle transitions and status queries.

        It defines:

            :methods:
                | test_initial_state_default - Verifies default state is IDLE.
                | test_initial_state_custom - Verifies custom initial state is respected.
                | test_transition_to - Verifies state change flag on transition_to.
                | test_is_active - Verifies active stream status reporting.
    '''

    def test_initial_state_default(self) -> None:
        '''
            Verifies initial state is IDLE.

            :exceptions: None.
        '''
        sm = StreamStateMachine(StreamState.IDLE)
        self.assertEqual(sm.state, StreamState.IDLE)

    def test_initial_state_custom(self) -> None:
        '''
            Verifies custom initial state is set upon construction.

            :exceptions: None.
        '''
        sm = StreamStateMachine(initial_state=StreamState.STREAMING)
        self.assertEqual(sm.state, StreamState.STREAMING)

    def test_transition_to(self) -> None:
        '''
            Verifies state change flag on transition_to.

            :exceptions: None.
        '''
        sm = StreamStateMachine(initial_state=StreamState.IDLE)
        changed = sm.transition_to(StreamState.STREAMING)
        self.assertTrue(changed)
        self.assertEqual(sm.state, StreamState.STREAMING)

        changed_again = sm.transition_to(StreamState.STREAMING)
        self.assertFalse(changed_again)
        self.assertEqual(sm.state, StreamState.STREAMING)

    def test_is_active(self) -> None:
        '''
            Verifies active stream status reporting for streaming and paused states.

            :exceptions: None.
        '''
        sm = StreamStateMachine(StreamState.IDLE)
        self.assertFalse(sm.is_active())

        sm.transition_to(StreamState.STREAMING)
        self.assertTrue(sm.is_active())

        sm.transition_to(StreamState.PAUSED)
        self.assertTrue(sm.is_active())

        sm.transition_to(StreamState.COMPLETED)
        self.assertFalse(sm.is_active())

        sm.transition_to(StreamState.STOPPED)
        self.assertFalse(sm.is_active())

        sm.transition_to(StreamState.ERROR)
        self.assertFalse(sm.is_active())


if __name__ == '__main__':
    main()
