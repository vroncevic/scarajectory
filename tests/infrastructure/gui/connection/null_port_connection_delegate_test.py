# -*- coding: UTF-8 -*-

'''
Module
    null_port_connection_delegate_test.py
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
    Unit tests for NullPortConnectionDelegate component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.connection.iport_connection_delegate import IPortConnectionDelegate
from scarajectory.infrastructure.gui.connection.null_port_connection_delegate import NullPortConnectionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestNullPortConnectionDelegate(TestCase):
    '''
        Test cases verifying NullPortConnectionDelegate contract and no-op behavior.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance against IPortConnectionDelegate.
        '''
        delegate = NullPortConnectionDelegate()
        self.assertIsInstance(delegate, IPortConnectionDelegate)

    def test_toggle_connection_noop(self) -> None:
        '''
            Tests that toggle_connection executes safely as a no-op.
        '''
        delegate = NullPortConnectionDelegate()
        try:
            delegate.toggle_connection()
        except Exception as exc:  # noqa: BLE001
            self.fail(f'toggle_connection raised unexpected exception: {exc}')


if __name__ == '__main__':
    main()
