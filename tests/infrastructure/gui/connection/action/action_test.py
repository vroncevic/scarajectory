# -*- coding: UTF-8 -*-

'''
Module
    action_test.py
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
    Unit tests for PortConnectionAction component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.connection.action.action import PortConnectionAction
from scarajectory.infrastructure.gui.connection.action.iaction import IPortConnectionAction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortConnectionActionTestCase(TestCase):
    '''
        Tests PortConnectionAction component behavior and protocol conformance.

        It defines:

            :methods:
                | setUpClass - Initializes root Tkinter window fixture.
                | tearDownClass - Destroys root window fixture.
                | setUp - Sets up mock collaborators and action component.
                | test_satisfies_protocol - Verifies component satisfies IPortConnectionAction.
                | test_on_toggle_connect - Verifies toggle invokes delegate and updates state.
                | test_set_connected_state - Verifies styling and preference saving on connect.
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
            Sets up mock collaborators and action component.

            :exceptions: None.
        '''
        self.mock_delegate = MagicMock()
        self.mock_selector = MagicMock()
        self.mock_selector.get_selected_port.return_value = '/dev/ttyUSB0'

        self.action = PortConnectionAction(
            self.root,
            connection_delegate=self.mock_delegate,
            selector=self.mock_selector,
        )

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies PortConnectionAction satisfies IPortConnectionAction protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.action, IPortConnectionAction)

    def test_on_toggle_connect(self) -> None:
        '''
            Verifies toggle invokes delegate with selected port and updates state.

            :exceptions: None.
        '''
        self.mock_delegate.is_connected.return_value = True
        self.action.on_toggle_connect()
        self.mock_selector.get_selected_port.assert_called_once()
        self.mock_delegate.toggle_connection.assert_called_once_with(
            '/dev/ttyUSB0'
        )
        self.assertEqual(self.action.connect_button_text, 'Disconnect')

    def test_set_connected_state(self) -> None:
        '''
            Verifies styling and preference saving when changing connected state.

            :exceptions: None.
        '''
        self.action.set_connected_state(True)
        self.assertEqual(self.action.connect_button_text, 'Disconnect')
        self.mock_selector.save_preference.assert_called_once()

        self.mock_selector.reset_mock()
        self.action.set_connected_state(False)
        self.assertEqual(self.action.connect_button_text, 'Connect')
        self.mock_selector.save_preference.assert_not_called()


if __name__ == '__main__':
    main()
