# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
    Handles DSL file opening, saving, and example loading actions.
'''

from __future__ import annotations

from tkinter import Widget
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.dsl.catalog.icatalog import IDslExampleCatalog
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView
from scarajectory.infrastructure.gui.dsl.document.imanager import IDslDocumentManager
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.infrastructure.gui.dsl.handler.file.bundle import FileHandlerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslFileHandler:
    '''
        Action handler executing DSL script persistence, file opening, and example loading.

        It defines:

            :attributes:
                | MSG_DEFAULT_DEMO - Log message when loading default fallback demo script.
                | _parent - Parent widget owning modal file dialogs.
                | _editor - Code editor structural protocol subcomponent.
                | _console - Diagnostic console view structural protocol subcomponent.
                | _catalog - Example scripts and demonstration catalog structural protocol.
                | _document_manager - Document persistence and modal dialog manager.
            :methods:
                | __init__ - Initializes the file action handler with bundle.
                | open_file - Opens a .scara DSL script file from storage.
                | save_file - Persists active DSL script to a file.
                | on_example_selected - Loads example script content into editor.
                | get_version - Returns the handler version string representation.
    '''

    MSG_DEFAULT_DEMO: ClassVar[str] = (
        'ℹ️ Demonstration SCARA DSL script loaded.'
    )

    _parent: Widget
    _editor: IDslCodeEditor
    _console: IDslConsoleView
    _catalog: IDslExampleCatalog
    _document_manager: IDslDocumentManager

    def __init__(
        self,
        *,
        bundle: FileHandlerBundle,
    ) -> None:
        '''
            Initializes the file action handler with collaborators bundle.

            :param bundle: Required FileHandlerBundle container.
            :exceptions: None.
        '''
        self._parent: Final[Widget] = bundle.parent
        self._editor: Final[IDslCodeEditor] = bundle.editor
        self._console: Final[IDslConsoleView] = bundle.console
        self._catalog: Final[IDslExampleCatalog] = bundle.catalog
        self._document_manager: Final[IDslDocumentManager] = (
            bundle.document_manager
        )

    def open_file(self) -> None:
        '''
            Presents modal open file dialog and loads script into editor.

            :exceptions: None.
        '''
        content, filepath = self._document_manager.open_document(
            parent=self._parent,
            initial_dir=str(self._catalog.examples_dir()),
        )

        if filepath:
            self._editor.set_text(content)
            self._console.log(f'ℹ️ Loaded file: {filepath}', is_error=False)

    def save_file(self) -> None:
        '''
            Presents modal save file dialog and saves editor content to disk.

            :exceptions: None.
        '''
        content: str = self._editor.get_text()
        filepath: str = self._document_manager.save_document(
            parent=self._parent,
            content=content,
            initial_dir=str(self._catalog.examples_dir()),
        )

        if filepath:
            self._console.log(f'ℹ️ Saved file: {filepath}', is_error=False)

    def on_example_selected(self, example_name: str) -> None:
        '''
            Loads the selected example script from disk into the editor.

            :param example_name: Name of selected example file.
            :exceptions: None.
        '''
        if example_name:
            content: str = self._catalog.load_example_content(
                filename=example_name
            )

            if content:
                self._editor.set_text(content)
                self._console.log(
                    f'ℹ️ Loaded example: {example_name}', is_error=False
                )

                return

        self._console.log(self.MSG_DEFAULT_DEMO, is_error=False)

    def get_version(self) -> str:
        '''
            Returns the handler version string representation.

            :return: Handler version string.
            :exceptions: None.
        '''
        return __version__
