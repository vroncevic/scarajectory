# -*- coding: UTF-8 -*-

'''
Module
    stream_control_transmitter_test.py
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
    Unit tests for StreamControlTransmitter and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.formatter.command_formatter import CommandFormatter
from scarajectory.infrastructure.streaming.stream_control_transmitter import StreamControlTransmitter
from scarajectory.infrastructure.streaming.stream_control_transmitter_factory import StreamControlTransmitterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamControlTransmitterTestCase(TestCase):
    '''
        Tests StreamControlTransmitter across ASCII and Binary wire protocols.

        It defines:

            :methods:
                | setUp - Initializes mock connection manager and transmitter.
                | test_binary_commands - Verifies transmission of binary control frames.
                | test_ascii_commands - Verifies transmission of ascii command strings.
                | test_factory - Verifies factory creation and version.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.

            :exceptions: None.
        '''
        self.mock_conn = MagicMock()
        self.frame_builder = BinaryFrameBuilderFactory.create()
        self.transmitter: StreamControlTransmitter = (
            StreamControlTransmitterFactory.create(
                raw_transceiver=self.mock_conn,
                frame_builder=self.frame_builder,
            )
        )

    def test_binary_commands(self) -> None:
        '''
            Tests sending binary commands.

            :exceptions: None.
        '''
        self.transmitter.send_enable(ProtocolMode.BINARY)
        self.assertTrue(self.mock_conn.send_raw_bytes.called)
        self.mock_conn.send_raw_bytes.reset_mock()

        self.transmitter.send_hold(ProtocolMode.BINARY)
        self.assertTrue(self.mock_conn.send_raw_bytes.called)
        self.mock_conn.send_raw_bytes.reset_mock()

        self.transmitter.send_resume(ProtocolMode.BINARY)
        self.assertTrue(self.mock_conn.send_raw_bytes.called)
        self.mock_conn.send_raw_bytes.reset_mock()

        self.transmitter.send_estop(ProtocolMode.BINARY)
        self.assertTrue(self.mock_conn.send_raw_bytes.called)

    def test_ascii_commands(self) -> None:
        '''
            Tests sending ASCII commands.

            :exceptions: None.
        '''
        self.transmitter.send_enable(ProtocolMode.ASCII)
        self.mock_conn.send_raw_command.assert_called_with(CommandFormatter.format_enable())
        self.mock_conn.send_raw_command.reset_mock()

        self.transmitter.send_hold(ProtocolMode.ASCII)
        self.mock_conn.send_raw_command.assert_called_with(CommandFormatter.format_pause())
        self.mock_conn.send_raw_command.reset_mock()

        self.transmitter.send_resume(ProtocolMode.ASCII)
        self.mock_conn.send_raw_command.assert_called_with(CommandFormatter.format_resume())
        self.mock_conn.send_raw_command.reset_mock()

        self.transmitter.send_estop(ProtocolMode.ASCII)
        self.mock_conn.send_raw_command.assert_called_with(CommandFormatter.format_estop())

    def test_factory(self) -> None:
        '''
            Tests factory version.

            :exceptions: None.
        '''
        self.assertEqual(StreamControlTransmitterFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
