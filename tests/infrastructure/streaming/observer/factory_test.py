# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for ObserverFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.observer.iregistry import IStreamObserverRegistry
from scarajectory.infrastructure.streaming.observer.factory import ObserverFactory
from scarajectory.infrastructure.streaming.observer.provides import ObserverProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestObserverFactory(TestCase):
    '''
    Test cases verifying ObserverFactory.

    It defines:

        :methods:
            | test_create - Tests factory creates ObserverProvides with valid ports.
            | test_get_version - Tests factory version string.
    '''

    def test_create(self) -> None:
        '''
            Tests factory creation of ObserverProvides.

            :exceptions: None.
        '''
        provides: ObserverProvides = ObserverFactory.create()
        self.assertIsInstance(provides, ObserverProvides)
        self.assertIsInstance(provides.stream_observer_registry, IStreamObserverRegistry)
        self.assertIsInstance(provides.stream_observer_dispatcher, IStreamObserverDispatcher)

    def test_get_version(self) -> None:
        '''
            Tests version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(ObserverFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
