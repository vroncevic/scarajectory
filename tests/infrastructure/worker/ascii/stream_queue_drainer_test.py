# -*- coding: UTF-8 -*-

'''
Module
    stream_queue_drainer_test.py
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
    Unit tests for StreamQueueDrainer and StreamQueueDrainerFactory.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.worker.ascii.istream_queue_drainer import IStreamQueueDrainer
from scarajectory.infrastructure.worker.ascii.stream_queue_drainer import StreamQueueDrainer
from scarajectory.infrastructure.worker.ascii.stream_queue_drainer_factory import StreamQueueDrainerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamQueueDrainer(TestCase):
    '''
        Test cases verifying queue draining and stream completion operations.
    '''

    def setUp(self) -> None:
        self.mock_state = MagicMock()
        self.mock_observer = MagicMock()
        self.pacing_config = StreamPacingConfig(
            poll_delay=0.001,
            send_delay=0.001,
            throttle_delay=0.001,
        )
        self.drainer: StreamQueueDrainer = StreamQueueDrainerFactory.create(
            state_controller=self.mock_state,
            observer_dispatcher=self.mock_observer,
            pacing_config=self.pacing_config,
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that StreamQueueDrainer implements IStreamQueueDrainer.
        '''
        self.assertIsInstance(self.drainer, IStreamQueueDrainer)

    def test_is_queue_empty_false(self) -> None:
        '''
            Tests is_queue_empty returns False when in-flight waypoints remain.
        '''
        session = StreamSession(
            waypoints=[
                Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0),
                Waypoint(x=30.0, y=40.0, z=0.0, speed=50.0),
            ],
            sent_count=2,
            done_count=1,
            failed_count=0,
            remote_queue_depth=1,
            start_time=0.0,
        )
        self.assertFalse(self.drainer.is_queue_empty(session))

    def test_is_queue_empty_true(self) -> None:
        '''
            Tests is_queue_empty returns True when done+failed equals count.
        '''
        session = StreamSession(
            waypoints=[
                Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0),
                Waypoint(x=30.0, y=40.0, z=0.0, speed=50.0),
            ],
            sent_count=2,
            done_count=1,
            failed_count=1,
            remote_queue_depth=0,
            start_time=0.0,
        )
        self.assertTrue(self.drainer.is_queue_empty(session))

    def test_drain_queue_completes_session(self) -> None:
        '''
            Tests drain_queue waits and marks session COMPLETED.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0)],
            sent_count=1,
            done_count=1,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        stop_event = Event()

        self.drainer.drain_queue(session, stop_event)

        self.mock_state.set_state.assert_called_once_with(
            StreamState.COMPLETED
        )
        self.mock_observer.notify_progress.assert_called_once()
        self.assertEqual(self.mock_observer.notify_log.call_count, 2)

        session_failed = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0)],
            sent_count=1,
            done_count=0,
            failed_count=1,
            remote_queue_depth=0,
            start_time=0.0,
        )
        self.drainer.drain_queue(session_failed, stop_event)
        self.assertEqual(self.mock_observer.notify_log.call_count, 4)

    def test_drain_queue_aborts_on_stop_event(self) -> None:
        '''
            Tests drain_queue aborts when stop_event is set.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0)],
            sent_count=1,
            done_count=0,
            failed_count=0,
            remote_queue_depth=1,
            start_time=0.0,
        )
        stop_event = Event()
        stop_event.set()

        self.drainer.drain_queue(session, stop_event)

        self.mock_state.set_state.assert_not_called()


if __name__ == '__main__':
    main()
