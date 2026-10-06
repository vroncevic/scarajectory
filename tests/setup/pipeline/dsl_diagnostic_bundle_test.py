# -*- coding: UTF-8 -*-

'''
Module
    dsl_diagnostic_bundle_test.py
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
    Unit tests for DslDiagnosticBundle container model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.linter.diagnostic.iscara_diagnostic_formatter import IScaraDiagnosticFormatter
from scaralang.infrastructure.command.compile.error.icompile_error_handler import ICompileErrorHandler
from scaralang.infrastructure.command.decompile.error.idecompile_error_handler import IDecompileErrorHandler
from scaralang.infrastructure.command.export.error.iexport_error_handler import IExportErrorHandler
from scaralang.infrastructure.command.lint.error.ilint_error_handler import ILintErrorHandler
from scarajectory.setup.pipeline.dsl_diagnostic_bundle import DslDiagnosticBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslDiagnosticBundleTestCase(TestCase):
    '''Unit testing suite for DslDiagnosticBundle.'''

    def test_bundle_creation(self) -> None:
        '''Verifies valid creation and attribute access.'''
        compile_handler = MagicMock(spec=ICompileErrorHandler)
        lint_handler = MagicMock(spec=ILintErrorHandler)
        decompile_handler = MagicMock(spec=IDecompileErrorHandler)
        export_handler = MagicMock(spec=IExportErrorHandler)
        formatter = MagicMock(spec=IScaraDiagnosticFormatter)

        bundle = DslDiagnosticBundle(
            compile_error_handler=compile_handler,
            lint_error_handler=lint_handler,
            decompile_error_handler=decompile_handler,
            export_error_handler=export_handler,
            diagnostic_formatter=formatter,
        )
        self.assertIs(bundle.compile_error_handler, compile_handler)
        self.assertIs(bundle.lint_error_handler, lint_handler)
        self.assertIs(bundle.decompile_error_handler, decompile_handler)
        self.assertIs(bundle.export_error_handler, export_handler)
        self.assertIs(bundle.diagnostic_formatter, formatter)

    def test_bundle_immutability(self) -> None:
        '''Verifies that DslDiagnosticBundle is frozen and immutable.'''
        compile_handler = MagicMock(spec=ICompileErrorHandler)
        lint_handler = MagicMock(spec=ILintErrorHandler)
        decompile_handler = MagicMock(spec=IDecompileErrorHandler)
        export_handler = MagicMock(spec=IExportErrorHandler)
        formatter = MagicMock(spec=IScaraDiagnosticFormatter)

        bundle = DslDiagnosticBundle(
            compile_error_handler=compile_handler,
            lint_error_handler=lint_handler,
            decompile_error_handler=decompile_handler,
            export_error_handler=export_handler,
            diagnostic_formatter=formatter,
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.compile_error_handler = MagicMock(spec=ICompileErrorHandler)  # type: ignore


if __name__ == '__main__':
    main()
