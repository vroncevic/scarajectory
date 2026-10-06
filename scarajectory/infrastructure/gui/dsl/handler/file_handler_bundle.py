# -*- coding: UTF-8 -*-

'''
Module
    file_handler_bundle.py
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
    Parameter bundle for DslEditorFileHandler collaborators.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Widget

from scarajectory.infrastructure.gui.dsl.code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.console_view import DslConsoleView
from scarajectory.infrastructure.gui.dsl.document.document_manager import DslDocumentManager
from scarajectory.infrastructure.gui.dsl.document.example_catalog import DslExampleCatalog

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True)
class FileHandlerBundle:
    '''
        Immutable container holding collaborators for DslEditorFileHandler.

        It defines:

            :attributes:
                | parent - Parent widget owning modal file dialogs.
                | editor - Multi-line DSL code editor component.
                | console - Status and diagnostics console view component.
                | catalog - Example scripts and demonstration catalog.
                | document_manager - Document persistence and modal dialog manager.
    '''

    parent: Widget
    editor: DslCodeEditor
    console: DslConsoleView
    catalog: DslExampleCatalog
    document_manager: DslDocumentManager
