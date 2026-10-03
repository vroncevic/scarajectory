# -*- coding: UTF-8 -*-

'''
Module
    ichannel_test.py
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
    Unit testing for IChannelDriver protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.driver.ichannel import IChannelDriver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ChannelDriverStub:
    '''Structural test stub satisfying IChannelDriver protocol.'''

    def open_channel(self, config: StreamConfig) -> None:
        '''Opens channel.'''
        _ = config

    def close_channel(self) -> None:
        '''Closes channel.'''

    def read_bytes(self, size: int) -> bytes:
        '''Reads bytes.'''
        _ = size
        return b''

    def write_bytes(self, payload: bytes) -> None:
        '''Writes bytes.'''
        _ = payload

    def is_open(self) -> bool:
        '''Checks link status.'''
        return True

    def channel_name(self) -> str:
        '''Returns channel descriptor.'''
        return 'STUB'


class IncompleteChannelDriverStub:
    '''Incomplete test stub missing write_bytes and is_open.'''

    def open_channel(self, config: StreamConfig) -> None:
        '''Opens channel.'''
        _ = config

    def close_channel(self) -> None:
        '''Closes channel.'''


class ChannelDriverTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IChannelDriver.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IChannelDriver protocol.'''
        stub = ChannelDriverStub()
        self.assertIsInstance(stub, IChannelDriver)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IChannelDriver protocol check.'''
        incomplete = IncompleteChannelDriverStub()
        self.assertNotIsInstance(incomplete, IChannelDriver)


if __name__ == '__main__':
    main()
