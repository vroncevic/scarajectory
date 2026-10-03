# -*- coding: UTF-8 -*-

'''
Module
    menu_layout_builder_test.py
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
    Unit tests for MenuLayoutBuilder component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.menu.menu_layout_builder import MenuLayoutBuilder
from scarajectory.infrastructure.gui.menu.menu_layout_builder_factory import MenuLayoutBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMenuLayoutBuilder(TestCase):
    '''
        Test cases for MenuLayoutBuilder.
    '''

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies factory creates MenuLayoutBuilder.
        '''
        builder = MenuLayoutBuilderFactory.create()
        self.assertIsInstance(builder, MenuLayoutBuilder)

    def test_build_menu_configures_root(self) -> None:
        '''
            Verifies build_menu configures menu on root window.
        '''
        mock_root = MagicMock()
        mock_menu_bar = MagicMock()
        mock_mutation = MagicMock()
        mock_history = MagicMock()
        mock_navigator = MagicMock()

        builder = MenuLayoutBuilder()
        builder.build_menu(
            mock_root,
            mock_menu_bar,
            mock_mutation,
            mock_history,
            mock_navigator,
        )
        self.assertTrue(mock_root.config.called)
