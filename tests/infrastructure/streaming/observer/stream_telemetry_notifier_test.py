# -*- coding: UTF-8 -*-

'''
Module
    stream_telemetry_notifier_test.py
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
    Unit tests for StreamTelemetryNotifier and StreamTelemetryNotifierFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.infrastructure.streaming.observer.istream_observer_registry import IStreamObserverRegistry
from scarajectory.infrastructure.streaming.observer.istream_telemetry_notifier import IStreamTelemetryNotifier
from scarajectory.infrastructure.streaming.observer.stream_telemetry_notifier import StreamTelemetryNotifier
from scarajectory.infrastructure.streaming.observer.stream_telemetry_notifier_factory import StreamTelemetryNotifierFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTelemetryNotifierTestCase(TestCase):
    '''
    Tests StreamTelemetryNotifier log and progress notification dispatching.

    It defines:

        :methods:
            | setUp - Initializes mock registry, mock observers, and notifier fixtures.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_notify_log - Verifies dispatching log messages to all observers.
            | test_notify_progress_without_observers - Verifies early exit when no observers exist.
            | test_notify_progress_with_observers - Verifies progress calculation and dispatch.
            | test_notify_progress_with_zero_start_time - Verifies progress calculation when start time is 0.
            | test_factory - Verifies factory creation and version query.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.mock_registry = MagicMock(spec=IStreamObserverRegistry)
        self.notifier: StreamTelemetryNotifier = (
            StreamTelemetryNotifierFactory.create(self.mock_registry)
        )
        self.mock_observer_1 = MagicMock(spec=IObserver)
        self.mock_observer_2 = MagicMock(spec=IObserver)

    def test_satisfies_protocol(self) -> None:
        '''
        Verifies structural typing contract for IStreamTelemetryNotifier.
        '''
        self.assertIsInstance(self.notifier, IStreamTelemetryNotifier)

    def test_notify_log(self) -> None:
        '''
        Verifies notify_log broadcasts messages to all registered observers.
        '''
        self.mock_registry.get_observers.return_value = (
            self.mock_observer_1,
            self.mock_observer_2,
        )

        self.notifier.notify_log('Command sent', is_outgoing=True)

        self.mock_observer_1.on_serial_log.assert_called_once_with(
            'Command sent', is_outgoing=True
        )
        self.mock_observer_2.on_serial_log.assert_called_once_with(
            'Command sent', is_outgoing=True
        )

    def test_notify_progress_without_observers(self) -> None:
        '''
        Verifies notify_progress exits early if no observers are registered.
        '''
        self.mock_registry.get_observers.return_value = ()
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=0.0, speed=100.0)],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )

        self.notifier.notify_progress(
            state=StreamState.STREAMING,
            session=session,
            current_line='G1 X10 Y20',
        )

        self.mock_observer_1.on_stream_progress.assert_not_called()

    def test_notify_progress_with_observers(self) -> None:
        '''
        Verifies notify_progress computes metrics and broadcasts StreamProgress.
        '''
        self.mock_registry.get_observers.return_value = (self.mock_observer_1,)
        wp1 = Waypoint(x=10.0, y=20.0, z=0.0, speed=100.0)
        wp2 = Waypoint(x=30.0, y=40.0, z=0.0, speed=100.0)
        session = StreamSession(
            waypoints=[wp1, wp2],
            sent_count=2,
            done_count=1,
            failed_count=0,
            remote_queue_depth=0,
            start_time=1.0,
        )

        self.notifier.notify_progress(
            state=StreamState.STREAMING,
            session=session,
            current_line='G1 X30 Y40',
            error='',
        )

        self.mock_observer_1.on_stream_progress.assert_called_once()
        progress: StreamProgress = (
            self.mock_observer_1.on_stream_progress.call_args[0][0]
        )
        self.assertEqual(progress.state, StreamState.STREAMING)
        self.assertEqual(progress.total_waypoints, 2)
        self.assertEqual(progress.sent_waypoints, 2)
        self.assertEqual(progress.completed_waypoints, 1)
        self.assertEqual(progress.failed_waypoints, 0)
        self.assertEqual(progress.current_line, 'G1 X30 Y40')
        self.assertEqual(progress.percentage, 50.0)
        self.assertGreater(progress.elapsed_seconds, 0.0)

    def test_notify_progress_with_zero_start_time(self) -> None:
        '''
        Verifies notify_progress computes 0.0 elapsed seconds when start_time is zero.
        '''
        self.mock_registry.get_observers.return_value = (self.mock_observer_1,)
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )

        self.notifier.notify_progress(
            state=StreamState.IDLE,
            session=session,
        )

        self.mock_observer_1.on_stream_progress.assert_called_once()
        progress: StreamProgress = (
            self.mock_observer_1.on_stream_progress.call_args[0][0]
        )
        self.assertEqual(progress.elapsed_seconds, 0.0)
        self.assertEqual(progress.percentage, 0.0)

    def test_factory(self) -> None:
        '''
        Verifies factory creation and version query.
        '''
        notifier = StreamTelemetryNotifierFactory.create(self.mock_registry)
        self.assertIsInstance(notifier, StreamTelemetryNotifier)
        self.assertEqual(StreamTelemetryNotifierFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
