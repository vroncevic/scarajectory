# -*- coding: UTF-8 -*-

'''
Module
    highlighter_test.py
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
    Unit tests for DslSyntaxHighlighter component.
'''

from __future__ import annotations

from tkinter import Text, Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.syntax.highlighter.highlighter import DslSyntaxHighlighter
from scarajectory.infrastructure.gui.dsl.syntax.highlighter.ihighlighter import IDslSyntaxHighlighter
from scarajectory.infrastructure.gui.dsl.syntax.tag.iapplier import IDslTagApplier
from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken
from scarajectory.infrastructure.gui.dsl.syntax.tokenizer.itokenizer import IDslSyntaxTokenizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxHighlighterTestCase(TestCase):
    '''
        Unit test suite validating DslSyntaxHighlighter coordinator.

        It defines:

            :methods:
                | setUp - Initializes fixtures and Tkinter root.
                | tearDown - Cleans up Tkinter root window.
                | test_protocol_compliance - Tests structural protocol satisfaction.
                | test_configure_styles - Tests style configuration delegation.
                | test_highlight - Tests highlight coordination between tokenizer and applier.
                | test_get_version - Tests component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()
        self.text_widget = Text(self.root)
        self.tokenizer = MagicMock(spec=IDslSyntaxTokenizer)
        self.tag_applier = MagicMock(spec=IDslTagApplier)
        self.highlighter = DslSyntaxHighlighter(
            tokenizer=self.tokenizer,
            tag_applier=self.tag_applier,
        )

    def tearDown(self) -> None:
        '''
            Cleans up Tkinter window.

            :exceptions: None.
        '''
        self.text_widget.destroy()
        self.root.destroy()

    def test_protocol_compliance(self) -> None:
        '''
            Tests that DslSyntaxHighlighter satisfies IDslSyntaxHighlighter structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.highlighter, IDslSyntaxHighlighter)

    def test_configure_styles(self) -> None:
        '''
            Tests configuring styles delegates to tag applier.

            :exceptions: None.
        '''
        self.highlighter.configure_styles(self.text_widget)
        self.tag_applier.configure_styles.assert_called_once_with(self.text_widget)

    def test_highlight(self) -> None:
        '''
            Tests highlight tokenizes content and applies tags.

            :exceptions: None.
        '''
        self.text_widget.insert('1.0', 'MOVE_J X=10\n')
        tokens = (SyntaxToken(tag='dsl_command', start_idx='1.0', end_idx='1.6'),)
        self.tokenizer.tokenize.return_value = tokens
        self.tokenizer.get_supported_tags.return_value = ('dsl_command',)

        self.highlighter.highlight(self.text_widget)

        self.tokenizer.tokenize.assert_called_once()
        self.tag_applier.apply_tokens.assert_called_once_with(
            self.text_widget, tokens, ('dsl_command',)
        )

    def test_get_version(self) -> None:
        '''
            Tests component version string.

            :exceptions: None.
        '''
        self.assertEqual(self.highlighter.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
