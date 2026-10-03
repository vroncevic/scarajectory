# -*- coding: UTF-8 -*-

'''
Module
    stream_observer_dispatcher_test.py
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
    Unit tests for StreamObserverDispatcher and StreamObserverDispatcherFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.core.service.streaming.istream_dispatcher import IStreamDispatcher
from scarajectory.infrastructure.streaming.observer.istream_observer_registry import IStreamObserverRegistry
from scarajectory.infrastructure.streaming.observer.istream_telemetry_notifier import IStreamTelemetryNotifier
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher import StreamObserverDispatcher
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamObserverDispatcherTestCase(TestCase):
    '''
    Tests StreamObserverDispatcher subscription delegation and telemetry broadcasting.

    It defines:

        :methods:
            | setUp - Initializes mock registry, mock notifier, and dispatcher fixtures.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_set_observer - Verifies delegating set_observer to registry.
            | test_attach_observer - Verifies delegating attach_observer to registry.
            | test_detach_observer - Verifies delegating detach_observer to registry.
            | test_has_observers - Verifies checking observers through registry.
            | test_notify_log - Verifies delegating notify_log to notifier.
            | test_notify_progress - Verifies delegating notify_progress to notifier.
            | test_factory_create - Verifies factory empty creation.
            | test_factory_create_with_observer - Verifies factory creation with initial observer.
            | test_factory_version - Verifies factory version query.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.mock_registry = MagicMock(spec=IStreamObserverRegistry)
        self.mock_notifier = MagicMock(spec=IStreamTelemetryNotifier)
        self.dispatcher = StreamObserverDispatcher(
            registry=self.mock_registry,
            notifier=self.mock_notifier,
        )
        self.mock_observer = MagicMock(spec=IObserver)

    def test_satisfies_protocol(self) -> None:
        '''
        Verifies structural typing contract for IStreamDispatcher.
        '''
        self.assertIsInstance(self.dispatcher, IStreamDispatcher)

    def test_set_observer(self) -> None:
        '''
        Verifies set_observer delegates to registry.
        '''
        self.dispatcher.set_observer(self.mock_observer)
        self.mock_registry.set_observer.assert_called_once_with(
            self.mock_observer
        )

    def test_attach_observer(self) -> None:
        '''
        Verifies attach_observer delegates to registry.
        '''
        self.dispatcher.attach_observer(self.mock_observer)
        self.mock_registry.attach_observer.assert_called_once_with(
            self.mock_observer
        )

    def test_detach_observer(self) -> None:
        '''
        Verifies detach_observer delegates to registry.
        '''
        self.dispatcher.detach_observer(self.mock_observer)
        self.mock_registry.detach_observer.assert_called_once_with(
            self.mock_observer
        )

    def test_has_observers(self) -> None:
        '''
        Verifies has_observers and has_observer query registry.
        '''
        self.mock_registry.get_observers.return_value = ()
        self.assertFalse(self.dispatcher.has_observers())
        self.assertFalse(self.dispatcher.has_observer())

        self.mock_registry.get_observers.return_value = (self.mock_observer,)
        self.assertTrue(self.dispatcher.has_observers())
        self.assertTrue(self.dispatcher.has_observer())

    def test_notify_log(self) -> None:
        '''
        Verifies notify_log delegates to notifier.
        '''
        self.dispatcher.notify_log('Hello', is_outgoing=True)
        self.mock_notifier.notify_log.assert_called_once_with(
            'Hello', is_outgoing=True
        )

    def test_notify_progress(self) -> None:
        '''
        Verifies notify_progress delegates to notifier.
        '''
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
            current_line='G28',
            error='',
        )
        self.mock_notifier.notify_progress.assert_called_once_with(
            state=StreamState.IDLE,
            session=session,
            current_line='G28',
            error='',
        )

    def test_factory_create(self) -> None:
        '''
        Verifies factory default creation creates functional dispatcher.
        '''
        instance = StreamObserverDispatcherFactory.create()
        self.assertIsInstance(instance, StreamObserverDispatcher)
        self.assertFalse(instance.has_observers())

    def test_factory_create_with_observer(self) -> None:
        '''
        Verifies factory creation with initial observer.
        '''
        instance = StreamObserverDispatcherFactory.create_with_observer(
            self.mock_observer
        )
        self.assertIsInstance(instance, StreamObserverDispatcher)
        self.assertTrue(instance.has_observers())

    def test_factory_version(self) -> None:
        '''
        Verifies factory version string.
        '''
        self.assertEqual(StreamObserverDispatcherFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
