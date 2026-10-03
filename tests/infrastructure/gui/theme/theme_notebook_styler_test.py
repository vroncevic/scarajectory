# -*- coding: UTF-8 -*-

'''
Module
    theme_notebook_styler_test.py
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
    Unit tests for ThemeNotebookStyler component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.theme.theme_notebook_styler import ThemeNotebookStyler
from scarajectory.infrastructure.gui.theme.theme_notebook_styler_factory import ThemeNotebookStylerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestThemeNotebookStyler(TestCase):
    '''
        Test cases for ThemeNotebookStyler.
    '''

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies factory creates ThemeNotebookStyler.
        '''
        styler = ThemeNotebookStylerFactory.create()
        self.assertIsInstance(styler, ThemeNotebookStyler)

    def test_configure_invokes_style_methods(self) -> None:
        '''
            Verifies configure applies styles to mock Style.
        '''
        mock_style = MagicMock()
        palette = {'bg_dark': '#1e2227', 'accent_blue': '#61afef'}
        styler = ThemeNotebookStyler()
        styler.configure(mock_style, palette)
        self.assertTrue(mock_style.configure.called)
        self.assertTrue(mock_style.map.called)
