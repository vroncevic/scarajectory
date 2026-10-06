# -*- coding: UTF-8 -*-

'''
Module
    binary_handler.py
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
    Action handler executing binary program file export and decompilation.
'''

from __future__ import annotations

from tkinter import Widget
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.infrastructure.gui.dsl.code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.console_view import DslConsoleView
from scarajectory.infrastructure.gui.dsl.handler.binary_handler_bundle import BinaryHandlerBundle
from scarajectory.setup.pipeline.dsl_diagnostic_bundle import DslDiagnosticBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorBinaryHandler:
    '''
        Action handler executing binary compilation export and binary file decompilation.

        It defines:

            :attributes:
                | _parent - Parent widget owning modal file dialogs.
                | _editor - Code editor subcomponent.
                | _console - Diagnostic console view subcomponent.
                | _compiler - SCARA wire and binary compiler service.
                | _decompiler - Binary program decompilation service.
                | _storage - Plan and binary file storage service.
                | _diagnostics - SCARA DSL diagnostic and error handling services bundle.
            :methods:
                | __init__ - Initializes the binary action handler with bundle.
                | export_binary_file - Prompts save dialog and exports active DSL script to .bin.
                | import_binary_file - Prompts open dialog, decompiles .bin and loads into editor.
                | get_version - Returns the handler version string representation.
    '''

    _parent: Widget
    _editor: DslCodeEditor
    _console: DslConsoleView
    _compiler: IScaraCompiler
    _decompiler: IScaraDecompiler
    _storage: IPlanStorageService
    _diagnostics: DslDiagnosticBundle

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
        self._editor: Final[DslCodeEditor] = bundle.editor
        self._console: Final[DslConsoleView] = bundle.console
        self._compiler: Final[IScaraCompiler] = bundle.compiler
        self._decompiler: Final[IScaraDecompiler] = bundle.decompiler
        self._storage: Final[IPlanStorageService] = bundle.storage
        self._diagnostics: Final[DslDiagnosticBundle] = bundle.diagnostics

    def export_binary_file(self) -> None:
        '''
            Presents modal save dialog and exports editor DSL content to a binary file.

            :exceptions: None.
        '''
        content: str = self._editor.get_text().strip()

        if not content:
            self._console.append_log(
                '❌ Editor is empty. Nothing to export to binary.',
                level='warning',
            )
            return

        self._parent.update_idletasks()
        filepath: str = asksaveasfilename(
            parent=self._parent.winfo_toplevel(),
            defaultextension='.bin',
            filetypes=[('SCARA Binary Program', '*.bin'), ('All Files', '*.*')],
        )

        if not filepath:
            return

        try:
            program: BinaryProgram = self._compiler.compile_to_binary(
                source=content
            )
            self._storage.save_binary_file(
                content=program.raw_bytes,
                filepath=filepath,
            )
            step_count: int = len(program.steps)
            self._console.append_log(
                f'✅ Successfully exported binary program ({step_count} steps) to {filepath}',
                level='success',
            )
        except Exception as err:
            err_msg: str = self._diagnostics.compile_error_handler.format_error(
                error=err
            )
            self._console.append_log(
                f'❌ Binary export failed: {err_msg}',
                level='error',
            )

    def import_binary_file(self) -> None:
        '''
            Presents modal open dialog, decompiles selected binary file, and loads into editor.

            :exceptions: None.
        '''
        self._parent.update_idletasks()
        filepath: str = askopenfilename(
            parent=self._parent.winfo_toplevel(),
            filetypes=[('SCARA Binary Program', '*.bin'), ('All Files', '*.*')],
        )

        if not filepath:
            return

        try:
            raw_bytes: bytes = self._storage.load_binary_file(filepath=filepath)
            dsl_code: str = self._decompiler.decompile_bytes(data=raw_bytes)
            self._editor.set_text(dsl_code)
            self._console.append_log(
                f'✅ Successfully decompiled binary program from {filepath} into editor.',
                level='success',
            )
        except Exception as err:
            err_msg: str = self._diagnostics.decompile_error_handler.format_error(
                error=err
            )
            self._console.append_log(
                f'❌ Binary decompile failed: {err_msg}',
                level='error',
            )

    def get_version(self) -> str:
        '''
            Returns the handler version string representation.

            :return: Handler version string.
            :exceptions: None.
        '''
        return __version__
