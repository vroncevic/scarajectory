# -*- coding: UTF-8 -*-

'''
Module
    dsl_diagnostic_bundle.py
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
    Bundle containing fine-grained SCARA DSL diagnostic and error handling services.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.linter.diagnostic.iscara_diagnostic_formatter import IScaraDiagnosticFormatter
from scaralang.infrastructure.command.compile.error.icompile_error_handler import ICompileErrorHandler
from scaralang.infrastructure.command.decompile.error.idecompile_error_handler import IDecompileErrorHandler
from scaralang.infrastructure.command.export.error.iexport_error_handler import IExportErrorHandler
from scaralang.infrastructure.command.lint.error.ilint_error_handler import ILintErrorHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class DslDiagnosticBundle:
    '''
        Bundle containing fine-grained SCARA DSL diagnostic and error handling services.

        It defines:

            :attributes:
                | compile_error_handler - Compile error formatting and exit code resolution handler.
                | lint_error_handler - Lint error formatting and exit code resolution handler.
                | decompile_error_handler - Decompile error formatting and exit code resolution handler.
                | export_error_handler - Export error formatting and exit code resolution handler.
                | diagnostic_formatter - Linter diagnostic report formatter service.
            :methods: None.
    '''

    compile_error_handler: ICompileErrorHandler
    lint_error_handler: ILintErrorHandler
    decompile_error_handler: IDecompileErrorHandler
    export_error_handler: IExportErrorHandler
    diagnostic_formatter: IScaraDiagnosticFormatter
