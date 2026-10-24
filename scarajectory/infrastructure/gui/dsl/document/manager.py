# -*- coding: UTF-8 -*-

'''
Module
    manager.py
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
from typing import ClassVar, Final

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer

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
                | FILETYPES - Supported file extension filters.
                | DEFAULT_EXTENSION - Default file extension for saving.
                | TITLE_ERROR - Dialog title for error message box.
                | MSG_OPEN_ERROR - Error message template for read failures.
                | MSG_SAVE_ERROR - Error message template for write failures.
                | EMPTY_RESULT - Fallback empty string representation.
                | _loader - Plan loader port used for file reading.
                | _storer - Plan storer port used for file writing.
            :methods:
                | __init__ - Initializes the document manager with loader and storer.
                | open_document - Prompts file open dialog and loads script text.
                | save_document - Prompts file save dialog and writes script text to disk.
                | get_version - Returns document manager version string.
    '''

    FILETYPES: ClassVar[tuple[tuple[str, str], ...]] = (
        ('SCARA DSL Scripts', '*.scara'),
        ('All Files', '*.*'),
    )
    DEFAULT_EXTENSION: ClassVar[str] = '.scara'
    TITLE_ERROR: ClassVar[str] = 'File Error'
    MSG_OPEN_ERROR: ClassVar[str] = 'Failed to open file:\n{}'
    MSG_SAVE_ERROR: ClassVar[str] = 'Failed to save file:\n{}'
    EMPTY_RESULT: ClassVar[str] = ''

    _loader: IPlanLoader
    _storer: IPlanStorer

    def __init__(
        self,
        *,
        loader: IPlanLoader,
        storer: IPlanStorer,
    ) -> None:
        '''
            Initializes the document manager with loader and storer ports.

            :param loader: Required IPlanLoader implementation.
            :param storer: Required IPlanStorer implementation.
            :exceptions: None.
        '''
        self._loader: Final[IPlanLoader] = loader
        self._storer: Final[IPlanStorer] = storer

    def open_document(
        self,
        *,
        parent: Widget,
        initial_dir: str = '',
    ) -> tuple[str, str]:
        '''
            Presents modal file dialog to select a .scara file and loads its text content.

            :param parent: Parent widget owning the modal dialog.
            :param initial_dir: Starting filesystem directory path.
            :return: Tuple of (content, filepath) if loaded, or ('', '') if cancelled/failed.
            :exceptions: None.
        '''
        parent.update_idletasks()
        filepath: str = askopenfilename(
            parent=parent.winfo_toplevel(),
            initialdir=initial_dir if initial_dir else None,
            filetypes=self.FILETYPES,
        )

        if not filepath:
            return self.EMPTY_RESULT, self.EMPTY_RESULT

        try:
            content: str = self._loader.load_text_file(filepath=filepath)
            parent.update_idletasks()
            return content, filepath
        except OSError as exc:
            showerror(self.TITLE_ERROR, self.MSG_OPEN_ERROR.format(exc))
            return self.EMPTY_RESULT, self.EMPTY_RESULT

    def save_document(
        self,
        *,
        parent: Widget,
        content: str,
        initial_dir: str = '',
    ) -> str:
        '''
            Presents modal file save dialog and saves script text content to disk.

            :param parent: Parent widget owning the modal dialog.
            :param content: DSL script text to write.
            :param initial_dir: Starting filesystem directory path.
            :return: Filepath where script was saved, or empty string if cancelled/failed.
            :exceptions: None.
        '''
        parent.update_idletasks()
        filepath: str = asksaveasfilename(
            parent=parent.winfo_toplevel(),
            initialdir=initial_dir if initial_dir else None,
            defaultextension=self.DEFAULT_EXTENSION,
            filetypes=self.FILETYPES,
        )

        if not filepath:
            return self.EMPTY_RESULT

        try:
            self._storer.save_text_file(content=content, filepath=filepath)
            parent.update_idletasks()
            return filepath
        except OSError as exc:
            showerror(self.TITLE_ERROR, self.MSG_SAVE_ERROR.format(exc))
            return self.EMPTY_RESULT

    def get_version(self) -> str:
        '''
            Returns the document manager version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
