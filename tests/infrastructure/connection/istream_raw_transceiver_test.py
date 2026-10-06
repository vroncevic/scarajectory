# -*- coding: UTF-8 -*-

'''
Module
    istream_raw_transceiver_test.py
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
    Unit tests for IStreamRawTransceiver protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.connection.istream_raw_transceiver import IStreamRawTransceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingStreamRawTransceiverStub:
    '''Conforming stub implementation satisfying IStreamRawTransceiver.'''

    def send_raw_command(self, cmd: str) -> bool:
        '''Transmits raw command string.'''
        _ = cmd
        return True

    def send_raw_bytes(self, payload: bytes) -> bool:
        '''Transmits raw byte payload.'''
        _ = payload
        return True


class IncompleteStreamRawTransceiverStub:
    '''Non-conforming stub implementation missing send_raw_bytes.'''

    def send_raw_command(self, cmd: str) -> bool:
        '''Transmits raw command string.'''
        _ = cmd
        return True

    def is_valid(self) -> bool:
        '''Checks validity state to satisfy class method count.'''
        return False


class IStreamRawTransceiverTestCase(TestCase):
    '''
        Tests IStreamRawTransceiver runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
                | test_protocol_methods - Verifies protocol defines required methods.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamRawTransceiver protocol.'''
        stub = ConformingStreamRawTransceiverStub()
        self.assertIsInstance(stub, IStreamRawTransceiver)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IStreamRawTransceiver protocol check.'''
        stub = IncompleteStreamRawTransceiverStub()
        self.assertNotIsInstance(stub, IStreamRawTransceiver)

    def test_protocol_methods(self) -> None:
        '''Verifies protocol defines expected method attributes.'''
        for method_name in ('send_raw_command', 'send_raw_bytes'):
            self.assertTrue(hasattr(IStreamRawTransceiver, method_name))


if __name__ == '__main__':
    main()
