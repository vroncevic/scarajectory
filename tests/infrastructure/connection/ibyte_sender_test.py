# -*- coding: UTF-8 -*-

'''
Module
    ibyte_sender_test.py
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
    Unit testing for IByteSender protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.connection.ibyte_sender import IByteSender

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ByteSenderStub:
    '''Structural test stub satisfying IByteSender protocol.'''

    def send_raw_bytes(self, payload: bytes) -> bool:
        '''Sends raw byte payload.'''
        return len(payload) > 0

    def is_connected(self) -> bool:
        '''Returns transport connection status.'''
        return True


class IncompleteByteSenderStub:
    '''Incomplete test stub missing required send_raw_bytes method.'''

    def flush(self) -> None:
        '''Flushes transmission buffer.'''

    def is_connected(self) -> bool:
        '''Returns transport connection status.'''
        return True


class ByteSenderTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IByteSender.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IByteSender protocol.'''
        stub = ByteSenderStub()
        self.assertIsInstance(stub, IByteSender)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IByteSender protocol check.'''
        incomplete = IncompleteByteSenderStub()
        self.assertNotIsInstance(incomplete, IByteSender)


if __name__ == '__main__':
    main()
