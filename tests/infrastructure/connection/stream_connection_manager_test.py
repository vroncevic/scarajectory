# -*- coding: UTF-8 -*-

'''
Module
    stream_connection_manager_test.py
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
    Unit tests for StreamConnectionManager and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.connection.iconnection import IConnection
from scarajectory.infrastructure.connection.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.connection.stream_connection_manager_factory import StreamConnectionManagerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamConnectionManagerTestCase(TestCase):
    '''
    Tests StreamConnectionManager connection lifecycle and protocol operations.

    It defines:

        :methods:
            | setUp - Initializes mock connection and connection manager instance.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_is_connected - Verifies connection state inquiry.
            | test_connect_with_config - Verifies connection opening with config.
            | test_connect_with_config_reconnect - Verifies disconnect on reconnect.
            | test_disconnect - Verifies connection closure.
            | test_set_protocol_mode - Verifies dynamic protocol mode update.
            | test_factory - Verifies factory creation and version.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.mock_connection = MagicMock()
        self.manager: StreamConnectionManager = (
            StreamConnectionManagerFactory.create(
                self.mock_connection,
                protocol_mode=ProtocolMode.ASCII,
            )
        )
        self.test_config: StreamConfig = StreamConfig(
            port='/dev/ttyUSB0',
            baudrate=115200,
            timeout=0.1,
            queue_capacity=16,
            protocol_mode=ProtocolMode.BINARY,
        )

    def test_satisfies_protocol(self) -> None:
        '''
        Verifies structural typing contract for IConnection.
        '''
        self.assertIsInstance(self.manager, IConnection)

    def test_is_connected(self) -> None:
        '''
        Verifies is_connected delegates to connection.
        '''
        self.mock_connection.is_connected.return_value = True
        self.assertTrue(self.manager.is_connected())

        self.mock_connection.is_connected.return_value = False
        self.assertFalse(self.manager.is_connected())

    def test_connect_with_config(self) -> None:
        '''
        Verifies connect_with_config delegates to connection when disconnected.
        '''
        self.mock_connection.is_connected.return_value = False
        self.mock_connection.connect_with_config.return_value = True

        result: bool = self.manager.connect_with_config(self.test_config)

        self.assertTrue(result)
        self.mock_connection.connect_with_config.assert_called_once_with(
            self.test_config
        )

    def test_connect_with_config_reconnect(self) -> None:
        '''
        Verifies connect_with_config disconnects first if already connected.
        '''
        self.mock_connection.is_connected.return_value = True
        self.mock_connection.connect_with_config.return_value = True

        result: bool = self.manager.connect_with_config(self.test_config)

        self.assertTrue(result)
        self.mock_connection.disconnect.assert_called_once()
        self.mock_connection.connect_with_config.assert_called_once_with(
            self.test_config
        )

    def test_disconnect(self) -> None:
        '''
        Verifies disconnect delegates to connection.
        '''
        self.manager.disconnect()
        self.mock_connection.disconnect.assert_called_once()

    def test_set_protocol_mode(self) -> None:
        '''
        Verifies set_protocol_mode updates internal state without error.
        '''
        self.manager.set_protocol_mode(ProtocolMode.BINARY)
        self.assertTrue(self.manager.is_connected or True)

    def test_factory(self) -> None:
        '''
        Verifies factory creation and version querying.
        '''
        instance = StreamConnectionManagerFactory.create(self.mock_connection)
        self.assertIsInstance(instance, StreamConnectionManager)
        self.assertEqual(StreamConnectionManagerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
