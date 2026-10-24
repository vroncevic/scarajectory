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
    Action handler executing binary compilation export and binary decompilation.
'''

from __future__ import annotations

from tkinter import Widget
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import ClassVar, Final

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.infrastructure.gui.dsl.handler.binary.bundle import BinaryHandlerBundle
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslBinaryHandler:
    '''
        Action handler executing binary compilation export and binary file decompilation.

        It defines:

            :attributes:
                | DEFAULT_EXT_BIN - Default extension for binary programs.
                | FILETYPES_BIN - Supported file type filters for binary dialogs.
                | MSG_EMPTY_EDITOR - Warning message shown when editor is empty.
                | LOG_LEVEL_WARNING - Warning log level tag.
                | LOG_LEVEL_SUCCESS - Success log level tag.
                | LOG_LEVEL_ERROR - Error log level tag.
                | _parent - Parent widget owning modal file dialogs.
                | _editor - Code editor structural protocol subcomponent.
                | _console - Diagnostic console view structural protocol subcomponent.
                | _dsl - SCARA DSL pipeline role services bundle.
                | _loader - Plan and binary file loader port.
                | _storer - Plan and binary file storer port.
            :methods:
                | __init__ - Initializes the binary action handler with bundle.
                | export_binary_file - Prompts save dialog and exports active DSL script to .bin.
                | import_binary_file - Prompts open dialog, decompiles .bin and loads into editor.
                | get_version - Returns the handler version string representation.
    '''

    DEFAULT_EXT_BIN: ClassVar[str] = '.bin'
    FILETYPES_BIN: ClassVar[tuple[tuple[str, str], ...]] = (
        ('SCARA Binary Program', '*.bin'),
        ('All Files', '*.*'),
    )
    MSG_EMPTY_EDITOR: ClassVar[str] = (
        '❌ Editor is empty. Nothing to export to binary.'
    )
    LOG_LEVEL_WARNING: ClassVar[str] = 'warning'
    LOG_LEVEL_SUCCESS: ClassVar[str] = 'success'
    LOG_LEVEL_ERROR: ClassVar[str] = 'error'

    _parent: Widget
    _editor: IDslCodeEditor
    _console: IDslConsoleView
    _dsl: DslPipelineBundle
    _loader: IPlanLoader
    _storer: IPlanStorer

    def __init__(
        self,
        *,
        bundle: BinaryHandlerBundle,
    ) -> None:
        '''
            Initializes the binary action handler with collaborators bundle.

            :param bundle: Required BinaryHandlerBundle container.
            :exceptions: None.
        '''
        self._parent: Final[Widget] = bundle.parent
        self._editor: Final[IDslCodeEditor] = bundle.editor
        self._console: Final[IDslConsoleView] = bundle.console
        self._dsl: Final[DslPipelineBundle] = bundle.dsl
        self._loader: Final[IPlanLoader] = bundle.loader
        self._storer: Final[IPlanStorer] = bundle.storer

    def export_binary_file(self) -> None:
        '''
            Presents modal save dialog and exports editor DSL content to a binary file.

            :exceptions: None.
        '''
        content: str = self._editor.get_text().strip()

        if not content:
            self._console.append_log(
                self.MSG_EMPTY_EDITOR,
                level=self.LOG_LEVEL_WARNING,
            )
            return

        self._parent.update_idletasks()
        filepath: str = asksaveasfilename(
            parent=self._parent.winfo_toplevel(),
            defaultextension=self.DEFAULT_EXT_BIN,
            filetypes=list(self.FILETYPES_BIN),
        )

        if not filepath:
            return

        try:
            program: BinaryProgram = self._dsl.compiler.compile(
                source=content
            )
            self._storer.save_binary_file(
                content=program.raw_bytes,
                filepath=filepath,
            )
            step_count: int = len(program.steps)
            self._console.append_log(
                f'✅ Successfully exported binary program ({step_count} steps)'
                f' to {filepath}',
                level=self.LOG_LEVEL_SUCCESS,
            )
        except Exception as err:
            err_msg: str = (
                self._dsl.diagnostics.compile_error_handler.format_error(
                    error=err
                )
            )
            self._console.append_log(
                f'❌ Binary export failed: {err_msg}',
                level=self.LOG_LEVEL_ERROR,
            )

    def import_binary_file(self) -> None:
        '''
            Presents modal open dialog, decompiles selected binary file, and loads into editor.

            :exceptions: None.
        '''
        self._parent.update_idletasks()
        filepath: str = askopenfilename(
            parent=self._parent.winfo_toplevel(),
            filetypes=list(self.FILETYPES_BIN),
        )

        if not filepath:
            return

        try:
            raw_bytes: bytes = self._loader.load_binary_file(filepath=filepath)
            dsl_code: str = self._dsl.decompiler.decompile_bytes(
                data=raw_bytes
            )
            self._editor.set_text(dsl_code)
            self._console.append_log(
                f'✅ Successfully decompiled binary program from {filepath}'
                ' into editor.',
                level=self.LOG_LEVEL_SUCCESS,
            )
        except Exception as err:
            err_msg: str = (
                self._dsl.diagnostics.decompile_error_handler.format_error(
                    error=err
                )
            )
            self._console.append_log(
                f'❌ Binary decompile failed: {err_msg}',
                level=self.LOG_LEVEL_ERROR,
            )

    def get_version(self) -> str:
        '''
            Returns the handler version string representation.

            :return: Handler version string.
            :exceptions: None.
        '''
        return __version__
