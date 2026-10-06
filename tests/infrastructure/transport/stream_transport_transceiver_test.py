# -*- coding: UTF-8 -*-

'''
Module
    stream_transport_transceiver_test.py
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
    Unit tests for StreamTransportTransceiver and StreamTransportTransceiverFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.transport.istream_transport_transceiver import IStreamTransportTransceiver
from scarajectory.infrastructure.transport.stream_transport_transceiver import StreamTransportTransceiver
from scarajectory.infrastructure.transport.stream_transport_transceiver_factory import StreamTransportTransceiverFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubDriver:
    '''
        Structural test double for IChannelDriver.
    '''

    def __init__(self, raise_on_write: bool = False) -> None:
        self.written: list[bytes] = []
        self.raise_on_write: bool = raise_on_write

    def write_bytes(self, data: bytes) -> None:
        '''Records or fails on written bytes.'''
        if self.raise_on_write:
            raise OSError('Write failure')
        self.written.append(data)

    def read_bytes(self, size: int) -> bytes:
        '''Returns mock bytes buffer.'''
        return b'\x01\x02\x03\x04\x05'[:size]

    def channel_name(self) -> str:
        '''Returns channel descriptor name.'''
        return 'StubChannel'


class StubConnection:
    '''
        Structural test double for IStreamTransportConnection.
    '''

    def __init__(self, connected: bool = True) -> None:
        self.connected: bool = connected

    def is_connected(self) -> bool:
        '''Returns connection status.'''
        return self.connected

    def disconnect(self) -> None:
        '''Simulates disconnect.'''
        self.connected = False


class StubRecordingListener:
    '''
        Structural test double recording emitted log entries.
    '''

    def __init__(self) -> None:
        self.logs: list[tuple[str, bool]] = []

    def on_line_received(self, line: str) -> None:
        '''Records line received.'''

    def on_bytes_received(self, data: bytes) -> None:
        '''Records bytes received.'''

    def on_log_emitted(self, message: str, is_sent: bool) -> None:
        '''Records log emission message and sent flag.'''
        self.logs.append((message, is_sent))


class StreamTransportTransceiverTestCase(TestCase):
    '''
        Test suite verifying StreamTransportTransceiver operations and error handling.

        It defines:

            :methods:
                | test_channel_name_and_factory - Tests channel name retrieval and factory creation.
                | test_send_raw_connected_and_disconnected - Tests send_raw in both connection states.
                | test_send_raw_write_exception - Tests send_raw error handling on write failure.
                | test_send_bytes_connected_and_disconnected - Tests send_bytes in both states.
                | test_send_bytes_write_exception - Tests send_bytes error handling on write failure.
                | test_read_bytes - Tests read_bytes behavior when connected and disconnected.
    '''

    def test_channel_name_and_factory(self) -> None:
        '''
            Tests channel name retrieval and factory creation.

            :exceptions: None.
        '''
        driver = StubDriver()
        listener = StubRecordingListener()
        connection = StubConnection()
        transceiver = StreamTransportTransceiverFactory.create(
            driver=driver,  # type: ignore[arg-type]
            listener=listener,  # type: ignore[arg-type]
            connection=connection,  # type: ignore[arg-type]
        )
        self.assertEqual(transceiver.channel_name(), 'StubChannel')
        self.assertIsInstance(transceiver, IStreamTransportTransceiver)
        self.assertEqual(StreamTransportTransceiverFactory.get_version(), '1.0.3')

    def test_send_raw_connected_and_disconnected(self) -> None:
        '''
            Tests send_raw in both connected and disconnected states.

            :exceptions: None.
        '''
        driver = StubDriver()
        listener = StubRecordingListener()
        connection = StubConnection(connected=True)
        transceiver = StreamTransportTransceiver(
            driver=driver,  # type: ignore[arg-type]
            listener=listener,  # type: ignore[arg-type]
            connection=connection,  # type: ignore[arg-type]
        )

        # Connected: without newline
        self.assertTrue(transceiver.send_raw('G0 X10 Y20'))
        self.assertEqual(driver.written[-1], b'G0 X10 Y20\n')
        self.assertIn(('G0 X10 Y20', True), listener.logs)

        # Connected: with newline
        self.assertTrue(transceiver.send_raw('G1 X30\n'))
        self.assertEqual(driver.written[-1], b'G1 X30\n')

        # Disconnected
        connection.disconnect()
        self.assertFalse(transceiver.send_raw('G0 X0'))
        self.assertTrue(any('Not connected' in log[0] for log in listener.logs))

    def test_send_raw_write_exception(self) -> None:
        '''
            Tests send_raw error handling on write failure.

            :exceptions: None.
        '''
        driver = StubDriver(raise_on_write=True)
        listener = StubRecordingListener()
        connection = StubConnection(connected=True)
        transceiver = StreamTransportTransceiver(
            driver=driver,  # type: ignore[arg-type]
            listener=listener,  # type: ignore[arg-type]
            connection=connection,  # type: ignore[arg-type]
        )
        self.assertFalse(transceiver.send_raw('M3 S1000'))
        self.assertTrue(any('Send error' in log[0] for log in listener.logs))

    def test_send_bytes_connected_and_disconnected(self) -> None:
        '''
            Tests send_bytes in both connected and disconnected states.

            :exceptions: None.
        '''
        driver = StubDriver()
        listener = StubRecordingListener()
        connection = StubConnection(connected=True)
        transceiver = StreamTransportTransceiver(
            driver=driver,  # type: ignore[arg-type]
            listener=listener,  # type: ignore[arg-type]
            connection=connection,  # type: ignore[arg-type]
        )

        # Connected
        self.assertTrue(transceiver.send_bytes(b'\xAA\xBB\xCC'))
        self.assertEqual(driver.written[-1], b'\xAA\xBB\xCC')

        # Disconnected
        connection.disconnect()
        self.assertFalse(transceiver.send_bytes(b'\xFF'))
        self.assertTrue(any('Not connected' in log[0] for log in listener.logs))

    def test_send_bytes_write_exception(self) -> None:
        '''
            Tests send_bytes error handling on write failure.

            :exceptions: None.
        '''
        driver = StubDriver(raise_on_write=True)
        listener = StubRecordingListener()
        connection = StubConnection(connected=True)
        transceiver = StreamTransportTransceiver(
            driver=driver,  # type: ignore[arg-type]
            listener=listener,  # type: ignore[arg-type]
            connection=connection,  # type: ignore[arg-type]
        )
        self.assertFalse(transceiver.send_bytes(b'\x01\x02'))
        self.assertTrue(
            any('Binary send error' in log[0] for log in listener.logs)
        )

    def test_read_bytes(self) -> None:
        '''
            Tests read_bytes behavior when connected and disconnected.

            :exceptions: None.
        '''
        driver = StubDriver()
        listener = StubRecordingListener()
        connection = StubConnection(connected=True)
        transceiver = StreamTransportTransceiver(
            driver=driver,  # type: ignore[arg-type]
            listener=listener,  # type: ignore[arg-type]
            connection=connection,  # type: ignore[arg-type]
        )

        self.assertEqual(transceiver.read_bytes(3), b'\x01\x02\x03')

        connection.disconnect()
        self.assertEqual(transceiver.read_bytes(3), b'')


if __name__ == '__main__':
    main()
