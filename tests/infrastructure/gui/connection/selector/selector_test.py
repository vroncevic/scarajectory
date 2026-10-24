# -*- coding: UTF-8 -*-

'''
Module
    selector_test.py
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
    Unit tests for PortSelector component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaracom.transport.preference.preference import SerialPreference
from scarajectory.infrastructure.gui.connection.selector.iselector import IPortSelector
from scarajectory.infrastructure.gui.connection.selector.selector import PortSelector

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortSelectorTestCase(TestCase):
    '''
        Tests PortSelector component and actions.

        It defines:

            :methods:
                | setUpClass - Initializes root Tkinter window fixture.
                | tearDownClass - Destroys root window fixture.
                | setUp - Sets up mock dependencies and selector instance.
                | test_satisfies_protocol - Verifies selector satisfies IPortSelector.
                | test_save_preference_and_get_selected_port - Tests preference saving.
                | test_refresh_ports_selection_fallbacks - Tests port scanning fallbacks.
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
            Sets up mock dependencies and selector instance.

            :exceptions: None.
        '''
        self.mock_repo = MagicMock()
        self.mock_repo.load_preference.return_value = SerialPreference(
            port='/dev/ttyUSB0',
            baud=115200,
        )
        self.selector = PortSelector(
            self.root,
            connection_repository=self.mock_repo,
        )

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies PortSelector satisfies IPortSelector protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.selector, IPortSelector)

    def test_save_preference_and_get_selected_port(self) -> None:
        '''
            Verifies save_preference ignores digital twin and saves hardware ports.

            :exceptions: None.
        '''
        self.mock_repo.reset_mock()
        self.selector.set_selected_port('/dev/ttyUSB1 (USB Serial)')
        self.assertEqual(self.selector.get_selected_port(), '/dev/ttyUSB1')
        self.selector.save_preference()
        self.mock_repo.save_preference.assert_called_once()

        self.mock_repo.reset_mock()
        self.selector.set_selected_port('127.0.0.1:8888 (Digital Twin)')
        self.selector.save_preference()
        self.mock_repo.save_preference.assert_not_called()

        self.selector.set_selected_port('')
        self.assertEqual(self.selector.get_selected_port(), '')

    @patch(
        'scarajectory.infrastructure.gui.connection.selector.selector.'
        'PortScannerFactory.create'
    )
    def test_refresh_ports_selection_fallbacks(
        self, mock_create_scanner: MagicMock
    ) -> None:
        '''
            Tests refresh_ports selection retaining and fallbacks.

            :param mock_create_scanner: Mocked scanner factory creation method.
            :exceptions: None.
        '''
        mock_scanner: MagicMock = MagicMock()
        mock_scanner.scan_ports.return_value = ['/dev/ttyUSB0', '/dev/ttyUSB1']
        mock_create_scanner.return_value = mock_scanner

        self.selector.set_selected_port('/dev/ttyUSB1')
        self.selector.refresh_ports()
        self.assertEqual(self.selector.get_selected_port(), '/dev/ttyUSB1')

        self.selector.set_selected_port('nonexistent_selected')
        self.mock_repo.load_preference.return_value = SerialPreference(
            port='/dev/ttyUSB0', baud=115200
        )
        self.selector.refresh_ports()
        self.assertEqual(self.selector.get_selected_port(), '/dev/ttyUSB0')

        self.selector.set_selected_port('nonexistent_selected')
        self.mock_repo.load_preference.return_value = SerialPreference(
            port='nonexistent_pref', baud=115200
        )
        self.selector.refresh_ports()
        self.assertEqual(self.selector.get_selected_port(), '127.0.0.1:8888')

        self.selector.set_selected_port('nonexistent_selected')
        self.mock_repo.load_preference.return_value = SerialPreference(
            port='', baud=115200
        )
        self.selector.refresh_ports()
        self.assertEqual(self.selector.get_selected_port(), '127.0.0.1:8888')


if __name__ == '__main__':
    main()
