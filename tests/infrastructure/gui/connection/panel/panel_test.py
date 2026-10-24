# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
    Unit tests for PortConnectionPanel component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaracom.transport.preference.preference import SerialPreference
from scarajectory.infrastructure.gui.connection.panel.ipanel import IPortConnectionPanel
from scarajectory.infrastructure.gui.connection.panel.panel import PortConnectionPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortConnectionPanelTestCase(TestCase):
    '''
        Tests PortConnectionPanel component and actions.

        It defines:

            :methods:
                | setUpClass - Initializes root Tkinter window fixture.
                | tearDownClass - Destroys root window fixture.
                | setUp - Sets up mock dependencies and panel instance.
                | test_satisfies_protocol - Verifies panel satisfies IPortConnectionPanel.
                | test_on_toggle_connect - Verifies delegate calls on connection toggle.
                | test_set_connected_state - Verifies button text updates.
                | test_refresh_ports_and_get_selected_port - Tests port scanning and retrieval.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Initializes root Tkinter window fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Destroys root window fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up mock dependencies and panel instance.

            :exceptions: None.
        '''
        self.mock_repo = MagicMock()
        self.mock_repo.load_preference.return_value = SerialPreference(
            port='/dev/ttyUSB0',
            baud=115200,
        )
        self.mock_delegate = MagicMock()

        self.panel = PortConnectionPanel(
            self.root,
            connection_repository=self.mock_repo,
            connection_delegate=self.mock_delegate,
        )

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies PortConnectionPanel satisfies IPortConnectionPanel protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.panel, IPortConnectionPanel)

    def test_on_toggle_connect(self) -> None:
        '''
            Verifies on_toggle_connect calls delegate with selected port and syncs state.

            :exceptions: None.
        '''
        self.mock_delegate.is_connected.return_value = True
        self.panel.on_toggle_connect()
        self.mock_delegate.toggle_connection.assert_called_once_with(
            '127.0.0.1:8888'
        )
        self.assertEqual(self.panel.connect_button_text, 'Disconnect')

    def test_set_connected_state(self) -> None:
        '''
            Verifies set_connected_state alters button text.

            :exceptions: None.
        '''
        self.panel.set_connected_state(True)
        self.assertEqual(self.panel.connect_button_text, 'Disconnect')

        self.panel.set_connected_state(False)
        self.assertEqual(self.panel.connect_button_text, 'Connect')

    @patch(
        'scarajectory.infrastructure.gui.connection.selector.selector.'
        'PortScannerFactory.create'
    )
    def test_refresh_ports_and_get_selected_port(
        self, mock_create_scanner: MagicMock
    ) -> None:
        '''
            Tests refresh_ports and get_selected_port delegation.

            :param mock_create_scanner: Mocked scanner factory creation method.
            :exceptions: None.
        '''
        mock_scanner: MagicMock = MagicMock()
        mock_scanner.scan_ports.return_value = ['/dev/ttyUSB0', '/dev/ttyUSB1']
        mock_create_scanner.return_value = mock_scanner

        mock_repo = MagicMock()
        mock_repo.load_preference.return_value = SerialPreference(
            port='/dev/ttyUSB1', baud=115200
        )
        panel = PortConnectionPanel(
            self.root,
            connection_repository=mock_repo,
            connection_delegate=self.mock_delegate,
        )
        self.assertEqual(panel.get_selected_port(), '/dev/ttyUSB1')
        panel.refresh_ports()
        self.assertEqual(panel.get_selected_port(), '/dev/ttyUSB1')


if __name__ == '__main__':
    main()
