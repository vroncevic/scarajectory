# -*- coding: UTF-8 -*-

'''
Module
    istream_observer_registry_test.py
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
    Unit testing for IStreamObserverRegistry protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.infrastructure.streaming.observer.istream_observer_registry import (
    IStreamObserverRegistry,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingRegistryStub:
    '''Conforming stub implementation satisfying IStreamObserverRegistry.'''

    def set_observer(self, observer: IObserver) -> None:
        '''Sets primary observer.'''
        _ = observer

    def attach_observer(self, observer: IObserver) -> None:
        '''Registers observer.'''
        _ = observer

    def detach_observer(self, observer: IObserver) -> None:
        '''Removes observer.'''
        _ = observer

    def get_observers(self) -> tuple[IObserver, ...]:
        '''Returns registered observers.'''
        return ()


class IncompleteRegistryStub:
    '''Non-conforming stub implementation missing observer methods.'''

    def set_observer(self, observer: IObserver) -> None:
        '''Sets primary observer.'''
        _ = observer

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class StreamObserverRegistryProtocolTestCase(TestCase):
    '''
        Tests IStreamObserverRegistry runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamObserverRegistry protocol.'''
        stub = ConformingRegistryStub()
        self.assertIsInstance(stub, IStreamObserverRegistry)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IStreamObserverRegistry protocol check.'''
        stub = IncompleteRegistryStub()
        self.assertNotIsInstance(stub, IStreamObserverRegistry)


if __name__ == '__main__':
    main()
