# -*- coding: UTF-8 -*-

'''
Module
    binary_handler_bundle.py
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
    Parameter bundle for DslEditorBinaryHandler collaborators.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Widget

from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.infrastructure.gui.dsl.code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.console_view import DslConsoleView
from scarajectory.setup.pipeline.dsl_diagnostic_bundle import DslDiagnosticBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class BinaryHandlerBundle:
    '''
        Immutable container holding collaborators for DslEditorBinaryHandler.

        It defines:

            :attributes:
                | parent - Parent widget owning modal file dialogs.
                | editor - Multi-line DSL code editor component.
                | console - Status and diagnostics console view component.
                | compiler - SCARA wire and binary compiler service.
                | decompiler - Binary program decompilation service.
                | storage - Plan and binary file storage service.
                | diagnostics - SCARA DSL diagnostic and error handling services bundle.
    '''

    parent: Widget
    editor: DslCodeEditor
    console: DslConsoleView
    compiler: IScaraCompiler
    decompiler: IScaraDecompiler
    storage: IPlanStorageService
    diagnostics: DslDiagnosticBundle
