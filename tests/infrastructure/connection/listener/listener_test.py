# -*- coding: UTF-8 -*-

'''
Module
    listener_test.py
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
    Unit tests for StreamTransportListener adapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.listener.itransport_listener import ITransportListener

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
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


class StreamTransportListenerTestCase(TestCase):
    '''
        Tests StreamTransportListener event routing to bytes receiver and dispatcher.

        It defines:

            :methods:
                | setUp - Initializes mock receivers and listener fixture.
                | test_satisfies_protocol - Verifies structural typing contracts.
                | test_on_bytes_received - Verifies routing inbound bytes to receiver.
                | test_on_log_emitted - Verifies routing log message to dispatcher.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.

            :exceptions: None.
        '''
        self.mock_receiver = MagicMock(spec=IStreamBytesReceiver)
        self.mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        self.listener: StreamTransportListener = StreamTransportListener(
            dispatcher=self.mock_dispatcher,
            bytes_receiver=self.mock_receiver,
        )

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies structural typing contract for ITransportListener.

            :exceptions: None.
        '''
        self.assertIsInstance(self.listener, ITransportListener)

    def test_on_bytes_received(self) -> None:
        '''
            Verifies on_bytes_received routes payload to bytes receiver.

            :exceptions: None.
        '''
        self.listener.on_bytes_received(b'\xAA\xBB')
        self.mock_receiver.handle_incoming_bytes.assert_called_once_with(b'\xAA\xBB')

    def test_on_log_emitted(self) -> None:
        '''
            Verifies on_log_emitted routes log message to dispatcher.

            :exceptions: None.
        '''
        self.listener.on_log_emitted('Connected', is_tx=False)
        self.mock_dispatcher.notify_log.assert_called_once_with(
            'Connected', is_outgoing=False
        )

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(self.listener.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
