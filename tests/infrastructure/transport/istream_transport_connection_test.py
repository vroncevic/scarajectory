# -*- coding: UTF-8 -*-

'''
Module
    istream_transport_connection_test.py
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
    Unit testing for IStreamTransportConnection protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.transport.istream_transport_connection import (
    IStreamTransportConnection,
)
from scarajectory.infrastructure.transport.listener.itransport_listener import (
    ITransportListener,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportConnectionStub:
    '''Structural test stub satisfying IStreamTransportConnection protocol.'''

    def is_connected(self) -> bool:
        '''Checks link status.'''
        return True

    def set_listener(self, listener: ITransportListener) -> None:
        '''Updates listener.'''
        _ = listener

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''Connects with config.'''
        _ = config
        return True

    def disconnect(self) -> None:
        '''Disconnects connection.'''


class IncompleteStreamTransportConnectionStub:
    '''Incomplete test stub missing required connection methods.'''

    def is_connected(self) -> bool:
        '''Checks link status.'''
        return True

    def disconnect(self) -> None:
        '''Disconnects connection.'''


class StreamTransportConnectionTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamTransportConnection.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamTransportConnection protocol.'''
        stub = StreamTransportConnectionStub()
        self.assertIsInstance(stub, IStreamTransportConnection)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IStreamTransportConnection protocol check.'''
        incomplete = IncompleteStreamTransportConnectionStub()
        self.assertNotIsInstance(incomplete, IStreamTransportConnection)


if __name__ == '__main__':
    main()
