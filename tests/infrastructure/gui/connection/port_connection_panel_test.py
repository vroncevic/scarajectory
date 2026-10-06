# -*- coding: UTF-8 -*-

'''
Module
    port_connection_panel_test.py
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

from scarajectory.core.model.preferences.connection_preference import ConnectionPreference
from scarajectory.infrastructure.gui.connection.port_connection_panel import PortConnectionPanel

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
                | setUpClass - Initializes root Tkinter window.
                | tearDownClass - Destroys root window.
                | setUp - Sets up mock dependencies and panel instance.
                | test_on_toggle_connect_and_set_delegate - Verifies delegate calls.
                | test_set_connected_state - Verifies button text and style updates.
                | test_save_preference_and_get_selected_port - Tests preference saving.
                | test_refresh_ports_selection_fallbacks - Tests port scanning fallbacks.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def setUp(self) -> None:
        self.mock_repo = MagicMock()
        self.mock_repo.load_preference.return_value = ConnectionPreference(
            port='/dev/ttyUSB0',
            baud=115200,
        )
        self.mock_delegate = MagicMock()
        self.panel = PortConnectionPanel(
            self.root,
            connection_repository=self.mock_repo,
            connection_delegate=self.mock_delegate,
        )

    def test_on_toggle_connect_and_set_delegate(self) -> None:
        '''Tests toggle connection delegate call and dynamic delegate injection.'''
        self.panel.on_toggle_connect()
        self.mock_delegate.toggle_connection.assert_called_once()

        new_delegate = MagicMock()
        self.panel.set_connection_delegate(new_delegate)
        self.panel.on_toggle_connect()
        new_delegate.toggle_connection.assert_called_once()

    def test_set_connected_state(self) -> None:
        '''Tests button text and style updates on connection state change.'''
        self.panel.set_connected_state(True)
        self.assertEqual(self.panel.connect_button_text, 'Disconnect')
        self.panel.set_connected_state(False)
        self.assertEqual(self.panel.connect_button_text, 'Connect')

    def test_save_preference_and_get_selected_port(self) -> None:
        '''Tests manual preference persistence and selected port parsing.'''
        self.panel.set_selected_port('/dev/ttyUSB1 - FTDI')
        self.assertEqual(self.panel.get_selected_port(), '/dev/ttyUSB1')
        self.panel.save_preference()
        self.mock_repo.save_preference.assert_called()

        self.mock_repo.save_preference.reset_mock()
        self.panel.set_selected_port('127.0.0.1:8888 (Digital Twin)')
        self.panel.save_preference()
        self.mock_repo.save_preference.assert_not_called()

        self.panel.set_selected_port('')
        self.assertEqual(self.panel.get_selected_port(), '')

    @patch(
        'scarajectory.infrastructure.gui.connection.port_connection_panel.'
        'SerialPortScanner.scan_ports'
    )
    def test_refresh_ports_selection_fallbacks(
        self, mock_scan_ports: MagicMock
    ) -> None:
        '''Tests refresh_ports selection retaining and fallbacks.'''
        mock_scan_ports.return_value = ['/dev/ttyUSB0', '/dev/ttyUSB1']

        self.panel.set_selected_port('/dev/ttyUSB1')
        self.panel.refresh_ports()
        self.assertEqual(self.panel.get_selected_port(), '/dev/ttyUSB1')

        self.panel.set_selected_port('nonexistent_selected')
        self.mock_repo.load_preference.return_value = ConnectionPreference(
            port='/dev/ttyUSB0', baud=115200
        )
        self.panel.refresh_ports()
        self.assertEqual(self.panel.get_selected_port(), '/dev/ttyUSB0')

        self.panel.set_selected_port('nonexistent_selected')
        self.mock_repo.load_preference.return_value = ConnectionPreference(
            port='nonexistent_preference', baud=115200
        )
        self.panel.refresh_ports()
        self.assertEqual(
            self.panel.get_selected_port(), '127.0.0.1:8888'
        )

        self.panel.set_selected_port('nonexistent_selected')
        self.mock_repo.load_preference.return_value = ConnectionPreference(
            port='', baud=115200
        )
        self.panel.refresh_ports()
        self.assertEqual(
            self.panel.get_selected_port(), '127.0.0.1:8888'
        )


if __name__ == '__main__':
    main()
