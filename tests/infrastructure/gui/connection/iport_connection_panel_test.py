# -*- coding: UTF-8 -*-

'''
Module
    iport_connection_panel_test.py
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

from scarajectory.infrastructure.gui.connection.iport_connection_panel import IPortConnectionPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingPortConnectionPanelStub:
    '''Conforming stub implementation satisfying IPortConnectionPanel.'''

    def set_connected_state(self, connected: bool) -> None:
        '''Updates connected state.'''
        _ = connected

    def get_selected_port(self) -> str:
        '''Returns selected port string.'''
        return '/dev/ttyUSB0'


class NonConformingPortConnectionPanelStub:
    '''Non-conforming stub missing get_selected_port method.'''

    def set_connected_state(self, connected: bool) -> None:
        '''Updates connected state.'''
        _ = connected

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'


class PortConnectionPanelTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IPortConnectionPanel.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies conforming stub satisfies IPortConnectionPanel protocol.'''
        stub = ConformingPortConnectionPanelStub()
        self.assertIsInstance(stub, IPortConnectionPanel)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-conforming stub fails IPortConnectionPanel protocol check.'''
        incomplete = NonConformingPortConnectionPanelStub()
        self.assertNotIsInstance(incomplete, IPortConnectionPanel)


if __name__ == '__main__':
    main()
