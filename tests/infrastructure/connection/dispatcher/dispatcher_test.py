# -*- coding: UTF-8 -*-

'''
Module
    dispatcher_test.py
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
    Unit testing for ChannelDispatcher implementation.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scarajectory.infrastructure.connection.dispatcher.dispatcher import ChannelDispatcher
from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ChannelDispatcherTestCase(TestCase):
    '''
        Test cases for ChannelDispatcher component.
    '''

    def setUp(self) -> None:
        self.mock_channel = MagicMock()
        self.mock_packer = MagicMock()
        self.dispatcher = ChannelDispatcher(
            raw_channel=self.mock_channel,
            frame_packer=self.mock_packer,
        )

    def test_protocol_compliance(self) -> None:
        '''
            Verifies ChannelDispatcher implements IChannelDispatcher.
        '''
        self.assertIsInstance(self.dispatcher, IChannelDispatcher)

    def test_is_connected(self) -> None:
        '''
            Verifies is_connected delegates to raw channel.
        '''
        self.mock_channel.is_connected.return_value = True
        self.assertTrue(self.dispatcher.is_connected())
        self.mock_channel.is_connected.return_value = False
        self.assertFalse(self.dispatcher.is_connected())

    def test_next_seq(self) -> None:
        '''
            Verifies sequential sequence counter.
        '''
        seq0 = self.dispatcher.next_seq()
        seq1 = self.dispatcher.next_seq()
        self.assertEqual(seq1, seq0 + 1)

    def test_seq_mask_constant(self) -> None:
        '''
            Verifies SEQ_NUM_MASK constant value.
        '''
        self.assertEqual(ChannelDispatcher.SEQ_NUM_MASK, 0xFF)

    def test_send_frame(self) -> None:
        '''
            Verifies send_frame delegates to raw_channel.send_raw_bytes with wire bytes.
        '''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
            payload=b'\x00\x01',
            crc16=0,
        )
        self.mock_channel.is_connected.return_value = True
        self.mock_packer.pack_frame.return_value = b'\xaa\x55\x01\x02'
        self.mock_channel.send_raw_bytes.return_value = True

        self.assertTrue(self.dispatcher.send_frame(frame))
        self.mock_packer.pack_frame.assert_called_once_with(frame=frame)
        self.mock_channel.send_raw_bytes.assert_called_once_with(b'\xaa\x55\x01\x02')


if __name__ == '__main__':
    main()
