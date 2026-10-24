# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit testing for ObserverProvides container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.observer.iregistry import IStreamObserverRegistry
from scarajectory.infrastructure.streaming.observer.provides import ObserverProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestObserverProvides(TestCase):
    '''
    Test cases verifying ObserverProvides container.

    It defines:

        :methods:
            | test_initialization - Tests attributes and immutability.
    '''

    def test_initialization(self) -> None:
        '''
            Tests initialization and immutability of ObserverProvides.

            :exceptions: None.
        '''
        registry = MagicMock(spec=IStreamObserverRegistry)
        dispatcher = MagicMock(spec=IStreamObserverDispatcher)

        provides = ObserverProvides(
            stream_observer_registry=registry,
            stream_observer_dispatcher=dispatcher,
        )

        self.assertIs(provides.stream_observer_registry, registry)
        self.assertIs(provides.stream_observer_dispatcher, dispatcher)


if __name__ == '__main__':
    main()
