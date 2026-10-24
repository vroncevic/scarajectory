# -*- coding: UTF-8 -*-

'''
Module
    iapplier_test.py
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
    Unit tests for IDslTagApplier protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Text
from unittest import TestCase, main

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


class MockTagApplier:
    '''Mock implementation satisfying IDslTagApplier structurally.'''

    def configure_styles(self, text_widget: Text) -> None:
        '''Configure styles.'''
        del text_widget

    def apply_tokens(
        self,
        text_widget: Text,
        tokens: Sequence[SyntaxToken],
        tags_to_clear: Sequence[str],
    ) -> None:
        '''Apply tokens.'''
        del text_widget, tokens, tags_to_clear

    def get_version(self) -> str:
        '''Return version.'''
        return '1.0.3'


class IncompleteTagApplier:
    '''Mock class failing to implement IDslTagApplier.'''

    def configure_styles(self, text_widget: Text) -> None:
        '''Configure styles.'''
        del text_widget

    def get_name(self) -> str:
        '''Return mock name.'''
        return 'incomplete'


class IDslTagApplierTestCase(TestCase):
    '''
        Unit test suite validating IDslTagApplier protocol compliance.

        It defines:

            :methods:
                | test_structural_compliance - Tests protocol matching.
                | test_incomplete_compliance - Tests protocol rejection.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Tests that structurally compliant class matches protocol.

            :exceptions: None.
        '''
        mock = MockTagApplier()
        self.assertIsInstance(mock, IDslTagApplier)

    def test_incomplete_compliance(self) -> None:
        '''
            Tests that incomplete class fails protocol check.

            :exceptions: None.
        '''
        mock = IncompleteTagApplier()
        self.assertNotIsInstance(mock, IDslTagApplier)


if __name__ == '__main__':
    main()
