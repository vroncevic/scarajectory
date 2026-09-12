# -*- coding: UTF-8 -*-

'''
Module
    dsl_document_manager.py
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
    Manages filesystem dialogs and document persistence for the SCARA DSL script editor.
'''

from __future__ import annotations

from tkinter import Widget
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror

from scarajectory.core.service.trajectory.iplan_storage_service import (
    IPlanStorageService,
)
from scarajectory.infrastructure.storage.plan_storage_service import (
    PlanStorageService,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslDocumentManager:
    '''
        Orchestrates modal file dialogs and script document persistence.

        It defines:

            :attributes:
                | _storage - Plan storage service instance used for file I/O.
            :methods:
                | __init__ - Initializes the document manager with storage service.
                | open_document - Prompts file open dialog and loads script text.
                | save_document - Prompts file save dialog and writes script text to disk.
    '''

    _storage: IPlanStorageService

    def __init__(
        self,
        *,
        storage: IPlanStorageService | None = None,
    ) -> None:
        '''
            Initializes the document manager with storage service.

            :param storage: Optional IPlanStorageService implementation.
            :exceptions: None.
        '''
        self._storage = (
            storage
            if storage is not None
            else PlanStorageService()
        )

    def open_document(
        self,
        *,
        parent: Widget,
        initial_dir: str | None = None,
    ) -> tuple[str, str] | None:
        '''
            Presents modal file dialog to select a .scara file and loads its text content.

            :param parent: Parent widget owning the modal dialog.
            :param initial_dir: Optional starting filesystem directory path.
            :return: Tuple of (content, filepath) if successfully loaded, or None if cancelled/failed.
            :exceptions: None.
        '''
        parent.update_idletasks()
        filepath: str = askopenfilename(
            parent=parent.winfo_toplevel(),
            initialdir=initial_dir,
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')],
        )
        if not filepath:
            return None

        try:
            content: str = self._storage.load_text_file(filepath)
            parent.update_idletasks()
            return content, filepath

        except OSError as exc:
            showerror('File Error', f'Failed to open file:\n{exc}')
            return None

    def save_document(
        self,
        *,
        parent: Widget,
        content: str,
    ) -> str | None:
        '''
            Presents modal file save dialog and saves script text content to disk.

            :param parent: Parent widget owning the modal dialog.
            :param content: DSL script text to write.
            :return: Filepath where script was saved, or None if cancelled/failed.
            :exceptions: None.
        '''
        parent.update_idletasks()
        filepath: str = asksaveasfilename(
            parent=parent.winfo_toplevel(),
            defaultextension='.scara',
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')],
        )
        if not filepath:
            return None

        try:
            self._storage.save_text_file(content, filepath)
            parent.update_idletasks()
            return filepath

        except OSError as exc:
            showerror('File Error', f'Failed to save file:\n{exc}')
            return None
