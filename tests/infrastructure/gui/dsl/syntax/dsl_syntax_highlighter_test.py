# -*- coding: UTF-8 -*-

'''
Module
    dsl_syntax_highlighter_test.py
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
    Unit tests for DslSyntaxHighlighter.
'''

from __future__ import annotations

from tkinter import Tk, Text
from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.syntax.highlighter import DslSyntaxHighlighter
from scarajectory.infrastructure.gui.dsl.syntax.highlighter_factory import DslSyntaxHighlighterFactory
from scarajectory.infrastructure.gui.dsl.syntax.ihighlighter import IDslSyntaxHighlighter

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
        Test cases verifying DslSyntaxHighlighter coordination behavior.
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
        self.highlighter = DslSyntaxHighlighterFactory.create_default()
        self.highlighter.configure_styles(self.text)

    def tearDown(self) -> None:
        self.text.destroy()

    def test_version(self) -> None:
        '''
            Tests component version string.
        '''
        self.assertEqual(DslSyntaxHighlighter.get_version(), '1.0.3')
        self.assertEqual(DslSyntaxHighlighterFactory.get_version(), '1.0.3')

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance of DslSyntaxHighlighter.
        '''
        self.assertIsInstance(self.highlighter, IDslSyntaxHighlighter)

    def test_highlight_code(self) -> None:
        '''
            Tests syntax highlighting across commands, params, and comments.
        '''
        self.text.insert(
            '1.0',
            '# Trajectory header\nMOVE_J X=100.5 Y=200 SPEED=50 RAPID\n'
        )
        self.highlighter.highlight(self.text)
        cmd_ranges = self.text.tag_ranges('dsl_command')
        param_ranges = self.text.tag_ranges('dsl_param')
        num_ranges = self.text.tag_ranges('dsl_number')
        comment_ranges = self.text.tag_ranges('dsl_comment')
        keyword_ranges = self.text.tag_ranges('dsl_keyword')

        self.assertGreater(len(cmd_ranges), 0)
        self.assertGreater(len(param_ranges), 0)
        self.assertGreater(len(num_ranges), 0)
        self.assertGreater(len(comment_ranges), 0)
        self.assertGreater(len(keyword_ranges), 0)


if __name__ == '__main__':
    main()
