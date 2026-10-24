# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
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
    Unit tests for StreamObserverRegistry subscriber management.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.core.service.streaming.observer.iregistry import IStreamObserverRegistry
from scarajectory.infrastructure.streaming.observer.registry import StreamObserverRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamObserverRegistryTestCase(TestCase):
    '''
    Tests StreamObserverRegistry registration, query, and lifecycle methods.

    It defines:

        :methods:
            | setUp - Initializes registry and mock observer fixtures.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_set_observer - Verifies replacing observer set with single observer.
            | test_attach_observer - Verifies registering unique observer instances.
            | test_detach_observer - Verifies removing existing observer instances.
            | test_detach_non_existing - Verifies detachment safety when observer missing.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.registry: StreamObserverRegistry = StreamObserverRegistry()
        self.mock_observer_1 = MagicMock(spec=IObserver)
        self.mock_observer_2 = MagicMock(spec=IObserver)

    def test_satisfies_protocol(self) -> None:
        '''
        Verifies structural typing contract for IStreamObserverRegistry.
        '''
        self.assertIsInstance(self.registry, IStreamObserverRegistry)

    def test_set_observer(self) -> None:
        '''
        Verifies set_observer replaces any existing observers with single observer.
        '''
        self.registry.attach_observer(self.mock_observer_1)
        self.registry.set_observer(self.mock_observer_2)

        observers = self.registry.get_observers()
        self.assertEqual(len(observers), 1)
        self.assertEqual(observers[0], self.mock_observer_2)

    def test_attach_observer(self) -> None:
        '''
        Verifies attach_observer appends observer and ignores duplicate registrations.
        '''
        self.registry.attach_observer(self.mock_observer_1)
        self.registry.attach_observer(self.mock_observer_2)
        self.registry.attach_observer(self.mock_observer_1)

        observers = self.registry.get_observers()
        self.assertEqual(len(observers), 2)
        self.assertEqual(observers, (self.mock_observer_1, self.mock_observer_2))

    def test_detach_observer(self) -> None:
        '''
        Verifies detach_observer removes registered observer.
        '''
        self.registry.attach_observer(self.mock_observer_1)
        self.registry.attach_observer(self.mock_observer_2)
        self.registry.detach_observer(self.mock_observer_1)

        observers = self.registry.get_observers()
        self.assertEqual(len(observers), 1)
        self.assertEqual(observers, (self.mock_observer_2,))

    def test_detach_non_existing(self) -> None:
        '''
        Verifies detach_observer does not fail when observer is not registered.
        '''
        self.registry.attach_observer(self.mock_observer_1)
        self.registry.detach_observer(self.mock_observer_2)

        observers = self.registry.get_observers()
        self.assertEqual(len(observers), 1)
        self.assertEqual(observers, (self.mock_observer_1,))


if __name__ == '__main__':
    main()
