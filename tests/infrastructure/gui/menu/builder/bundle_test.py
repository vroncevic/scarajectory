# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit testing for MenuBuildersBundle container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.menu.builder.bundle import MenuBuildersBundle
from scarajectory.infrastructure.gui.menu.builder.ihotkey import IMenuHotkeyBinder
from scarajectory.infrastructure.gui.menu.builder.ilayout import IMenuLayoutBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MenuBuildersBundleTestCase(TestCase):
    '''
        Unit tests for MenuBuildersBundle container.

        It defines:

            :methods:
                | test_menu_builders_bundle_attributes - Verifies stored builders.
    '''

    def test_menu_builders_bundle_attributes(self) -> None:
        '''
            Verifies MenuBuildersBundle stores injected builders correctly.

            :exceptions: None.
        '''
        mock_layout = MagicMock(spec=IMenuLayoutBuilder)
        mock_hotkey = MagicMock(spec=IMenuHotkeyBinder)

        builders = MenuBuildersBundle(
            layout_builder=mock_layout,
            hotkey_binder=mock_hotkey,
        )

        self.assertIs(builders.layout_builder, mock_layout)
        self.assertIs(builders.hotkey_binder, mock_hotkey)


if __name__ == '__main__':
    main()
