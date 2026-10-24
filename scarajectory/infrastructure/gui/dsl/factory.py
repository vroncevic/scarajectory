# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
from scarajectory.infrastructure.gui.dsl.catalog.catalog import DslExampleCatalog
from scarajectory.infrastructure.gui.dsl.catalog.factory import DslExampleCatalogFactory
from scarajectory.infrastructure.gui.dsl.console.console import DslConsoleView
from scarajectory.infrastructure.gui.dsl.console.factory import DslConsoleViewFactory
from scarajectory.infrastructure.gui.dsl.document.factory import DslDocumentManagerFactory
from scarajectory.infrastructure.gui.dsl.document.manager import DslDocumentManager
from scarajectory.infrastructure.gui.dsl.editor.editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.editor.factory import DslCodeEditorFactory
from scarajectory.infrastructure.gui.dsl.handler.binary.bundle import BinaryHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.binary.factory import DslBinaryHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.binary.handler import DslBinaryHandler
from scarajectory.infrastructure.gui.dsl.handler.execution.bundle import ExecutionHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.execution.factory import DslExecutionHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.execution.handler import DslExecutionHandler
from scarajectory.infrastructure.gui.dsl.handler.file.bundle import FileHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.file.factory import DslFileHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.file.handler import DslFileHandler
from scarajectory.infrastructure.gui.dsl.tab import DslEditorTab
from scarajectory.infrastructure.gui.dsl.toolbar.bundle import DslEditorToolbarBundle
from scarajectory.infrastructure.gui.dsl.toolbar.factory import DslEditorToolbarFactory
from scarajectory.infrastructure.gui.dsl.toolbar.toolbar import DslEditorToolbar
from scarajectory.infrastructure.gui.emulator.launcher.factory import EmulatorLauncherFactory
from scarajectory.infrastructure.gui.emulator.launcher.ilauncher import IEmulatorLauncher

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
    def create(
        cls,
        parent: Widget,
        *,
        bundle: DslEditorBundle,
    ) -> DslEditorTab:
        '''
            Assembles and instantiates a DslEditorTab with standard collaborators.

            :param parent: Parent container widget.
            :param bundle: Injected DslEditorBundle dependency bundle.
            :return: Fully assembled DslEditorTab.
            :exceptions: None.
        '''
        tab: DslEditorTab = DslEditorTab(parent)

        editor: DslCodeEditor = DslCodeEditorFactory.create_default(tab)
        console: DslConsoleView = DslConsoleViewFactory.create(tab)

        launcher: IEmulatorLauncher = EmulatorLauncherFactory.create()
        catalog: DslExampleCatalog = DslExampleCatalogFactory.create_default(
            loader=bundle.loader,
            workspace=bundle.workspace,
        )
        document_manager: DslDocumentManager = (
            DslDocumentManagerFactory.create(
                loader=bundle.loader,
                storer=bundle.storer,
            )
        )

        execution_handler: DslExecutionHandler = (
            DslExecutionHandlerFactory.create(
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

        file_handler: DslFileHandler = DslFileHandlerFactory.create(
            bundle=FileHandlerBundle(
                parent=tab,
                editor=editor,
                console=console,
                catalog=catalog,
                document_manager=document_manager,
            )
        )

        binary_handler: DslBinaryHandler = DslBinaryHandlerFactory.create(
            bundle=BinaryHandlerBundle(
                parent=tab,
                editor=editor,
                console=console,
                dsl=bundle.dsl,
                loader=bundle.loader,
                storer=bundle.storer,
            )
        )

        toolbar: DslEditorToolbar = DslEditorToolbarFactory.create(
            tab,
            bundle=DslEditorToolbarBundle(
                execution_delegate=execution_handler,
                file_delegate=file_handler,
                binary_delegate=binary_handler,
            ),
        )
        example_files: tuple[str, ...] = catalog.get_example_files()

        if example_files:
            toolbar.set_example_files(list(example_files))

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
