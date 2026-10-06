# -*- coding: UTF-8 -*-

'''
Module
    code_editor_factory_test.py
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
    Unit tests for DslCodeEditorFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.code_editor_factory import DslCodeEditorFactory
from scarajectory.infrastructure.gui.dsl.syntax.highlighter_factory import DslSyntaxHighlighterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslCodeEditorFactory(TestCase):
    '''
        Test cases for DslCodeEditorFactory.
    '''

    def setUp(self) -> None:
        self.root = Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        self.root.destroy()

    def test_create(self) -> None:
        '''
            Tests create with explicit highlighter.
        '''
        highlighter = DslSyntaxHighlighterFactory.create_default()
        editor = DslCodeEditorFactory.create(self.root, highlighter=highlighter)
        self.assertIsInstance(editor, DslCodeEditor)

    def test_create_default(self) -> None:
        '''
            Tests create_default factory method.
        '''
        editor = DslCodeEditorFactory.create_default(self.root)
        self.assertIsInstance(editor, DslCodeEditor)

    def test_get_version(self) -> None:
        '''
            Tests get_version returns semantic version string.
        '''
        ver = DslCodeEditorFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
