# -*- coding: UTF-8 -*-

'''
Module
    tab_test.py
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
    Unit tests for DslEditorTab presentation component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.itab import IDslEditorTab
from scarajectory.infrastructure.gui.dsl.tab import DslEditorTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorTab(TestCase):
    '''
        Test cases verifying DslEditorTab layout mounting and initial content loading.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def test_structural_conformance(self) -> None:
        '''
            Tests that DslEditorTab satisfies IDslEditorTab.

            :exceptions: None.
        '''
        tab = DslEditorTab(self.root)
        self.assertTrue(isinstance(tab, IDslEditorTab))
        self.assertEqual(tab.get_version(), '1.0.3')
        tab.destroy()

    def test_initialization_with_empty_store_loads_example(self) -> None:
        '''
            Tests that DslEditorTab loads example script when store is empty.

            :exceptions: None.
        '''
        store = MagicMock(count=0)
        tab: DslEditorTab = DslEditorTab(self.root)
        mock_toolbar = MagicMock()
        mock_toolbar.get_selected_example.return_value = 'demo.scara'
        mock_editor = MagicMock()
        mock_console = MagicMock()
        mock_exec = MagicMock()
        mock_file = MagicMock()
        mock_bin = MagicMock()

        tab.mount_views(
            toolbar=mock_toolbar, editor=mock_editor, console=mock_console
        )
        tab.mount_handlers(
            execution_handler=mock_exec,
            file_handler=mock_file,
            binary_handler=mock_bin,
            store=store,
        )
        tab.load_initial_content()

        mock_file.on_example_selected.assert_called_once_with('demo.scara')
        tab.destroy()

    def test_initialization_with_populated_store_exports_plan(self) -> None:
        '''
            Tests that DslEditorTab exports plan into editor when store contains waypoints.

            :exceptions: None.
        '''
        store = MagicMock(count=3)
        tab: DslEditorTab = DslEditorTab(self.root)
        mock_toolbar = MagicMock()
        mock_editor = MagicMock()
        mock_console = MagicMock()
        mock_exec = MagicMock()
        mock_file = MagicMock()
        mock_bin = MagicMock()

        tab.mount_views(
            toolbar=mock_toolbar, editor=mock_editor, console=mock_console
        )
        tab.mount_handlers(
            execution_handler=mock_exec,
            file_handler=mock_file,
            binary_handler=mock_bin,
            store=store,
        )
        tab.load_initial_content()

        mock_exec.export_plan_to_editor.assert_called_once()
        mock_file.on_example_selected.assert_not_called()
        tab.destroy()


if __name__ == '__main__':
    main()
