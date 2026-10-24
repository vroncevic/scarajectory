# -*- coding: UTF-8 -*-

'''
Module
    drainer_test.py
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
    Unit tests for QueueDrainer implementation.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.drainer.drainer import QueueDrainer
from scarajectory.infrastructure.worker.drainer.idrainer import IQueueDrainer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueDrainerTestCase(TestCase):
    '''
        Unit tests for QueueDrainer.

        It defines:

            :methods:
                | setUp - Prepares test instance and mock collaborators.
                | test_structural_conformance - Verifies conformance to IQueueDrainer.
                | test_is_queue_empty - Verifies empty check logic.
                | test_drain_queue_success - Verifies draining and state transition.
                | test_drain_queue_stopped - Verifies early termination on stop event.
                | test_drain_queue_waits_for_completion - Verifies sleep in drain_queue loop.
    '''

    def setUp(self) -> None:
        '''
            Prepares drainer and mock collaborators.

            :exceptions: None.
        '''
        self.mock_state = MagicMock(spec=IStreamStateMachine)
        self.mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        self.config = StreamPacingConfig(
            poll_delay=0.001,
            send_delay=0.001,
            throttle_delay=0.001,
        )
        self.drainer = QueueDrainer(
            state_controller=self.mock_state,
            observer_dispatcher=self.mock_dispatcher,
            pacing_config=self.config,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies drainer satisfies IQueueDrainer structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.drainer, IQueueDrainer)

    def test_is_queue_empty(self) -> None:
        '''
            Verifies is_queue_empty logic based on completed + failed count.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=5,
            done_count=3,
            failed_count=2,
            remote_queue_depth=0,
            start_time=100.0,
        )
        self.assertTrue(self.drainer.is_queue_empty(session=session, total_items=5))
        self.assertFalse(self.drainer.is_queue_empty(session=session, total_items=6))

    def test_drain_queue_success(self) -> None:
        '''
            Verifies queue draining and completed state transition.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=2,
            done_count=2,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )
        stop_event = Event()
        self.drainer.drain_queue(
            session=session,
            total_items=2,
            stop_event=stop_event,
        )
        self.mock_state.transition_to.assert_called_with(StreamState.COMPLETED)
        self.mock_dispatcher.notify_progress.assert_called_once()
        self.mock_dispatcher.notify_log.assert_called_once()

    def test_drain_queue_stopped(self) -> None:
        '''
            Verifies drain_queue aborts when stop_event is pre-set.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=5,
            done_count=0,
            failed_count=0,
            remote_queue_depth=5,
            start_time=100.0,
        )
        stop_event = Event()
        stop_event.set()
        self.drainer.drain_queue(
            session=session,
            total_items=5,
            stop_event=stop_event,
        )
        self.mock_state.transition_to.assert_not_called()

    def test_drain_queue_waits_for_completion(self) -> None:
        '''
            Verifies drain_queue executes sleep loop until queue is empty.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=2,
            done_count=1,
            failed_count=0,
            remote_queue_depth=1,
            start_time=100.0,
        )
        stop_event = Event()

        def complete_item(_delay: float) -> None:
            session.done_count = 2

        with patch(
            'scarajectory.infrastructure.worker.drainer.drainer.sleep',
            side_effect=complete_item,
        ):
            self.drainer.drain_queue(
                session=session,
                total_items=2,
                stop_event=stop_event,
            )
        self.mock_state.transition_to.assert_called_with(StreamState.COMPLETED)


if __name__ == '__main__':
    main()
