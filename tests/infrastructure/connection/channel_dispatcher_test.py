# -*- coding: UTF-8 -*-

'''
Module
    channel_dispatcher_test.py
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
    Unit tests for ChannelDispatcher and ChannelDispatcherFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.channel_dispatcher import ChannelDispatcher
from scarajectory.infrastructure.connection.channel_dispatcher_factory import ChannelDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockRawChannel:
    '''Mock raw channel recording sent payloads.'''

    def __init__(self, connected: bool = True) -> None:
        self.connected = connected
        self.sent_cmds: list[str] = []
        self.sent_bytes: list[bytes] = []

    def is_connected(self) -> bool:
        '''Checks connection status.'''
        return self.connected

    def send_raw_command(self, cmd: str) -> None:
        '''Records sent command.'''
        self.sent_cmds.append(cmd)

    def send_raw_bytes(self, payload: bytes) -> bool:
        '''Records sent bytes.'''
        self.sent_bytes.append(payload)
        return True


class TestChannelDispatcher(TestCase):
    '''Test cases for ChannelDispatcher.'''

    def setUp(self) -> None:
        self._raw = MockRawChannel(connected=True)
        self._builder = BinaryFrameBuilderFactory.create()
        self._dispatcher = ChannelDispatcher(
            raw_channel=self._raw,
            frame_builder=self._builder,
            protocol_mode=ProtocolMode.ASCII,
        )

    def test_connection_status(self) -> None:
        '''Tests connection status queries.'''
        self.assertTrue(self._dispatcher.is_connected())
        disconnected = MockRawChannel(connected=False)
        d2 = ChannelDispatcherFactory.create(
            raw_channel=disconnected,
            frame_builder=self._builder,
            protocol_mode=ProtocolMode.BINARY,
        )
        self.assertFalse(d2.is_connected())

    def test_next_seq_cyclic(self) -> None:
        '''Tests sequence number cycling.'''
        first = self._dispatcher.next_seq()
        second = self._dispatcher.next_seq()
        self.assertEqual(first, 0)
        self.assertEqual(second, 1)

    def test_send_command(self) -> None:
        '''Tests sending ASCII text command.'''
        res = self._dispatcher.send_command('CMD:HOME')
        self.assertTrue(res)
        self.assertIn('CMD:HOME', self._raw.sent_cmds)

    def test_send_frame(self) -> None:
        '''Tests sending binary frame.'''
        frame: BinaryFrame = self._builder.build_system_cmd(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
        )
        res = self._dispatcher.send_frame(frame)
        self.assertTrue(res)
        self.assertEqual(len(self._raw.sent_bytes), 1)

    def test_protocol_mode_property(self) -> None:
        '''Tests getting and setting protocol mode property.'''
        self.assertEqual(self._dispatcher.protocol_mode, ProtocolMode.ASCII)
        self._dispatcher.protocol_mode = ProtocolMode.BINARY
        self.assertEqual(self._dispatcher.protocol_mode, ProtocolMode.BINARY)


if __name__ == '__main__':
    main()
