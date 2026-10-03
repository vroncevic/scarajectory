# -*- coding: UTF-8 -*-

'''
Module
    iport_connection_delegate_test.py
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
    Unit testing for IPortConnectionDelegate protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.connection.iport_connection_delegate import (
    IPortConnectionDelegate,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingPortConnectionDelegateStub:
    '''Conforming stub implementation satisfying IPortConnectionDelegate.'''

    def toggle_connection(self) -> None:
        '''Toggles communication port connection.'''

    def get_state(self) -> bool:
        '''Secondary helper method satisfying R0903 minimum public methods.'''
        return True


class IncompletePortConnectionDelegateStub:
    '''Non-conforming stub implementation missing toggle_connection.'''

    def connect(self) -> None:
        '''Irrelevant connection method.'''

    def disconnect(self) -> None:
        '''Irrelevant disconnection method.'''


class PortConnectionDelegateProtocolTestCase(TestCase):
    '''
        Tests IPortConnectionDelegate runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IPortConnectionDelegate protocol.'''
        stub = ConformingPortConnectionDelegateStub()
        self.assertIsInstance(stub, IPortConnectionDelegate)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IPortConnectionDelegate protocol check.'''
        stub = IncompletePortConnectionDelegateStub()
        self.assertNotIsInstance(stub, IPortConnectionDelegate)


if __name__ == '__main__':
    main()
