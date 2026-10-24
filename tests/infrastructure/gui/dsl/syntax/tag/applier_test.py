# -*- coding: UTF-8 -*-

'''
Module
    applier_test.py
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
    Unit tests for DslTagApplier component.
'''

from __future__ import annotations

from tkinter import Text, Tk
from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.syntax.tag.applier import DslTagApplier
from scarajectory.infrastructure.gui.dsl.syntax.tag.iapplier import IDslTagApplier
from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslTagApplierTestCase(TestCase):
    '''
        Unit test suite validating DslTagApplier formatting.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and Tkinter root.
                | tearDown - Cleans up Tkinter root window.
                | test_protocol_compliance - Tests structural protocol satisfaction.
                | test_configure_styles - Tests configuring tags on Text widget.
                | test_apply_tokens - Tests applying token spans and clearing tags.
                | test_get_version - Tests component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures and Text widget.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()
        self.text_widget = Text(self.root)
        self.applier = DslTagApplier()

    def tearDown(self) -> None:
        '''
            Cleans up Tkinter window.

            :exceptions: None.
        '''
        self.text_widget.destroy()
        self.root.destroy()

    def test_protocol_compliance(self) -> None:
        '''
            Tests that DslTagApplier satisfies IDslTagApplier structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.applier, IDslTagApplier)

    def test_configure_styles(self) -> None:
        '''
            Tests configuring syntax tags on text widget.

            :exceptions: None.
        '''
        self.applier.configure_styles(self.text_widget)
        configured_tags = self.text_widget.tag_names()
        self.assertIn('dsl_comment', configured_tags)
        self.assertIn('dsl_command', configured_tags)
        self.assertIn('dsl_keyword', configured_tags)
        self.assertIn('dsl_param', configured_tags)
        self.assertIn('dsl_number', configured_tags)

    def test_apply_tokens(self) -> None:
        '''
            Tests applying token spans and clearing old tags.

            :exceptions: None.
        '''
        self.text_widget.insert('1.0', 'MOVE_J X=100\n')
        tokens = [
            SyntaxToken(tag='dsl_command', start_idx='1.0', end_idx='1.6'),
            SyntaxToken(tag='dsl_param', start_idx='1.7', end_idx='1.8'),
            SyntaxToken(tag='dsl_number', start_idx='1.9', end_idx='1.12'),
        ]
        self.applier.apply_tokens(
            self.text_widget,
            tokens,
            ('dsl_command', 'dsl_param', 'dsl_number'),
        )
        ranges = self.text_widget.tag_ranges('dsl_command')
        self.assertEqual(len(ranges), 2)

    def test_get_version(self) -> None:
        '''
            Tests component version string.

            :exceptions: None.
        '''
        self.assertEqual(self.applier.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
