# -*- coding: UTF-8 -*-

'''
Module
    istream_transport_transceiver_test.py
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
    Unit testing for IStreamTransportTransceiver protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.transport.istream_transport_transceiver import (
    IStreamTransportTransceiver,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportTransceiverStub:
    '''Structural test stub satisfying IStreamTransportTransceiver protocol.'''

    def send_raw(self, cmd: str) -> bool:
        '''Transmits string.'''
        return len(cmd) > 0

    def send_bytes(self, payload: bytes) -> bool:
        '''Transmits bytes.'''
        return len(payload) > 0

    def read_bytes(self, size: int) -> bytes:
        '''Reads bytes.'''
        _ = size
        return b''

    def channel_name(self) -> str:
        '''Returns descriptor name.'''
        return 'STUB_CHANNEL'


class IncompleteStreamTransportTransceiverStub:
    '''Incomplete test stub missing transceiver methods.'''

    def send_raw(self, cmd: str) -> bool:
        '''Transmits string.'''
        return len(cmd) > 0

    def channel_name(self) -> str:
        '''Returns descriptor name.'''
        return 'INCOMPLETE_CHANNEL'


class StreamTransportTransceiverTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamTransportTransceiver.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamTransportTransceiver protocol.'''
        stub = StreamTransportTransceiverStub()
        self.assertIsInstance(stub, IStreamTransportTransceiver)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IStreamTransportTransceiver protocol check.'''
        incomplete = IncompleteStreamTransportTransceiverStub()
        self.assertNotIsInstance(incomplete, IStreamTransportTransceiver)


if __name__ == '__main__':
    main()
