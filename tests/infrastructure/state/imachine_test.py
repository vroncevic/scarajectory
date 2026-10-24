# -*- coding: UTF-8 -*-

'''
Module
    imachine_test.py
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
    Unit tests for IStreamStateMachine structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.infrastructure.state.imachine import IStreamStateMachine

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyStateMachine:
    '''Dummy state machine class for testing IStreamStateMachine structural conformance.'''

    @property
    def state(self) -> StreamState:
        '''Returns stream state.'''
        return StreamState.IDLE

    def transition_to(self, target: StreamState) -> bool:
        '''Transitions to target stream state.'''
        return target == StreamState.IDLE

    def is_active(self) -> bool:
        '''Checks if state machine is active.'''
        return False


class DummyIncompleteStateMachine:
    '''Incomplete dummy state machine class missing required methods.'''

    def is_active(self) -> bool:
        '''Checks if state machine is active.'''
        return False

    def reset_state(self) -> None:
        '''Dummy method to satisfy minimum method count.'''


class TestIStreamStateMachine(TestCase):
    '''Unit tests validating IStreamStateMachine protocol structure and checks.'''

    def test_protocol_conformance_valid(self) -> None:
        '''Verifies valid structural implementation satisfies IStreamStateMachine.'''
        dummy = DummyStateMachine()
        self.assertIsInstance(dummy, IStreamStateMachine)

    def test_protocol_conformance_invalid(self) -> None:
        '''Verifies incomplete implementation fails IStreamStateMachine check.'''
        dummy_incomplete = DummyIncompleteStateMachine()
        self.assertNotIsInstance(dummy_incomplete, IStreamStateMachine)


if __name__ == '__main__':
    main()
