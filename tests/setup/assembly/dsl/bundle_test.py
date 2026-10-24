# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for DslPipelineBundle container model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.icompiler import IScaraCompiler
from scaralang.core.service.compiler.plan.script.icompiler import IScriptPlanCompiler
from scaralang.core.service.decompiler.idecompiler import IScaraDecompiler
from scaralang.core.service.exporter.scara.iexporter import IScaraPlanExporter
from scaralang.core.service.linter.validator.ivalidator import IScriptValidator
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


class DslPipelineBundleTest(TestCase):
    '''
        Unit testing suite for DslPipelineBundle.

        It defines:

            :methods:
                | test_bundle_creation - Tests creating bundle with mock components.
                | test_bundle_immutability - Verifies frozen immutability of bundle.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies valid creation and attribute access.

            :exceptions: None.
        '''
        compiler = MagicMock(spec=IScaraCompiler)
        decompiler = MagicMock(spec=IScaraDecompiler)
        plan_compiler = MagicMock(spec=IScriptPlanCompiler)
        plan_exporter = MagicMock(spec=IScaraPlanExporter)
        validator = MagicMock(spec=IScriptValidator)
        diagnostics = MagicMock(spec=DslDiagnosticBundle)

        bundle = DslPipelineBundle(
            compiler=compiler,
            decompiler=decompiler,
            plan_compiler=plan_compiler,
            plan_exporter=plan_exporter,
            validator=validator,
            diagnostics=diagnostics,
        )
        self.assertIs(bundle.compiler, compiler)
        self.assertIs(bundle.decompiler, decompiler)
        self.assertIs(bundle.plan_compiler, plan_compiler)
        self.assertIs(bundle.plan_exporter, plan_exporter)
        self.assertIs(bundle.validator, validator)
        self.assertIs(bundle.diagnostics, diagnostics)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies that DslPipelineBundle is frozen and immutable.

            :exceptions: None.
        '''
        compiler = MagicMock(spec=IScaraCompiler)
        decompiler = MagicMock(spec=IScaraDecompiler)
        plan_compiler = MagicMock(spec=IScriptPlanCompiler)
        plan_exporter = MagicMock(spec=IScaraPlanExporter)
        validator = MagicMock(spec=IScriptValidator)
        diagnostics = MagicMock(spec=DslDiagnosticBundle)

        bundle = DslPipelineBundle(
            compiler=compiler,
            decompiler=decompiler,
            plan_compiler=plan_compiler,
            plan_exporter=plan_exporter,
            validator=validator,
            diagnostics=diagnostics,
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.compiler = MagicMock(spec=IScaraCompiler)  # type: ignore[misc]


if __name__ == '__main__':
    main()
