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
    Unit tests for StreamRawTransceiver communication adapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.connection.stream_raw_transceiver import StreamRawTransceiver
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.istream_transport_transceiver import IStreamTransportTransceiver

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
        Tests StreamRawTransceiver command and byte transmission.

        It defines:

            :methods:
                | test_is_connected - Verifies connection state reflection.
                | test_send_raw_command - Verifies command sending when connected and disconnected.
                | test_send_raw_bytes - Verifies byte sending when connected and disconnected.
    '''

    def test_is_connected(self) -> None:
        '''Verifies is_connected delegates to underlying connection.'''
        mock_conn = MagicMock(spec=IStreamTransportConnection)
        mock_trans = MagicMock(spec=IStreamTransportTransceiver)
        transceiver = StreamRawTransceiver(
            connection=mock_conn,
            transceiver=mock_trans,
        )

        mock_conn.is_connected.return_value = True
        self.assertTrue(transceiver.is_connected())

        mock_conn.is_connected.return_value = False
        self.assertFalse(transceiver.is_connected())

    def test_send_raw_command(self) -> None:
        '''Verifies send_raw_command behavior under connected and disconnected states.'''
        mock_conn = MagicMock(spec=IStreamTransportConnection)
        mock_trans = MagicMock(spec=IStreamTransportTransceiver)
        mock_trans.send_raw.return_value = True
        transceiver = StreamRawTransceiver(
            connection=mock_conn,
            transceiver=mock_trans,
        )

        mock_conn.is_connected.return_value = True
        self.assertTrue(transceiver.send_raw_command('M114\n'))
        mock_trans.send_raw.assert_called_once_with('M114\n')

        mock_conn.is_connected.return_value = False
        self.assertFalse(transceiver.send_raw_command('M114\n'))

    def test_send_raw_bytes(self) -> None:
        '''Verifies send_raw_bytes behavior under connected and disconnected states.'''
        mock_conn = MagicMock(spec=IStreamTransportConnection)
        mock_trans = MagicMock(spec=IStreamTransportTransceiver)
        mock_trans.send_bytes.return_value = True
        transceiver = StreamRawTransceiver(
            connection=mock_conn,
            transceiver=mock_trans,
        )

        mock_conn.is_connected.return_value = True
        self.assertTrue(transceiver.send_raw_bytes(b'\x01\x02\x03'))
        mock_trans.send_bytes.assert_called_once_with(b'\x01\x02\x03')

        mock_conn.is_connected.return_value = False
        self.assertFalse(transceiver.send_raw_bytes(b'\x01\x02\x03'))


if __name__ == '__main__':
    main()
