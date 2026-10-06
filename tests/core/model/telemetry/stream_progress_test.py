# -*- coding: UTF-8 -*-

'''
Module
    stream_progress_test.py
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
    Unit tests for StreamProgress immutable progress metrics container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamProgressTestCase(TestCase):
    '''
        Tests for StreamProgress metrics container.

        It defines:

            :methods:
                | test_progress_creation - Verifies progress attributes assignment.
                | test_progress_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_progress_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        progress = StreamProgress(
            state=StreamState.STREAMING,
            total_waypoints=50,
            sent_waypoints=25,
            completed_waypoints=24,
            failed_waypoints=0,
            current_line='G1 X100 Y50',
            error_message='',
            elapsed_seconds=3.2,
            percentage=50.0,
        )
        self.assertEqual(progress.state, StreamState.STREAMING)
        self.assertEqual(progress.total_waypoints, 50)
        self.assertEqual(progress.sent_waypoints, 25)
        self.assertEqual(progress.completed_waypoints, 24)
        self.assertEqual(progress.failed_waypoints, 0)
        self.assertEqual(progress.current_line, 'G1 X100 Y50')
        self.assertEqual(progress.error_message, '')
        self.assertAlmostEqual(progress.elapsed_seconds, 3.2)
        self.assertAlmostEqual(progress.percentage, 50.0)

    def test_progress_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen StreamProgress raises FrozenInstanceError.

            :exceptions: None.
        '''
        progress = StreamProgress(
            state=StreamState.IDLE,
            total_waypoints=0,
            sent_waypoints=0,
            completed_waypoints=0,
            failed_waypoints=0,
            current_line='',
            error_message='',
            elapsed_seconds=0.0,
            percentage=0.0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(progress, 'percentage', 10.0)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical StreamProgress instances.

            :exceptions: None.
        '''
        p1 = StreamProgress(
            state=StreamState.COMPLETED,
            total_waypoints=10,
            sent_waypoints=10,
            completed_waypoints=10,
            failed_waypoints=0,
            current_line='END',
            error_message='',
            elapsed_seconds=1.5,
            percentage=100.0,
        )
        p2 = StreamProgress(
            state=StreamState.COMPLETED,
            total_waypoints=10,
            sent_waypoints=10,
            completed_waypoints=10,
            failed_waypoints=0,
            current_line='END',
            error_message='',
            elapsed_seconds=1.5,
            percentage=100.0,
        )
        self.assertEqual(p1, p2)


if __name__ == '__main__':
    main()
