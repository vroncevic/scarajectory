# -*- coding: UTF-8 -*-

'''
Module
    ibytes_receiver_test.py
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
    Unit testing for IStreamBytesReceiver protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase

from scarajectory.infrastructure.connection.receiver.ibytes_receiver import IStreamBytesReceiver


class MockBytesReceiver:
    '''Mock class implementing IStreamBytesReceiver protocol.'''

    def handle_incoming_bytes(self, chunk: bytes) -> None:
        '''Handles raw binary packet byte payload.'''

    def is_running(self) -> bool:
        '''Queries active lifecycle state.'''
        return True


class IStreamBytesReceiverTestCase(TestCase):
    '''
        Test cases for IStreamBytesReceiver protocol verification.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Verifies MockBytesReceiver structurally satisfies IStreamBytesReceiver.
        '''
        receiver = MockBytesReceiver()
        self.assertIsInstance(receiver, IStreamBytesReceiver)
