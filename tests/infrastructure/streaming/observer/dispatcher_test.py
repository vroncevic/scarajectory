# -*- coding: UTF-8 -*-

'''
Module
    dispatcher_test.py
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
    Unit tests for StreamObserverDispatcher telemetry broadcasting.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.core.service.streaming.observer.iregistry import IStreamObserverRegistry
from scarajectory.infrastructure.streaming.observer.dispatcher import StreamObserverDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamObserverDispatcherTestCase(TestCase):
    '''
    Tests StreamObserverDispatcher telemetry progress and serial log broadcasting.

    It defines:

        :methods:
            | setUp - Initializes mock registry and dispatcher fixtures.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_notify_log - Verifies broadcasting log message to registered observers.
            | test_notify_progress - Verifies computing metrics and dispatching progress.
            | test_notify_progress_no_observers - Verifies early return when no observers registered.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.mock_registry = MagicMock(spec=IStreamObserverRegistry)
        self.mock_observer = MagicMock(spec=IObserver)
        self.mock_registry.get_observers.return_value = (self.mock_observer,)
        self.dispatcher = StreamObserverDispatcher(registry=self.mock_registry)

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies structural typing contract for IStreamObserverDispatcher.

            :exceptions: None.
        '''
        self.assertIsInstance(self.dispatcher, IStreamObserverDispatcher)

    def test_notify_log(self) -> None:
        '''
            Verifies broadcasting log message to all registered observers.

            :exceptions: None.
        '''
        self.dispatcher.notify_log('Test Message', is_outgoing=True)
        self.mock_observer.on_serial_log.assert_called_once_with(
            'Test Message', is_outgoing=True
        )

    def test_notify_progress(self) -> None:
        '''
            Verifies computing metrics and dispatching progress to observers.

            :exceptions: None.
        '''
        waypoint = TrajectoryWaypoint(
            x=10.0,
            y=20.0,
            z=0.0,
            phi=0.0,
            speed=100.0,
            name='P1',
            command='G1 X10 Y20',
        )
        session = StreamSession(
            waypoints=[waypoint],
            sent_count=1,
            done_count=1,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )
        self.dispatcher.notify_progress(
            state=StreamState.STREAMING,
            session=session,
            current_line='G1 X10 Y20',
            error='',
        )
        self.mock_observer.on_stream_progress.assert_called_once()

    def test_notify_progress_no_observers(self) -> None:
        '''
            Verifies early return when no observers registered.

            :exceptions: None.
        '''
        self.mock_registry.get_observers.return_value = ()
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        self.dispatcher.notify_progress(
            state=StreamState.IDLE,
            session=session,
            current_line='',
            error='',
        )
        self.mock_observer.on_stream_progress.assert_not_called()


if __name__ == '__main__':
    main()
