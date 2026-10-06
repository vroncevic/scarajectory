# -*- coding: UTF-8 -*-

'''
Module
    binary_queue_drainer_test.py
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
    Unit tests for BinaryQueueDrainer and its factory.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.worker.binary.binary_queue_drainer import BinaryQueueDrainer
from scarajectory.infrastructure.worker.binary.binary_queue_drainer_factory import BinaryQueueDrainerFactory
from scarajectory.infrastructure.worker.binary.ibinary_queue_drainer import IBinaryQueueDrainer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryQueueDrainerTestCase(TestCase):
    '''
        Tests BinaryQueueDrainer execution and completion reporting.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and drainer.
                | test_factory_and_protocol - Tests construction and protocol adherence.
                | test_is_queue_empty - Tests queue empty conditions.
                | test_drain_queue_completed - Tests waiting and completion state transitions.
                | test_drain_queue_stopped - Tests early exit on stop signal.
    '''

    def setUp(self) -> None:
        self.mock_state = MagicMock()
        self.mock_state.state = StreamState.STREAMING
        self.mock_observer = MagicMock()
        self.pacing_config = StreamPacingConfig(
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )
        self.drainer: BinaryQueueDrainer = BinaryQueueDrainerFactory.create(
            state_controller=self.mock_state,
            observer_dispatcher=self.mock_observer,
            pacing_config=self.pacing_config,
        )

    def test_factory_and_protocol(self) -> None:
        '''Tests factory creation and protocol adherence.'''
        self.assertIsInstance(self.drainer, IBinaryQueueDrainer)
        version: str = BinaryQueueDrainerFactory.get_version()
        self.assertEqual(version, '1.0.3')

    def test_is_queue_empty(self) -> None:
        '''Tests is_queue_empty calculation against total items.'''
        session: StreamSession = SessionFactory.create(waypoints=[])
        session.done_count = 2
        session.failed_count = 1
        self.assertTrue(self.drainer.is_queue_empty(session=session, total_items=3))
        self.assertFalse(self.drainer.is_queue_empty(session=session, total_items=4))

    def test_drain_queue_completed(self) -> None:
        '''Tests queue draining until all items are completed.'''
        session: StreamSession = SessionFactory.create(waypoints=[])
        session.done_count = 1
        session.failed_count = 0
        stop_event = Event()

        with patch.object(self.drainer, 'is_queue_empty', side_effect=[False, True]):
            self.drainer.drain_queue(
                session=session,
                total_items=2,
                stop_event=stop_event,
            )

        self.mock_state.set_state.assert_called_once_with(StreamState.COMPLETED)
        self.mock_observer.notify_progress.assert_called_once()
        self.mock_observer.notify_log.assert_called_once()

    def test_drain_queue_stopped(self) -> None:
        '''Tests queue draining when stop_event is already set.'''
        session: StreamSession = SessionFactory.create(waypoints=[])
        session.done_count = 0
        stop_event = Event()
        stop_event.set()

        self.drainer.drain_queue(
            session=session,
            total_items=2,
            stop_event=stop_event,
        )

        self.mock_state.set_state.assert_not_called()
        self.mock_observer.notify_progress.assert_not_called()


if __name__ == '__main__':
    main()
