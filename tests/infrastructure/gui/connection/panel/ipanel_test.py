# -*- coding: UTF-8 -*-

'''
Module
    ipanel_test.py
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
    Unit testing for IPortConnectionPanel protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.connection.panel.ipanel import IPortConnectionPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingPortConnectionPanelStub:
    '''
        Conforming stub implementation satisfying IPortConnectionPanel.

        It defines:

            :methods:
                | set_connected_state - Updates connected state.
                | get_selected_port - Returns selected port string.
    '''

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates connected state.

            :param connected: True if connected.
            :exceptions: None.
        '''
        del connected

    def get_selected_port(self) -> str:
        '''
            Returns selected port string.

            :return: Port identifier string.
            :exceptions: None.
        '''
        return '/dev/ttyUSB0'


class NonConformingPortConnectionPanelStub:
    '''
        Non-conforming stub missing get_selected_port method.

        It defines:

            :methods:
                | set_connected_state - Updates connected state.
                | get_version - Returns version string.
    '''

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates connected state.

            :param connected: True if connected.
            :exceptions: None.
        '''
        del connected

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'


class TestIPortConnectionPanel(TestCase):
    '''
        Unit tests validating structural protocol runtime checks for IPortConnectionPanel.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming stub satisfies protocol.
                | test_protocol_conformance_failure - Verifies non-conforming stub fails protocol.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies conforming stub satisfies IPortConnectionPanel protocol.

            :exceptions: None.
        '''
        stub = ConformingPortConnectionPanelStub()
        self.assertIsInstance(stub, IPortConnectionPanel)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-conforming stub fails IPortConnectionPanel protocol check.

            :exceptions: None.
        '''
        incomplete = NonConformingPortConnectionPanelStub()
        self.assertNotIsInstance(incomplete, IPortConnectionPanel)


if __name__ == '__main__':
    main()
