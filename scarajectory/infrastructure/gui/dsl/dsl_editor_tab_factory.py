# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_tab_factory.py
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
    Factory module for assembling and instantiating DslEditorTab components.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.dsl.bundle import DslEditorBundle
from scarajectory.infrastructure.gui.dsl.code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.code_editor_factory import DslCodeEditorFactory
from scarajectory.infrastructure.gui.dsl.console_view import DslConsoleView
from scarajectory.infrastructure.gui.dsl.document.document_manager import DslDocumentManager
from scarajectory.infrastructure.gui.dsl.document.document_manager_factory import DslDocumentManagerFactory
from scarajectory.infrastructure.gui.dsl.document.example_catalog import DslExampleCatalog
from scarajectory.infrastructure.gui.dsl.document.example_catalog_factory import DslExampleCatalogFactory
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.dsl.handler.binary_handler import DslEditorBinaryHandler
from scarajectory.infrastructure.gui.dsl.handler.binary_handler_bundle import BinaryHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.binary_handler_factory import DslEditorBinaryHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.execution_handler import DslEditorExecutionHandler
from scarajectory.infrastructure.gui.dsl.handler.execution_handler_bundle import ExecutionHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.execution_handler_factory import DslEditorExecutionHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.file_handler import DslEditorFileHandler
from scarajectory.infrastructure.gui.dsl.handler.file_handler_bundle import FileHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.file_handler_factory import DslEditorFileHandlerFactory
from scarajectory.infrastructure.gui.dsl.toolbar import DslEditorToolbar
from scarajectory.infrastructure.gui.emulator.emulator_launcher_factory import EmulatorLauncherFactory
from scarajectory.infrastructure.gui.emulator.iemulator_launcher import IEmulatorLauncher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorTabFactory:
    '''
        Factory responsible for assembling DslEditorTab GUI instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a DslEditorTab with bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, parent: Widget, *, bundle: DslEditorBundle) -> DslEditorTab:
        '''
            Assembles and instantiates a DslEditorTab with standard collaborators.

            :param parent: Parent container widget.
            :param bundle: Injected DslEditorBundle dependency bundle.
            :return: Fully assembled DslEditorTab.
            :exceptions: None.
        '''
        tab: DslEditorTab = DslEditorTab(parent)

        editor: DslCodeEditor = DslCodeEditorFactory.create_default(tab)
        console: DslConsoleView = DslConsoleView(tab)

        launcher: IEmulatorLauncher = EmulatorLauncherFactory.create()
        catalog: DslExampleCatalog = (
            DslExampleCatalogFactory.create_default(storage=bundle.storage)
        )
        document_manager: DslDocumentManager = (
            DslDocumentManagerFactory.create(storage=bundle.storage)
        )

        execution_handler: DslEditorExecutionHandler = (
            DslEditorExecutionHandlerFactory.create(
                bundle=ExecutionHandlerBundle(
                    store=bundle.store,
                    mutation=bundle.mutation,
                    dsl=bundle.dsl,
                    launcher=launcher,
                    editor=editor,
                    console=console,
                )
            )
        )

        file_handler: DslEditorFileHandler = (
            DslEditorFileHandlerFactory.create(
                bundle=FileHandlerBundle(
                    parent=tab,
                    editor=editor,
                    console=console,
                    catalog=catalog,
                    document_manager=document_manager,
                )
            )
        )

        binary_handler: DslEditorBinaryHandler = (
            DslEditorBinaryHandlerFactory.create(
                bundle=BinaryHandlerBundle(
                    parent=tab,
                    editor=editor,
                    console=console,
                    compiler=bundle.dsl.compiler,
                    decompiler=bundle.dsl.decompiler,
                    storage=bundle.storage,
                    diagnostics=bundle.dsl.diagnostics,
                )
            )
        )

        toolbar: DslEditorToolbar = DslEditorToolbar(
            tab,
            execution_delegate=execution_handler,
            file_delegate=file_handler,
            binary_delegate=binary_handler,
        )
        example_files: list[str] = catalog.get_example_files()

        if example_files:
            toolbar.set_example_files(example_files)

        tab.mount_views(toolbar=toolbar, editor=editor, console=console)
        tab.mount_handlers(
            execution_handler=execution_handler,
            file_handler=file_handler,
            binary_handler=binary_handler,
            store=bundle.store,
        )
        tab.load_initial_content()

        return tab

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
