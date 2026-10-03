# -*- coding: UTF-8 -*-

'''
Module
    serial_channel_test.py
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
    Unit testing for SerialChannelDriver and SerialChannelDriverFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from serial import SerialException

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.driver.serial_channel import (
    SerialChannelDriver,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialChannelTestCase(TestCase):
    '''Unit tests for SerialChannelDriver I/O lifecycle operations.'''

    def test_unopened_driver_defaults(self) -> None:
        '''Verifies behavior and defaults when driver is closed.'''
        driver = SerialChannelDriver()
        self.assertFalse(driver.is_open())
        self.assertEqual(driver.channel_name(), 'Serial')
        self.assertEqual(driver.read_bytes(10), b'')
        driver.write_bytes(b'PING')
        driver.close_channel()
        self.assertFalse(driver.is_open())

    @patch('scarajectory.infrastructure.transport.driver.serial_channel.Serial')
    def test_open_channel_and_io(self, mock_serial_cls: MagicMock) -> None:
        '''Verifies open channel, read, write, channel_name, and close workflow.'''
        mock_serial = MagicMock()
        mock_serial.is_open = True
        mock_serial.port = '/dev/ttyUSB0'
        mock_serial.read.return_value = b'PONG'
        mock_serial_cls.return_value = mock_serial

        driver = SerialChannelDriver()
        config = StreamConfig(
            port='/dev/ttyUSB0',
            baudrate=115200,
            timeout=0.1,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        driver.open_channel(config)

        self.assertTrue(driver.is_open())
        self.assertEqual(driver.channel_name(), '/dev/ttyUSB0')
        self.assertEqual(driver.read_bytes(4), b'PONG')

        driver.write_bytes(b'PING')
        mock_serial.write.assert_called_once_with(b'PING')
        mock_serial.flush.assert_called_once()

        driver.close_channel()
        mock_serial.close.assert_called_once()
        self.assertFalse(driver.is_open())

    @patch('scarajectory.infrastructure.transport.driver.serial_channel.Serial')
    def test_close_channel_exception_handling(
        self, mock_serial_cls: MagicMock
    ) -> None:
        '''Verifies close_channel suppresses exceptions during port release.'''
        mock_serial = MagicMock()
        mock_serial.close.side_effect = SerialException('Port disconnected')
        mock_serial_cls.return_value = mock_serial

        driver = SerialChannelDriver()
        config = StreamConfig(
            port='/dev/ttyUSB0',
            baudrate=115200,
            timeout=0.1,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        driver.open_channel(config)
        driver.close_channel()
        self.assertFalse(driver.is_open())


if __name__ == '__main__':
    main()
