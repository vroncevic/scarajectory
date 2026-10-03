# -*- coding: UTF-8 -*-

'''
Module
    theme_button_styler_test.py
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
    Unit tests for ThemeButtonStyler component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.theme.theme_button_styler import ThemeButtonStyler
from scarajectory.infrastructure.gui.theme.theme_button_styler_factory import ThemeButtonStylerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestThemeButtonStyler(TestCase):
    '''
        Test cases for ThemeButtonStyler.
    '''

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies factory creates ThemeButtonStyler.
        '''
        styler = ThemeButtonStylerFactory.create()
        self.assertIsInstance(styler, ThemeButtonStyler)

    def test_configure_invokes_style_methods(self) -> None:
        '''
            Verifies configure applies styles to mock Style.
        '''
        mock_style = MagicMock()
        palette = {'fg_text': '#abb2bf', 'accent_blue': '#61afef'}
        styler = ThemeButtonStyler()
        styler.configure(mock_style, palette)
        self.assertTrue(mock_style.configure.called)
        self.assertTrue(mock_style.map.called)
