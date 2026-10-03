# -*- coding: UTF-8 -*-

'''
Module
    istream_line_receiver_test.py
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
    Unit testing for IStreamLineReceiver protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.worker.istream_line_receiver import IStreamLineReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamLineReceiverStub:
    '''Structural test stub satisfying IStreamLineReceiver protocol.'''

    def handle_incoming_line(self, line: str) -> None:
        '''Processes incoming text response line.'''

    def is_running(self) -> bool:
        '''Checks receiver active status.'''
        return True


class IncompleteStreamLineReceiverStub:
    '''Incomplete test stub missing required handle_incoming_line method.'''

    def process_text(self, text: str) -> None:
        '''Generic text handler.'''

    def is_running(self) -> bool:
        '''Checks receiver active status.'''
        return True


class StreamLineReceiverTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamLineReceiver.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamLineReceiver protocol.'''
        stub = StreamLineReceiverStub()
        self.assertIsInstance(stub, IStreamLineReceiver)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IStreamLineReceiver protocol check.'''
        incomplete = IncompleteStreamLineReceiverStub()
        self.assertNotIsInstance(incomplete, IStreamLineReceiver)


if __name__ == '__main__':
    main()
