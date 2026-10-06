# -*- coding: UTF-8 -*-

'''
Module
    session_factory_test.py
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
    Unit tests for SessionFactory creation service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.session_factory import SessionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSessionFactory(TestCase):
    '''
        Test cases verifying SessionFactory.

        It defines:

            :methods:
                | test_create_default - Verifies default session creation.
                | test_create_with_parameters - Verifies session creation with custom arguments.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create_default(self) -> None:
        '''
            Verifies default Session creation.

            :exceptions: None.
        '''
        session: StreamSession = SessionFactory.create()
        self.assertEqual(session.sent_count, 0)
        self.assertEqual(session.done_count, 0)
        self.assertEqual(session.failed_count, 0)
        self.assertEqual(len(session.waypoints), 0)

    def test_create_with_parameters(self) -> None:
        '''
            Verifies Session creation with explicit parameters.

            :exceptions: None.
        '''
        wp = Waypoint(x=10.0, y=20.0, z=5.0, phi=0.0, speed=100.0)
        session: StreamSession = SessionFactory.create(
            waypoints=[wp],
            sent_count=1,
            done_count=1,
            failed_count=0,
            remote_queue_depth=3,
            start_time=123.456,
        )
        self.assertEqual(session.sent_count, 1)
        self.assertEqual(session.done_count, 1)
        self.assertEqual(session.failed_count, 0)
        self.assertEqual(session.remote_queue_depth, 3)
        self.assertEqual(session.start_time, 123.456)
        self.assertEqual(len(session.waypoints), 1)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns non-empty string.

            :exceptions: None.
        '''
        self.assertEqual(SessionFactory.get_version(), __version__)


if __name__ == '__main__':
    main()
