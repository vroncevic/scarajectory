# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for StateProvides output bundle.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.state.machine import StreamStateMachine
from scarajectory.infrastructure.state.provides import StateProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStateProvides(TestCase):
    '''
        Test cases for StateProvides output bundle.

        It defines:

            :methods:
                | test_provides_encapsulation - Verifies StateProvides wraps IStreamStateMachine.
    '''

    def test_provides_encapsulation(self) -> None:
        '''
            Verifies StateProvides holds machine implementing IStreamStateMachine.

            :exceptions: None.
        '''
        machine = StreamStateMachine(StreamState.IDLE)
        provides = StateProvides(stream_state_machine=machine)
        self.assertIsInstance(provides.stream_state_machine, IStreamStateMachine)
        self.assertIs(provides.stream_state_machine, machine)


if __name__ == '__main__':
    main()
