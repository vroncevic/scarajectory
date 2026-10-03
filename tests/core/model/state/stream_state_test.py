# -*- coding: UTF-8 -*-

'''
Module
    stream_state_test.py
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
    Unit tests for StreamState motion streaming status enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_state import StreamState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamStateTestCase(TestCase):
    '''
        Tests for StreamState enumeration values and membership.

        It defines:

            :methods:
                | test_enumeration_values - Verifies string representation of streaming states.
                | test_enumeration_members - Verifies all expected members are defined.
    '''

    def test_enumeration_values(self) -> None:
        '''
            Verifies string representation of streaming states.

            :exceptions: None.
        '''
        self.assertEqual(StreamState.IDLE.value, 'IDLE')
        self.assertEqual(StreamState.STREAMING.value, 'STREAMING')
        self.assertEqual(StreamState.PAUSED.value, 'PAUSED')
        self.assertEqual(StreamState.STOPPED.value, 'STOPPED')
        self.assertEqual(StreamState.COMPLETED.value, 'COMPLETED')
        self.assertEqual(StreamState.ERROR.value, 'ERROR')

    def test_enumeration_members(self) -> None:
        '''
            Verifies all expected members are defined.

            :exceptions: None.
        '''
        members = list(StreamState)
        self.assertEqual(len(members), 6)
        self.assertIn(StreamState.IDLE, members)
        self.assertIn(StreamState.STREAMING, members)
        self.assertIn(StreamState.PAUSED, members)
        self.assertIn(StreamState.STOPPED, members)
        self.assertIn(StreamState.COMPLETED, members)
        self.assertIn(StreamState.ERROR, members)


if __name__ == '__main__':
    main()
