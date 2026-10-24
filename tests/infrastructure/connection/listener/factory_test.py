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
    Unit tests for StreamTransportListenerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.connection.listener.factory import StreamTransportListenerFactory
from scarajectory.infrastructure.connection.listener.listener import StreamTransportListener
from scarajectory.infrastructure.connection.receiver.ibytes_receiver import IStreamBytesReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportListenerFactoryTestCase(TestCase):
    '''
        Tests StreamTransportListenerFactory instantiation and versioning.

        It defines:

            :methods:
                | test_factory_create - Verifies instantiating listener with receiver.
                | test_factory_version - Verifies factory version query.
    '''

    def test_factory_create(self) -> None:
        '''
            Verifies factory creation of StreamTransportListener with receiver.

            :exceptions: None.
        '''
        mock_receiver = MagicMock(spec=IStreamBytesReceiver)
        mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        instance = StreamTransportListenerFactory.create(
            dispatcher=mock_dispatcher,
            bytes_receiver=mock_receiver,
        )
        self.assertIsInstance(instance, StreamTransportListener)

    def test_factory_version(self) -> None:
        '''
            Verifies factory version query.

            :exceptions: None.
        '''
        self.assertEqual(
            StreamTransportListenerFactory.get_version(), '1.0.3'
        )


if __name__ == '__main__':
    main()
