# -*- coding: UTF-8 -*-

'''
Module
    theme_manager_test.py
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
    Unit tests for ThemeManager design token and palette registry.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestThemeManager(unittest.TestCase):
    '''
        Test cases for ThemeManager design tokens and palette queries.

        It defines:

            :methods:
                | test_palette_contents - Tests presence of standard theme design token keys.
                | test_get_color_lookup - Tests single key query and fallback.
                | test_palette_immutability - Tests that get_palette returns independent copies.
    '''

    def test_palette_contents(self) -> None:
        '''
            Tests palette dictionary keys.

            :exceptions: None.
        '''
        palette = ThemeManager.get_palette()
        self.assertIn('bg_dark', palette)
        self.assertIn('bg_card', palette)
        self.assertIn('bg_canvas', palette)
        self.assertIn('fg_text', palette)
        self.assertIn('accent_blue', palette)

    def test_get_color_lookup(self) -> None:
        '''
            Tests get_color token resolution.

            :exceptions: None.
        '''
        color = ThemeManager.get_color('accent_blue')
        self.assertEqual(color, '#61afef')

        fallback = ThemeManager.get_color('non_existent_color')
        self.assertEqual(fallback, '#ffffff')

    def test_palette_immutability(self) -> None:
        '''
            Tests modification safety of get_palette copy.

            :exceptions: None.
        '''
        palette1 = ThemeManager.get_palette()
        palette1['bg_dark'] = '#000000'

        palette2 = ThemeManager.get_palette()
        self.assertNotEqual(palette2['bg_dark'], '#000000')


if __name__ == '__main__':
    unittest.main()
