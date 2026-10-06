# -*- coding: UTF-8 -*-

'''
Module
    stream_transport_connection_test.py
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
    Unit tests for StreamTransportConnection and StreamTransportConnectionFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.driver.serial_channel_factory import SerialChannelDriverFactory
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.listener.null_transport_listener import NullTransportListener
from scarajectory.infrastructure.transport.listener.transport_listener_holder import TransportListenerHolder
from scarajectory.infrastructure.transport.stream_transport_connection import StreamTransportConnection
from scarajectory.infrastructure.transport.stream_transport_connection_factory import StreamTransportConnectionFactory
from scarajectory.infrastructure.transport.worker.transport_reader_worker_factory import TransportReaderWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockRecordingListener:
    '''Mock listener recording emitted log entries.'''

    def __init__(self) -> None:
        self.logs: list[tuple[str, bool]] = []
        self.lines: list[str] = []
        self.bytes_data: list[bytes] = []

    def on_line_received(self, line: str) -> None:
        '''Records received text line.'''
        self.lines.append(line)

    def on_bytes_received(self, data: bytes) -> None:
        '''Records received binary data.'''
        self.bytes_data.append(data)

    def on_log_emitted(self, message: str, is_sent: bool) -> None:
        '''Records emitted log message with sent flag.'''
        self.logs.append((message, is_sent))


class TestStreamTransportConnection(TestCase):
    '''Test suite verifying StreamTransportConnection lifecycle and factory operations.'''

    def test_initial_state_not_connected(self) -> None:
        '''Tests that newly constructed connection reports not connected.'''
        driver = SerialChannelDriverFactory.create()
        listener = NullTransportListener()
        connection = StreamTransportConnectionFactory.create(
            driver=driver,
            listener=listener,
        )
        self.assertFalse(connection.is_connected())
        self.assertIsInstance(connection, IStreamTransportConnection)

    def test_disconnect_on_closed_channel(self) -> None:
        '''Tests that disconnect on an unopened connection executes safely.'''
        driver = SerialChannelDriverFactory.create()
        listener = NullTransportListener()
        connection = StreamTransportConnectionFactory.create(
            driver=driver,
            listener=listener,
        )
        connection.disconnect()
        self.assertFalse(connection.is_connected())

    def test_set_listener(self) -> None:
        '''Tests updating the active event listener.'''
        driver = SerialChannelDriverFactory.create()
        initial_listener = TransportListenerHolder(NullTransportListener())
        connection = StreamTransportConnectionFactory.create(
            driver=driver,
            listener=initial_listener,
        )
        new_listener = MockRecordingListener()
        connection.set_listener(new_listener)
        connection._listener = NullTransportListener()
        connection.set_listener(new_listener)
        self.assertFalse(connection.is_connected())

    def test_failed_connect_emits_log(self) -> None:
        '''Tests that connect_with_config emits error log when driver cannot open invalid port.'''
        driver = SerialChannelDriverFactory.create()
        listener = MockRecordingListener()
        connection = StreamTransportConnectionFactory.create(
            driver=driver,
            listener=listener,
        )
        config = StreamConfig(
            port='INVALID_PORT_PATH_FOR_TEST_123',
            baudrate=115200,
            timeout=1.0,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        success = connection.connect_with_config(config)
        self.assertFalse(success)
        self.assertFalse(connection.is_connected())
        self.assertTrue(any('[ERR]' in log[0] for log in listener.logs))

    def test_successful_connect_and_disconnect(self) -> None:
        '''Tests full successful connect, reader start, and clean disconnect lifecycle.'''
        mock_driver = MagicMock()
        mock_driver.is_open.return_value = True
        mock_driver.channel_name.return_value = 'MOCK_PORT'
        mock_worker = MagicMock()
        mock_worker_factory = MagicMock()
        mock_worker_factory.create.return_value = mock_worker

        listener = MockRecordingListener()
        connection = StreamTransportConnection(
            driver=mock_driver,
            listener=listener,
            worker_factory=mock_worker_factory,
        )
        mock_worker.run.side_effect = (
            lambda: connection._stop_event.wait(timeout=2.0)
        )
        config = StreamConfig(
            port='/dev/ttyUSB0',
            baudrate=115200,
            timeout=0.1,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        connected = connection.connect_with_config(config)
        self.assertTrue(connected)
        self.assertTrue(any('[HOST]: Connected' in log[0] for log in listener.logs))

        connection.disconnect()
        self.assertTrue(any('[HOST]: Disconnected' in log[0] for log in listener.logs))

    def test_disconnect_channel_close_exception(self) -> None:
        '''Tests that exceptions during channel close are captured and logged.'''
        mock_driver = MagicMock()
        mock_driver.is_open.return_value = True
        mock_driver.close_channel.side_effect = RuntimeError('USB detached')
        listener = MockRecordingListener()
        connection = StreamTransportConnection(
            driver=mock_driver,
            listener=listener,
            worker_factory=TransportReaderWorkerFactory,
        )
        connection.disconnect()
        self.assertTrue(any('[ERR]: Error closing channel' in log[0] for log in listener.logs))

    def test_factory_version(self) -> None:
        '''Tests factory version accessor.'''
        version = StreamTransportConnectionFactory.get_version()
        self.assertEqual(version, '1.0.3')

    def test_worker_factory_methods(self) -> None:
        '''Tests that default TransportReaderWorkerFactory has create and get_version.'''
        self.assertTrue(callable(TransportReaderWorkerFactory.create))
        self.assertEqual(TransportReaderWorkerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
