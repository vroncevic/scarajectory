# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Parameter bundle for DslBinaryHandler collaborators.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Widget

from scaralang.core.service.compiler.icompiler import IScaraCompiler
from scaralang.core.service.decompiler.idecompiler import IScaraDecompiler
from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.setup.assembly.dsl.diagnostic_bundle import DslDiagnosticBundle
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle

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
        Immutable container holding collaborators for DslBinaryHandler.

        It defines:

            :attributes:
                | parent - Parent widget owning modal file dialogs.
                | editor - Multi-line DSL code editor structural protocol.
                | console - Status and diagnostics console view structural protocol.
                | dsl - SCARA DSL pipeline role services bundle.
                | loader - Plan and binary file loader port.
                | storer - Plan and binary file storer port.
            :properties:
                | compiler - Injected IScaraCompiler service port.
                | decompiler - Injected IScaraDecompiler service port.
                | diagnostics - SCARA DSL diagnostic and error handling services bundle.
    '''

    parent: Widget
    editor: IDslCodeEditor
    console: IDslConsoleView
    dsl: DslPipelineBundle
    loader: IPlanLoader
    storer: IPlanStorer

    @property
    def compiler(self) -> IScaraCompiler:
        '''
            Returns compiler port from DSL pipeline.

            :return: IScaraCompiler instance.
        '''
        return self.dsl.compiler

    @property
    def decompiler(self) -> IScaraDecompiler:
        '''
            Returns decompiler port from DSL pipeline.

            :return: IScaraDecompiler instance.
        '''
        return self.dsl.decompiler

    @property
    def diagnostics(self) -> DslDiagnosticBundle:
        '''
            Returns diagnostics bundle from DSL pipeline.

            :return: DslDiagnosticBundle instance.
        '''
        return self.dsl.diagnostics
