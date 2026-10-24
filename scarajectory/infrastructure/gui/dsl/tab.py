# -*- coding: UTF-8 -*-

'''
Module
    tab.py
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
    Dedicated SCARA DSL code editor tab container integrated into controls notebook.
'''

from __future__ import annotations

from tkinter import BOTH, Widget, X
from tkinter.ttk import Frame
from typing import ClassVar

from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.infrastructure.gui.dsl.handler.binary.idelegate import IDslBinaryDelegate
from scarajectory.infrastructure.gui.dsl.handler.execution.idelegate import IDslExecutionDelegate
from scarajectory.infrastructure.gui.dsl.handler.file.idelegate import IDslFileDelegate
from scarajectory.infrastructure.gui.dsl.toolbar.itoolbar import IDslEditorToolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorTab(Frame):
    '''
        SCARA DSL script editor presentation container frame.

        It defines:

            :attributes:
                | PADDING - Default frame inner padding.
                | PAD_CONSOLE_Y - Vertical padding tuple for diagnostic console.
                | _store - Injected waypoint query collaborator.
                | _toolbar - Action toolbar subcomponent.
                | _editor - Code editor subcomponent.
                | _console - Diagnostic console view subcomponent.
                | _execution_handler - Delegate for DSL execution actions.
                | _file_handler - Delegate for DSL file and example actions.
                | _binary_handler - Delegate for DSL binary actions.
            :methods:
                | __init__ - Initializes the editor tab container frame.
                | mount_views - Mounts toolbar, editor, and console subcomponents.
                | mount_handlers - Injects execution, file, and binary delegates.
                | load_initial_content - Loads exported plan or demonstration script.
                | get_version - Returns tab component version string.
    '''

    PADDING: ClassVar[int] = 4
    PAD_CONSOLE_Y: ClassVar[tuple[int, int]] = (4, 0)

    _store: IWaypointStore
    _toolbar: IDslEditorToolbar
    _editor: IDslCodeEditor
    _console: IDslConsoleView
    _execution_handler: IDslExecutionDelegate
    _file_handler: IDslFileDelegate
    _binary_handler: IDslBinaryDelegate

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes the SCARA DSL editor tab container frame.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, padding=self.PADDING)

    def mount_views(
        self,
        *,
        toolbar: IDslEditorToolbar,
        editor: IDslCodeEditor,
        console: IDslConsoleView,
    ) -> None:
        '''
            Mounts and packs toolbar, code editor, and console view subcomponents.

            :param toolbar: Assembled action toolbar.
            :param editor: Syntax-highlighted code editor.
            :param console: Diagnostic output console.
            :exceptions: None.
        '''
        self._toolbar = toolbar
        self._toolbar.pack(fill=X)

        self._editor = editor
        self._editor.pack(fill=BOTH, expand=True)

        self._console = console
        self._console.pack(fill=X, pady=self.PAD_CONSOLE_Y)

    def mount_handlers(
        self,
        *,
        execution_handler: IDslExecutionDelegate,
        file_handler: IDslFileDelegate,
        binary_handler: IDslBinaryDelegate,
        store: IWaypointStore,
    ) -> None:
        '''
            Injects action delegates and store collaborator.

            :param execution_handler: Delegate handling compilation and execution.
            :param file_handler: Delegate handling file persistence and demo loading.
            :param binary_handler: Delegate handling binary program export and decompilation.
            :param store: Waypoint query store.
            :exceptions: None.
        '''
        self._execution_handler = execution_handler
        self._file_handler = file_handler
        self._binary_handler = binary_handler
        self._store = store

    def load_initial_content(self) -> None:
        '''
            Loads either the exported active plan or demonstration script into the editor.

            :exceptions: None.
        '''
        if self._store.count > 0:
            self._execution_handler.export_plan_to_editor()
        else:
            selected: str = self._toolbar.get_selected_example()
            self._file_handler.on_example_selected(selected)

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component semantic version.
            :exceptions: None.
        '''
        return __version__
