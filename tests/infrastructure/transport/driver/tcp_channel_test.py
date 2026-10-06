# -*- coding: UTF-8 -*-

'''
Module
    tcp_channel_test.py
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
    Unit testing for TcpChannelDriver component.
'''

from __future__ import annotations

from socket import AF_INET, SOCK_STREAM, socket as Socket
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.driver.tcp_channel import TcpChannelDriver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TcpChannelDriverTestCase(TestCase):
    '''
        Test cases verifying TcpChannelDriver socket lifecycle, I/O, and errors.

        It defines:

            :methods:
                | test_lifecycle_when_not_connected - Tests behavior of closed channel.
                | test_open_channel_and_data_exchange - Tests real loopback transfer.
                | test_disconnect_and_timeout - Tests remote peer disconnect and timeout.
                | test_socket_exception_branches - Tests mocked errors and fallbacks.
    '''

    def test_lifecycle_when_not_connected(self) -> None:
        '''Verifies channel state, name, and read/write when not connected.'''
        driver = TcpChannelDriver()
        self.assertFalse(driver.is_open())
        self.assertEqual(driver.channel_name(), 'TCP')
        self.assertEqual(driver.read_bytes(10), b'')
        driver.write_bytes(b'noop')
        driver.close_channel()
        self.assertFalse(driver.is_open())

    def test_open_channel_and_data_exchange(self) -> None:
        '''Verifies connecting to a loopback server, sending data, and closing.'''
        server_sock = Socket(AF_INET, SOCK_STREAM)
        server_sock.bind(('127.0.0.1', 0))
        server_sock.listen(1)
        port: int = server_sock.getsockname()[1]

        driver = TcpChannelDriver()
        config = StreamConfig(
            port=f'127.0.0.1:{port}',
            baudrate=115200,
            timeout=0.2,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        driver.open_channel(config)
        client_conn, _ = server_sock.accept()

        self.assertTrue(driver.is_open())
        self.assertIn('127.0.0.1', driver.channel_name())

        driver.write_bytes(b'PING')
        self.assertEqual(client_conn.recv(4), b'PING')

        client_conn.sendall(b'PONG')
        self.assertEqual(driver.read_bytes(4), b'PONG')

        driver.close_channel()
        client_conn.close()
        server_sock.close()
        self.assertFalse(driver.is_open())

    def test_disconnect_and_timeout(self) -> None:
        '''Verifies peer disconnect raises reset error and timeout returns empty bytes.'''
        server_sock = Socket(AF_INET, SOCK_STREAM)
        server_sock.bind(('127.0.0.1', 0))
        server_sock.listen(1)
        port: int = server_sock.getsockname()[1]

        driver = TcpChannelDriver()
        config = StreamConfig(
            port=f'127.0.0.1:{port}',
            baudrate=115200,
            timeout=0.01,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        driver.open_channel(config)
        client_conn, _ = server_sock.accept()

        self.assertEqual(driver.read_bytes(10), b'')

        client_conn.close()
        server_sock.close()

        with self.assertRaises(ConnectionResetError):
            driver.read_bytes(5)

        driver.close_channel()
        self.assertFalse(driver.is_open())

    @patch('scarajectory.infrastructure.transport.driver.tcp_channel.Socket')
    def test_socket_exception_branches(
        self, mock_socket_cls: MagicMock
    ) -> None:
        '''Verifies port parsing fallbacks, socket errors, and channel name exceptions.'''
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        mock_sock.connect.side_effect = ConnectionRefusedError('Refused')

        driver = TcpChannelDriver()
        config_bad_port = StreamConfig(
            port='127.0.0.1:invalid_num',
            baudrate=115200,
            timeout=-1.0,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        with self.assertRaises(ConnectionRefusedError):
            driver.open_channel(config_bad_port)

        mock_sock.close.assert_called_once()

        mock_sock.connect.side_effect = None
        driver.open_channel(config_bad_port)

        mock_sock.getpeername.side_effect = OSError('No peer')
        self.assertEqual(driver.channel_name(), 'TCP')

        mock_sock.shutdown.side_effect = OSError('Shutdown error')
        mock_sock.close.side_effect = OSError('Close error')
        driver.close_channel()
        self.assertFalse(driver.is_open())


if __name__ == '__main__':
    main()
