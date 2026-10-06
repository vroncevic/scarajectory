# -*- coding: UTF-8 -*-

'''
Module
    stream_ascii_transport_listener_test.py
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
    Unit tests for StreamAsciiTransportListener and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.connection.istream_line_receiver import IStreamLineReceiver
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener
from scarajectory.infrastructure.transport.listener.stream_ascii_transport_listener import StreamAsciiTransportListener
from scarajectory.infrastructure.transport.listener.stream_ascii_transport_listener_factory import StreamAsciiTransportListenerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamAsciiTransportListenerTestCase(TestCase):
    '''
    Tests StreamAsciiTransportListener event routing to line receiver and dispatcher.

    It defines:

        :methods:
            | setUp - Initializes mock receivers and listener fixture.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_on_line_received - Verifies routing inbound line to receiver.
            | test_on_bytes_received - Verifies no-op on raw bytes.
            | test_on_log_emitted - Verifies routing log message to dispatcher.
            | test_factory - Verifies factory creation and version query.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.mock_receiver = MagicMock(spec=IStreamLineReceiver)
        self.mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        self.listener: StreamAsciiTransportListener = (
            StreamAsciiTransportListenerFactory.create(
                line_receiver=self.mock_receiver,
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
        Verifies on_line_received routes line to line receiver.
        '''
        self.listener.on_line_received('ok\n')
        self.mock_receiver.handle_incoming_line.assert_called_once_with('ok\n')

    def test_on_bytes_received(self) -> None:
        '''
        Verifies on_bytes_received is safe no-op for ASCII mode.
        '''
        self.listener.on_bytes_received(b'\x01\x02')
        self.mock_receiver.handle_incoming_line.assert_not_called()

    def test_on_log_emitted(self) -> None:
        '''
        Verifies on_log_emitted routes log message to dispatcher.
        '''
        self.listener.on_log_emitted('Connected', is_tx=False)
        self.mock_dispatcher.notify_log.assert_called_once_with(
            'Connected', is_outgoing=False
        )

    def test_factory(self) -> None:
        '''
        Verifies factory creation and version query.
        '''
        instance = StreamAsciiTransportListenerFactory.create(
            line_receiver=self.mock_receiver,
            dispatcher=self.mock_dispatcher,
        )
        self.assertIsInstance(instance, StreamAsciiTransportListener)
        self.assertEqual(
            StreamAsciiTransportListenerFactory.get_version(), '1.0.3'
        )


if __name__ == '__main__':
    main()
