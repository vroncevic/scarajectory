# -*- coding: UTF-8 -*-

'''
Module
    tokenizer_test.py
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
    Unit tests for DslSyntaxTokenizer component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken
from scarajectory.infrastructure.gui.dsl.syntax.tokenizer.itokenizer import IDslSyntaxTokenizer
from scarajectory.infrastructure.gui.dsl.syntax.tokenizer.tokenizer import DslSyntaxTokenizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxTokenizerTestCase(TestCase):
    '''
        Test cases verifying DslSyntaxTokenizer scanning behavior.

        It defines:

            :methods:
                | setUp - Initializes tokenizer test instance.
                | test_protocol_compliance - Tests structural protocol check.
                | test_supported_tags - Tests supported syntax tag sequence.
                | test_tokenize_empty - Tests tokenizing empty string.
                | test_tokenize_comment - Tests tokenizing comments.
                | test_tokenize_command_and_params - Tests commands and parameters.
                | test_tokenize_keywords - Tests tokenizing keywords.
                | test_get_version - Tests component version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes tokenizer test fixture.

            :exceptions: None.
        '''
        self.tokenizer = DslSyntaxTokenizer()

    def test_protocol_compliance(self) -> None:
        '''
            Tests that DslSyntaxTokenizer satisfies IDslSyntaxTokenizer structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.tokenizer, IDslSyntaxTokenizer)

    def test_supported_tags(self) -> None:
        '''
            Tests supported syntax tag sequence.

            :exceptions: None.
        '''
        tags: tuple[str, ...] = self.tokenizer.get_supported_tags()
        self.assertIn('dsl_comment', tags)
        self.assertIn('dsl_command', tags)
        self.assertIn('dsl_keyword', tags)
        self.assertIn('dsl_param', tags)
        self.assertIn('dsl_number', tags)

    def test_tokenize_empty(self) -> None:
        '''
            Tests tokenizing empty text string and ignored matches.

            :exceptions: None.
        '''
        tokens: tuple[SyntaxToken, ...] = self.tokenizer.tokenize('')
        self.assertEqual(len(tokens), 0)
        mock_match = MagicMock()
        mock_match.lastgroup = None
        mock_regex = MagicMock()
        mock_regex.finditer.return_value = [mock_match]
        with patch.object(self.tokenizer, 'TOKEN_REGEX', mock_regex):
            self.assertEqual(len(self.tokenizer.tokenize('line')), 0)

    def test_tokenize_comment(self) -> None:
        '''
            Tests tokenizing comment line.

            :exceptions: None.
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

            :exceptions: None.
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

            :exceptions: None.
        '''
        code: str = 'CONFIG RIGHT RAPID ON MOTOR CLOSED_LOOP'
        tokens: tuple[SyntaxToken, ...] = self.tokenizer.tokenize(code)
        tags = [t.tag for t in tokens]
        self.assertIn('dsl_keyword', tags)

    def test_get_version(self) -> None:
        '''
            Tests component version string.

            :exceptions: None.
        '''
        self.assertEqual(self.tokenizer.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
