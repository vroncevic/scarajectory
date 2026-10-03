# -*- coding: UTF-8 -*-

'''
Module
    stream_binary_transport_listener_test.py
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
    Unit tests for StreamBinaryTransportListener and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.istream_bytes_receiver import IStreamBytesReceiver
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener
from scarajectory.infrastructure.transport.listener.stream_binary_transport_listener import StreamBinaryTransportListener
from scarajectory.infrastructure.transport.listener.stream_binary_transport_listener_factory import StreamBinaryTransportListenerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamBinaryTransportListenerTestCase(TestCase):
    '''
    Tests StreamBinaryTransportListener event routing to bytes receiver and dispatcher.

    It defines:

        :methods:
            | setUp - Initializes mock receivers and listener fixture.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_on_line_received - Verifies no-op on text line.
            | test_on_bytes_received - Verifies routing inbound bytes to receiver.
            | test_on_log_emitted - Verifies routing log message to dispatcher.
            | test_factory - Verifies factory creation and version query.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.mock_receiver = MagicMock(spec=IStreamBytesReceiver)
        self.mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        self.listener: StreamBinaryTransportListener = (
            StreamBinaryTransportListenerFactory.create(
                bytes_receiver=self.mock_receiver,
                dispatcher=self.mock_dispatcher,
            )
        )

    def test_satisfies_protocol(self) -> None:
        '''
        Verifies structural typing contract for ITransportListener.
        '''
        self.assertIsInstance(self.listener, ITransportListener)

    def test_on_line_received(self) -> None:
        '''
        Verifies on_line_received is safe no-op for binary mode.
        '''
        self.listener.on_line_received('ignored line')
        self.mock_receiver.handle_incoming_bytes.assert_not_called()

    def test_on_bytes_received(self) -> None:
        '''
        Verifies on_bytes_received routes payload to bytes receiver.
        '''
        self.listener.on_bytes_received(b'\xAA\xBB')
        self.mock_receiver.handle_incoming_bytes.assert_called_once_with(
            b'\xAA\xBB'
        )

    def test_on_log_emitted(self) -> None:
        '''
        Verifies on_log_emitted routes log message to dispatcher.
        '''
        self.listener.on_log_emitted('Frame sent', is_tx=True)
        self.mock_dispatcher.notify_log.assert_called_once_with(
            'Frame sent', is_outgoing=True
        )

    def test_factory(self) -> None:
        '''
        Verifies factory creation and version query.
        '''
        instance = StreamBinaryTransportListenerFactory.create(
            bytes_receiver=self.mock_receiver,
            dispatcher=self.mock_dispatcher,
        )
        self.assertIsInstance(instance, StreamBinaryTransportListener)
        self.assertEqual(
            StreamBinaryTransportListenerFactory.get_version(), '1.0.4'
        )


if __name__ == '__main__':
    main()
