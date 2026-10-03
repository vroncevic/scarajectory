# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_tab_test.py
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
    Unit tests for DslEditorTab and DslEditorTabFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.dsl.bundle import DslEditorBundle
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab_factory import DslEditorTabFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
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

    def setUp(self) -> None:
        self.mock_store = MagicMock()
        self.mock_store.count = 0
        self.mock_mutation = MagicMock()
        self.mock_dsl_service = MagicMock()
        self.mock_storage = MagicMock()
        self.mock_launcher = MagicMock()
        self.mock_catalog = MagicMock()
        self.mock_catalog.get_example_files.return_value = ['demo.scara']
        self.mock_catalog.get_default_script.return_value = 'DEFAULT_SCRIPT'
        self.mock_catalog.load_example_content.return_value = 'DEMO_SCRIPT'
        self.mock_doc_manager = MagicMock()

    def test_factory_version(self) -> None:
        '''
            Tests DslEditorTabFactory version string.
        '''
        self.assertEqual(DslEditorTabFactory.get_version(), '1.0.4')

    def test_initialization_with_empty_store_loads_example(self) -> None:
        '''
            Tests that DslEditorTab loads example script when store is empty.
        '''
        self.mock_store.count = 0
        tab: DslEditorTab = DslEditorTab(self.root)
        mock_toolbar = MagicMock()
        mock_toolbar.get_selected_example.return_value = 'demo.scara'
        mock_editor = MagicMock()
        mock_console = MagicMock()
        mock_exec = MagicMock()
        mock_file = MagicMock()

        tab.mount_views(toolbar=mock_toolbar, editor=mock_editor, console=mock_console)
        tab.mount_handlers(
            execution_handler=mock_exec,
            file_handler=mock_file,
            store=self.mock_store,
        )
        tab.load_initial_content()

        self.assertIs(tab.editor, mock_editor)
        self.assertIs(tab.console, mock_console)
        self.assertIs(tab.toolbar, mock_toolbar)
        self.assertIs(tab.execution_handler, mock_exec)
        self.assertIs(tab.file_handler, mock_file)
        mock_file.on_example_selected.assert_called_once_with('demo.scara')
        tab.destroy()

    def test_initialization_with_populated_store_exports_plan(self) -> None:
        '''
            Tests that DslEditorTab exports plan into editor when store contains waypoints.
        '''
        self.mock_store.count = 3
        tab: DslEditorTab = DslEditorTab(self.root)
        mock_toolbar = MagicMock()
        mock_editor = MagicMock()
        mock_console = MagicMock()
        mock_exec = MagicMock()
        mock_file = MagicMock()

        tab.mount_views(toolbar=mock_toolbar, editor=mock_editor, console=mock_console)
        tab.mount_handlers(
            execution_handler=mock_exec,
            file_handler=mock_file,
            store=self.mock_store,
        )
        tab.load_initial_content()

        mock_exec.export_plan_to_editor.assert_called_once()
        mock_file.on_example_selected.assert_not_called()
        tab.destroy()

    @patch(
        'scarajectory.infrastructure.gui.dsl.dsl_editor_tab_factory.'
        'EmulatorLauncherFactory.create'
    )
    @patch(
        'scarajectory.infrastructure.gui.dsl.dsl_editor_tab_factory.'
        'DslExampleCatalogFactory.create_default'
    )
    @patch(
        'scarajectory.infrastructure.gui.dsl.dsl_editor_tab_factory.'
        'DslDocumentManagerFactory.create'
    )
    def test_factory_create(
        self,
        mock_doc_mgr_create: MagicMock,
        mock_cat_create: MagicMock,
        mock_launcher_create: MagicMock,
    ) -> None:
        '''
            Tests that DslEditorTabFactory.create assembles collaborating
            services and returns DslEditorTab.
        '''
        mock_launcher_create.return_value = self.mock_launcher
        mock_cat_create.return_value = self.mock_catalog
        mock_doc_mgr_create.return_value = self.mock_doc_manager

        bundle: DslEditorBundle = DslEditorBundle(
            store=self.mock_store,
            mutation=self.mock_mutation,
            dsl_service=self.mock_dsl_service,
            storage=self.mock_storage,
        )
        tab: DslEditorTab = DslEditorTabFactory.create(self.root, bundle=bundle)
        self.assertIsInstance(tab, DslEditorTab)
        tab.destroy()


if __name__ == '__main__':
    main()
