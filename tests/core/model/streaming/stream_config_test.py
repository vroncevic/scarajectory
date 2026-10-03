# -*- coding: UTF-8 -*-

'''
Module
    stream_config_test.py
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
    Unit tests for StreamConfig serial and network communication DTO.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamConfigTestCase(TestCase):
    '''
        Tests for StreamConfig immutable parameters container.

        It defines:

            :methods:
                | test_config_creation - Verifies attribute assignment upon creation.
                | test_config_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across identical instances.
    '''

    def test_config_creation(self) -> None:
        '''
            Verifies attribute assignment upon creation.

            :exceptions: None.
        '''
        config = StreamConfig(
            port='/dev/ttyUSB0',
            baudrate=115200,
            timeout=2.0,
            queue_capacity=16,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertEqual(config.port, '/dev/ttyUSB0')
        self.assertEqual(config.baudrate, 115200)
        self.assertEqual(config.timeout, 2.0)
        self.assertEqual(config.queue_capacity, 16)
        self.assertEqual(config.protocol_mode, ProtocolMode.ASCII)

    def test_config_immutability(self) -> None:
        '''
            Verifies frozen instance constraints.

            :exceptions: None.
        '''
        config = StreamConfig(
            port='COM3',
            baudrate=9600,
            timeout=1.0,
            queue_capacity=8,
            protocol_mode=ProtocolMode.BINARY,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(config, 'baudrate', 57600)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical instances.

            :exceptions: None.
        '''
        c1 = StreamConfig(
            port='127.0.0.1:8888',
            baudrate=0,
            timeout=0.5,
            queue_capacity=32,
            protocol_mode=ProtocolMode.BINARY,
        )
        c2 = StreamConfig(
            port='127.0.0.1:8888',
            baudrate=0,
            timeout=0.5,
            queue_capacity=32,
            protocol_mode=ProtocolMode.BINARY,
        )
        self.assertEqual(c1, c2)


if __name__ == '__main__':
    main()
