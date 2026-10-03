# -*- coding: UTF-8 -*-

'''
Module
    stream_session_test.py
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
    Unit tests for StreamSession streaming execution progress tracking container.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamSessionTestCase(TestCase):
    '''
        Tests for StreamSession mutable state container.

        It defines:

            :methods:
                | test_session_initialization - Verifies attributes set upon initialization.
                | test_session_mutation - Verifies updating counters during streaming execution.
    '''

    def test_session_initialization(self) -> None:
        '''
            Verifies attributes set upon initialization.

            :exceptions: None.
        '''
        waypoint = Waypoint(x=10.0, y=20.0, z=5.0, speed=25.0)
        session = StreamSession(
            waypoints=[waypoint],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )
        self.assertEqual(len(session.waypoints), 1)
        self.assertEqual(session.waypoints[0].x, 10.0)
        self.assertEqual(session.sent_count, 0)
        self.assertEqual(session.done_count, 0)
        self.assertEqual(session.failed_count, 0)
        self.assertEqual(session.remote_queue_depth, 0)
        self.assertEqual(session.start_time, 100.0)

    def test_session_mutation(self) -> None:
        '''
            Verifies updating counters during streaming execution.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        session.sent_count += 5
        session.done_count += 4
        session.failed_count += 1
        session.remote_queue_depth = 2

        self.assertEqual(session.sent_count, 5)
        self.assertEqual(session.done_count, 4)
        self.assertEqual(session.failed_count, 1)
        self.assertEqual(session.remote_queue_depth, 2)


if __name__ == '__main__':
    main()
