# -*- coding: UTF-8 -*-

'''
Module
    hotkey_test.py
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
    Unit tests for MenuHotkeyBinder component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.menu.builder.hotkey import MenuHotkeyBinder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMenuHotkeyBinder(TestCase):
    '''
        Test cases for MenuHotkeyBinder.

        It defines:

            :methods:
                | test_bind_hotkeys_registers_shortcuts - Verifies hotkey registration.
                | test_get_version - Verifies component version string.
    '''

    def test_bind_hotkeys_registers_shortcuts(self) -> None:
        '''
            Verifies bind_hotkeys registers shortcuts on root.

            :exceptions: None.
        '''
        mock_root = MagicMock()
        mock_menu_bar = MagicMock()
        mock_bundle = MagicMock()

        binder = MenuHotkeyBinder()
        binder.bind_hotkeys(mock_root, mock_menu_bar, mock_bundle)
        self.assertGreaterEqual(mock_root.bind.call_count, 5)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = MenuHotkeyBinder().get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
