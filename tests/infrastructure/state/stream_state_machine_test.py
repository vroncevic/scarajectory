# -*- coding: UTF-8 -*-

'''
Module
    stream_state_machine_test.py
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
    Unit tests for StreamStateMachine and StreamStateMachineFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.infrastructure.state.stream_state_machine import (
    StreamStateMachine,
)
from scarajectory.infrastructure.state.stream_state_machine_factory import (
    StreamStateMachineFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamStateMachineTestCase(TestCase):
    '''
        Tests for StreamStateMachine lifecycle transitions and status queries.

        It defines:

            :methods:
                | test_factory_and_initial_state - Verifies factory creation and defaults.
                | test_state_mutation_and_property - Verifies state getter and set_state.
                | test_transition_to - Verifies state change flag on transition_to.
                | test_is_active - Verifies active stream status reporting.
                | test_reset - Verifies resetting state machine back to IDLE.
    '''

    def test_factory_and_initial_state(self) -> None:
        '''
            Verifies factory creation and defaults.

            :exceptions: None.
        '''
        sm_default = StreamStateMachineFactory.create()
        self.assertIsInstance(sm_default, StreamStateMachine)
        self.assertEqual(sm_default.state, StreamState.IDLE)
        self.assertEqual(StreamStateMachineFactory.get_version(), '1.0.4')

        sm_custom = StreamStateMachineFactory.create(
            initial_state=StreamState.STREAMING
        )
        self.assertEqual(sm_custom.state, StreamState.STREAMING)

    def test_state_mutation_and_property(self) -> None:
        '''
            Verifies state getter and set_state.

            :exceptions: None.
        '''
        sm = StreamStateMachine(initial_state=StreamState.IDLE)
        sm.set_state(StreamState.PAUSED)
        self.assertEqual(sm.state, StreamState.PAUSED)

    def test_transition_to(self) -> None:
        '''
            Verifies state change flag on transition_to.

            :exceptions: None.
        '''
        sm = StreamStateMachine(initial_state=StreamState.IDLE)
        # Transition to new state: returns True
        changed = sm.transition_to(StreamState.STREAMING)
        self.assertTrue(changed)
        self.assertEqual(sm.state, StreamState.STREAMING)

        # Transition to identical state: returns False
        changed_again = sm.transition_to(StreamState.STREAMING)
        self.assertFalse(changed_again)

    def test_is_active(self) -> None:
        '''
            Verifies active stream status reporting.

            :exceptions: None.
        '''
        sm = StreamStateMachine()
        self.assertFalse(sm.is_active())

        sm.set_state(StreamState.STREAMING)
        self.assertTrue(sm.is_active())

        sm.set_state(StreamState.PAUSED)
        self.assertTrue(sm.is_active())

        sm.set_state(StreamState.COMPLETED)
        self.assertFalse(sm.is_active())

        sm.set_state(StreamState.ERROR)
        self.assertFalse(sm.is_active())

    def test_reset(self) -> None:
        '''
            Verifies resetting state machine back to IDLE.

            :exceptions: None.
        '''
        sm = StreamStateMachine(initial_state=StreamState.STREAMING)
        sm.reset()
        self.assertEqual(sm.state, StreamState.IDLE)


if __name__ == '__main__':
    main()
