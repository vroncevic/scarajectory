# -*- coding: UTF-8 -*-

'''
Module
    editor_test.py
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
    Unit tests for DslCodeEditor component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.editor.editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.infrastructure.gui.dsl.syntax.highlighter.ihighlighter import IDslSyntaxHighlighter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslCodeEditorTestCase(TestCase):
    '''
        Unit test suite validating DslCodeEditor component.

        It defines:

            :methods:
                | setUp - Initializes Tkinter root and editor widget.
                | tearDown - Cleans up Tkinter root window.
                | test_protocol_compliance - Tests structural protocol satisfaction.
                | test_get_and_set_text - Tests reading and setting buffer text.
                | test_clear - Tests clearing buffer content.
                | test_highlight - Tests triggering syntax highlight refresh.
                | test_get_version - Tests component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures and DslCodeEditor instance.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()
        self.highlighter = MagicMock(spec=IDslSyntaxHighlighter)
        self.editor = DslCodeEditor(self.root, highlighter=self.highlighter)

    def tearDown(self) -> None:
        '''
            Cleans up Tkinter window.

            :exceptions: None.
        '''
        self.editor.destroy()
        self.root.destroy()

    def test_protocol_compliance(self) -> None:
        '''
            Tests that DslCodeEditor satisfies IDslCodeEditor structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.editor, IDslCodeEditor)

    def test_get_and_set_text(self) -> None:
        '''
            Tests setting and retrieving editor text buffer.

            :exceptions: None.
        '''
        self.editor.set_text('MOVE_J X=10\n')
        self.assertEqual(self.editor.get_text(), 'MOVE_J X=10\n\n')
        self.highlighter.highlight.assert_called()

    def test_clear(self) -> None:
        '''
            Tests clearing text in editor.

            :exceptions: None.
        '''
        self.editor.set_text('CONTENT')
        self.editor.clear()
        self.assertEqual(self.editor.get_text(), '\n')

    def test_highlight(self) -> None:
        '''
            Tests manual highlight invocation.

            :exceptions: None.
        '''
        self.editor.highlight()
        self.highlighter.highlight.assert_called()

    def test_get_version(self) -> None:
        '''
            Tests component version string.

            :exceptions: None.
        '''
        self.assertEqual(self.editor.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
