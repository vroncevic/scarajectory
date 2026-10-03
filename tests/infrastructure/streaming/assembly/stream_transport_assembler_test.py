# -*- coding: UTF-8 -*-

'''
Module
    stream_transport_assembler_test.py
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
    Unit tests for StreamTransportAssembler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.connection.stream_raw_transceiver import StreamRawTransceiver
from scarajectory.infrastructure.streaming.assembly.stream_transport_assembler import StreamTransportAssembler
from scarajectory.infrastructure.transport.bundle import TransportBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamTransportAssembler(TestCase):
    '''
        Test cases verifying StreamTransportAssembler behavior.
    '''

    def test_assemble_components(self) -> None:
        '''
            Tests assembly of connection manager and raw transceiver.
        '''
        mock_transport = TransportBundle(
            connection=MagicMock(),
            transceiver=MagicMock(),
        )
        conn_mgr, raw_xceiver = StreamTransportAssembler.assemble(
            mock_transport, protocol_mode=ProtocolMode.ASCII
        )
        self.assertIsInstance(conn_mgr, StreamConnectionManager)
        self.assertIsInstance(raw_xceiver, StreamRawTransceiver)

    def test_get_version(self) -> None:
        '''
            Tests get_version returns string.
        '''
        self.assertIsInstance(StreamTransportAssembler.get_version(), str)


if __name__ == '__main__':
    main()
