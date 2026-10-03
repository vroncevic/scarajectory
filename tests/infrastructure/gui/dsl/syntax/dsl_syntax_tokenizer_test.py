# -*- coding: UTF-8 -*-

'''
Module
    dsl_syntax_tokenizer_test.py
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
    Unit tests for DslSyntaxTokenizer and DslSyntaxTokenizerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.syntax.tokenizer import DslSyntaxTokenizer
from scarajectory.infrastructure.gui.dsl.syntax.tokenizer_factory import DslSyntaxTokenizerFactory
from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxTokenizerTestCase(TestCase):
    '''
        Test cases verifying DslSyntaxTokenizer scanning behavior.
    '''

    def setUp(self) -> None:
        self.tokenizer = DslSyntaxTokenizerFactory.create()

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(
            DslSyntaxTokenizerFactory.get_version(), '1.0.4'
        )

    def test_supported_tags(self) -> None:
        '''
            Tests supported syntax tag sequence.
        '''
        tags: tuple[str, ...] = self.tokenizer.get_supported_tags()
        self.assertIn('dsl_comment', tags)
        self.assertIn('dsl_command', tags)
        self.assertIn('dsl_keyword', tags)
        self.assertIn('dsl_param', tags)
        self.assertIn('dsl_number', tags)

    def test_tokenize_empty(self) -> None:
        '''
            Tests tokenizing empty text string.
        '''
        tokens: tuple[SyntaxToken, ...] = self.tokenizer.tokenize('')
        self.assertEqual(len(tokens), 0)

    def test_tokenize_comment(self) -> None:
        '''
            Tests tokenizing comment line.
        '''
        tokens: tuple[SyntaxToken, ...] = self.tokenizer.tokenize(
            '# Trajectory comment'
        )
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].tag, 'dsl_comment')
        self.assertEqual(tokens[0].start_idx, '1.0')
        self.assertEqual(tokens[0].end_idx, '1.20')

    def test_tokenize_command_and_params(self) -> None:
        '''
            Tests tokenizing command with parameters and numbers.
        '''
        code: str = 'MOVE_J X=100.5 Y=200 SPEED=50'
        tokens: tuple[SyntaxToken, ...] = self.tokenizer.tokenize(code)
        tags = [t.tag for t in tokens]
        self.assertIn('dsl_command', tags)
        self.assertIn('dsl_param', tags)
        self.assertIn('dsl_number', tags)

    def test_tokenize_keywords(self) -> None:
        '''
            Tests tokenizing secondary keywords.
        '''
        code: str = 'RAPID WORK FINE BLEND'
        tokens: tuple[SyntaxToken, ...] = self.tokenizer.tokenize(code)
        self.assertEqual(len(tokens), 4)
        for tok in tokens:
            self.assertEqual(tok.tag, 'dsl_keyword')


if __name__ == '__main__':
    main()
