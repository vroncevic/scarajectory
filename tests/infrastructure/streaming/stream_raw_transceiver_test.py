# -*- coding: UTF-8 -*-

'''
Module
    stream_raw_transceiver_test.py
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
    Unit tests for StreamRawTransceiver and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.connection.ibyte_sender import IByteSender
from scarajectory.infrastructure.connection.icommand_sender import ICommandSender
from scarajectory.infrastructure.connection.istream_raw_transceiver import IStreamRawTransceiver
from scarajectory.infrastructure.connection.stream_raw_transceiver import StreamRawTransceiver
from scarajectory.infrastructure.connection.stream_raw_transceiver_factory import StreamRawTransceiverFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamRawTransceiverTestCase(TestCase):
    '''
    Tests StreamRawTransceiver raw string command and byte dispatch operations.

    It defines:

        :methods:
            | setUp - Initializes mock connection and transceiver instances.
            | test_satisfies_protocol - Verifies structural typing contracts.
            | test_send_raw_command_connected - Verifies string command sending.
            | test_send_raw_command_disconnected - Verifies disconnect rejection.
            | test_send_raw_bytes_connected - Verifies byte packet sending.
            | test_send_raw_bytes_disconnected - Verifies byte disconnect rejection.
            | test_factory - Verifies factory creation and version.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures.
        '''
        self.mock_connection = MagicMock()
        self.mock_transceiver = MagicMock()
        self.transceiver: StreamRawTransceiver = (
            StreamRawTransceiverFactory.create(
                connection=self.mock_connection,
                transceiver=self.mock_transceiver,
            )
        )

    def test_satisfies_protocol(self) -> None:
        '''
        Verifies structural typing contracts for transceiver protocols.
        '''
        self.assertIsInstance(self.transceiver, IStreamRawTransceiver)
        self.assertIsInstance(self.transceiver, ICommandSender)
        self.assertIsInstance(self.transceiver, IByteSender)

    def test_send_raw_command_connected(self) -> None:
        '''
        Verifies string command sending delegates to transceiver when connected.
        '''
        self.mock_connection.is_connected.return_value = True
        self.mock_transceiver.send_raw.return_value = True

        result: bool = self.transceiver.send_raw_command('G0 X10 Y20\n')

        self.assertTrue(result)
        self.mock_transceiver.send_raw.assert_called_once_with('G0 X10 Y20\n')

    def test_send_raw_command_disconnected(self) -> None:
        '''
        Verifies string command sending fails immediately when disconnected.
        '''
        self.mock_connection.is_connected.return_value = False

        result: bool = self.transceiver.send_raw_command('G0 X10 Y20\n')

        self.assertFalse(result)
        self.mock_transceiver.send_raw.assert_not_called()

    def test_send_raw_bytes_connected(self) -> None:
        '''
        Verifies byte packet sending delegates to transceiver when connected.
        '''
        self.mock_connection.is_connected.return_value = True
        self.mock_transceiver.send_bytes.return_value = True

        result: bool = self.transceiver.send_raw_bytes(b'\x01\x02\x03')

        self.assertTrue(result)
        self.mock_transceiver.send_bytes.assert_called_once_with(b'\x01\x02\x03')

    def test_send_raw_bytes_disconnected(self) -> None:
        '''
        Verifies byte packet sending fails immediately when disconnected.
        '''
        self.mock_connection.is_connected.return_value = False

        result: bool = self.transceiver.send_raw_bytes(b'\x01\x02\x03')

        self.assertFalse(result)
        self.mock_transceiver.send_bytes.assert_not_called()

    def test_factory(self) -> None:
        '''
        Verifies factory creation and version querying.
        '''
        instance = StreamRawTransceiverFactory.create(
            connection=self.mock_connection,
            transceiver=self.mock_transceiver,
        )
        self.assertIsInstance(instance, StreamRawTransceiver)
        self.assertEqual(StreamRawTransceiverFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
