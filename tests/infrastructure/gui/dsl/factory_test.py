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
    Unit tests for DslEditorTabFactory.
'''

from __future__ import annotations

from tkinter import Tk
from types import SimpleNamespace
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.dsl.bundle import DslEditorBundle
from scarajectory.infrastructure.gui.dsl.factory import DslEditorTabFactory
from scarajectory.infrastructure.gui.dsl.tab import DslEditorTab
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle
from scarajectory.setup.assembly.dsl.diagnostic_bundle import DslDiagnosticBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorTabFactory(TestCase):
    '''
        Test cases verifying DslEditorTabFactory creation and version.
    '''

    root: Tk
    mocks: SimpleNamespace

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def setUp(self) -> None:
        mocks = SimpleNamespace(
            store=MagicMock(count=0),
            mutation=MagicMock(),
            compiler=MagicMock(),
            validator=MagicMock(),
            exporter=MagicMock(),
            loader=MagicMock(),
            storer=MagicMock(),
            launcher=MagicMock(),
            catalog=MagicMock(),
            doc_manager=MagicMock(),
        )
        mocks.catalog.get_example_files.return_value = ['demo.scara']
        mocks.catalog.get_default_script.return_value = 'DEFAULT_SCRIPT'
        mocks.catalog.load_example_content.return_value = 'DEMO_SCRIPT'
        self.mocks = mocks

    def test_factory_version(self) -> None:
        '''
            Tests DslEditorTabFactory version string.

            :exceptions: None.
        '''
        self.assertEqual(DslEditorTabFactory.get_version(), '1.0.3')

    @patch(
        'scarajectory.infrastructure.gui.dsl.factory.'
        'EmulatorLauncherFactory.create'
    )
    @patch(
        'scarajectory.infrastructure.gui.dsl.factory.'
        'DslExampleCatalogFactory.create_default'
    )
    @patch(
        'scarajectory.infrastructure.gui.dsl.factory.'
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

            :exceptions: None.
        '''
        mock_launcher_create.return_value = self.mocks.launcher
        mock_cat_create.return_value = self.mocks.catalog
        mock_doc_mgr_create.return_value = self.mocks.doc_manager

        dsl_bundle = DslPipelineBundle(
            compiler=MagicMock(),
            decompiler=MagicMock(),
            plan_compiler=self.mocks.compiler,
            plan_exporter=self.mocks.exporter,
            validator=self.mocks.validator,
            diagnostics=MagicMock(spec=DslDiagnosticBundle),
        )
        bundle: DslEditorBundle = DslEditorBundle(
            store=self.mocks.store,
            mutation=self.mocks.mutation,
            dsl=dsl_bundle,
            loader=self.mocks.loader,
            storer=self.mocks.storer,
            workspace=MagicMock(spec=IWorkspaceManager),
        )
        tab: DslEditorTab = DslEditorTabFactory.create(self.root, bundle=bundle)
        self.assertIsInstance(tab, DslEditorTab)
        tab.destroy()


if __name__ == '__main__':
    main()
