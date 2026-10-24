# -*- coding: UTF-8 -*-

'''
Module
    imanager.py
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
    Defines structural protocol IDslDocumentManager for document dialog persistence.
'''

from __future__ import annotations

from tkinter import Widget
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDslDocumentManager(Protocol):
    '''
        Structural protocol defining document persistence and modal file dialogs.

        It defines:

            :methods:
                | open_document - Prompts file open dialog and loads script text.
                | save_document - Prompts file save dialog and writes script text.
                | get_version - Returns document manager component version string.
    '''

    def open_document(
        self,
        *,
        parent: Widget,
        initial_dir: str = '',
    ) -> tuple[str, str]:
        '''
            Presents modal file dialog to select a .scara file and loads content.

            :param parent: Parent widget owning the modal dialog.
            :param initial_dir: Optional starting directory path.
            :return: Tuple of (content, filepath) if loaded, or ('', '') if cancelled.
        '''

    def save_document(
        self,
        *,
        parent: Widget,
        content: str,
        initial_dir: str = '',
    ) -> str:
        '''
            Presents modal file save dialog and saves script content to disk.

            :param parent: Parent widget owning the modal dialog.
            :param content: DSL script text to write.
            :param initial_dir: Optional starting directory path.
            :return: Filepath where script was saved, or empty string if cancelled.
        '''

    def get_version(self) -> str:
        '''
            Returns document manager component version string.

            :return: Semantic version string.
        '''
