# -*- coding: UTF-8 -*-

'''
Module
    bootstrap_test.py
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
    Unit tests for BootstrapBytesReceiver component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.connection.receiver.bootstrap import BootstrapBytesReceiver
from scarajectory.infrastructure.connection.receiver.ibytes_receiver import IStreamBytesReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BootstrapBytesReceiverTestCase(TestCase):
    '''
        Tests BootstrapBytesReceiver methods and protocol conformance.

        It defines:

            :methods:
                | test_satisfies_protocol - Verifies IStreamBytesReceiver structural conformance.
                | test_handle_incoming_bytes - Verifies handling bytes without exception.
                | test_is_running - Verifies is_running returns False.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies structural conformance to IStreamBytesReceiver.

            :exceptions: None.
        '''
        receiver = BootstrapBytesReceiver()
        self.assertIsInstance(receiver, IStreamBytesReceiver)

    def test_handle_incoming_bytes(self) -> None:
        '''
            Verifies bytes handling executes safely.

            :exceptions: None.
        '''
        receiver = BootstrapBytesReceiver()
        receiver.handle_incoming_bytes(b'\x01\x02\x03')

    def test_is_running(self) -> None:
        '''
            Verifies is_running returns False.

            :exceptions: None.
        '''
        receiver = BootstrapBytesReceiver()
        self.assertFalse(receiver.is_running())

    def test_get_version(self) -> None:
        '''
            Verifies version string reported by component.

            :exceptions: None.
        '''
        receiver = BootstrapBytesReceiver()
        self.assertEqual(receiver.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
