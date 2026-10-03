# -*- coding: UTF-8 -*-

'''
Module
    dsl_tag_applier_test.py
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
    Unit tests for DslTagApplier.
'''

from __future__ import annotations

from tkinter import Tk, Text
from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.syntax.tag_applier import DslTagApplier
from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslTagApplierTestCase(TestCase):
    '''
        Test cases verifying DslTagApplier tag formatting behavior.
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
        self.text = Text(self.root)
        self.applier = DslTagApplier()

    def tearDown(self) -> None:
        self.text.destroy()

    def test_configure_styles(self) -> None:
        '''
            Tests tag configuration on text widget.
        '''
        self.applier.configure_styles(self.text)
        configured_tags = self.text.tag_names()
        self.assertIn('dsl_comment', configured_tags)
        self.assertIn('dsl_command', configured_tags)
        self.assertIn('dsl_keyword', configured_tags)
        self.assertIn('dsl_param', configured_tags)
        self.assertIn('dsl_number', configured_tags)

    def test_apply_tokens(self) -> None:
        '''
            Tests clearing old tags and applying token spans.
        '''
        self.applier.configure_styles(self.text)
        self.text.insert('1.0', 'MOVE_J X=100\n')
        tokens = (
            SyntaxToken(tag='dsl_command', start_idx='1.0', end_idx='1.6'),
            SyntaxToken(tag='dsl_param', start_idx='1.7', end_idx='1.8'),
            SyntaxToken(tag='dsl_number', start_idx='1.9', end_idx='1.12'),
        )
        self.applier.apply_tokens(
            self.text,
            tokens,
            ('dsl_command', 'dsl_param', 'dsl_number'),
        )
        cmd_ranges = self.text.tag_ranges('dsl_command')
        self.assertGreater(len(cmd_ranges), 0)


if __name__ == '__main__':
    main()
