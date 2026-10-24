# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for DslSyntaxHighlighterFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.syntax.highlighter.factory import DslSyntaxHighlighterFactory
from scarajectory.infrastructure.gui.dsl.syntax.highlighter.highlighter import DslSyntaxHighlighter
from scarajectory.infrastructure.gui.dsl.syntax.tag.iapplier import IDslTagApplier
from scarajectory.infrastructure.gui.dsl.syntax.tokenizer.itokenizer import IDslSyntaxTokenizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxHighlighterFactoryTestCase(TestCase):
    '''
        Unit test suite validating DslSyntaxHighlighterFactory.

        It defines:

            :methods:
                | test_create - Tests factory construction with explicit dependencies.
                | test_create_default - Tests factory construction with defaults.
                | test_get_version - Tests factory version string.
    '''

    def test_create(self) -> None:
        '''
            Tests factory create with explicit dependencies.

            :exceptions: None.
        '''
        tokenizer = MagicMock(spec=IDslSyntaxTokenizer)
        tag_applier = MagicMock(spec=IDslTagApplier)
        highlighter = DslSyntaxHighlighterFactory.create(
            tokenizer=tokenizer,
            tag_applier=tag_applier,
        )
        self.assertIsInstance(highlighter, DslSyntaxHighlighter)

    def test_create_default(self) -> None:
        '''
            Tests factory create_default with subcomponent factories.

            :exceptions: None.
        '''
        highlighter = DslSyntaxHighlighterFactory.create_default()
        self.assertIsInstance(highlighter, DslSyntaxHighlighter)

    def test_get_version(self) -> None:
        '''
            Tests factory version getter.

            :exceptions: None.
        '''
        self.assertEqual(DslSyntaxHighlighterFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
