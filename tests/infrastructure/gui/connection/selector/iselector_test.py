# -*- coding: UTF-8 -*-

'''
Module
    iselector_test.py
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
    Unit testing for IPortSelector protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.connection.selector.iselector import IPortSelector

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingPortSelectorStub:
    '''
        Conforming stub implementation satisfying IPortSelector.

        It defines:

            :methods:
                | refresh_ports - Scans ports.
                | get_selected_port - Returns selected port.
                | set_selected_port - Sets selected port.
                | save_preference - Saves preference.
    '''

    def refresh_ports(self) -> None:
        '''
            Scans ports.

            :exceptions: None.
        '''

    def get_selected_port(self) -> str:
        '''
            Returns selected port.

            :return: Port name.
            :exceptions: None.
        '''
        return '/dev/ttyUSB0'

    def set_selected_port(self, port: str) -> None:
        '''
            Sets selected port.

            :param port: Port name string.
            :exceptions: None.
        '''
        del port

    def save_preference(self) -> None:
        '''
            Saves preference.

            :exceptions: None.
        '''


class NonConformingPortSelectorStub:
    '''
        Non-conforming stub missing save_preference.

        It defines:

            :methods:
                | refresh_ports - Scans ports.
                | get_selected_port - Returns selected port.
    '''

    def refresh_ports(self) -> None:
        '''
            Scans ports.

            :exceptions: None.
        '''

    def get_selected_port(self) -> str:
        '''
            Returns selected port.

            :return: Port name.
            :exceptions: None.
        '''
        return '/dev/ttyUSB0'


class TestIPortSelector(TestCase):
    '''
        Unit tests validating structural protocol runtime checks for IPortSelector.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming stub satisfies protocol.
                | test_protocol_conformance_failure - Verifies non-conforming stub fails protocol.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies conforming stub satisfies IPortSelector protocol.

            :exceptions: None.
        '''
        stub = ConformingPortSelectorStub()
        self.assertIsInstance(stub, IPortSelector)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-conforming stub fails IPortSelector protocol check.

            :exceptions: None.
        '''
        incomplete = NonConformingPortSelectorStub()
        self.assertNotIsInstance(incomplete, IPortSelector)


if __name__ == '__main__':
    main()
