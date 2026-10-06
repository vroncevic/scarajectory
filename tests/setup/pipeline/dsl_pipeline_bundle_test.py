# -*- coding: UTF-8 -*-

'''
Module
    dsl_pipeline_bundle_test.py
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

from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.linter.script.iscara_dsl_validator import IScaraDslValidator
from scarajectory.setup.pipeline.dsl_diagnostic_bundle import DslDiagnosticBundle
from scarajectory.setup.pipeline.dsl_pipeline_bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslPipelineBundleTestCase(TestCase):
    '''Unit testing suite for DslPipelineBundle.'''

    def test_bundle_creation(self) -> None:
        '''Verifies valid creation and attribute access.'''
        compiler = MagicMock(spec=IScaraCompiler)
        decompiler = MagicMock(spec=IScaraDecompiler)
        plan_compiler = MagicMock(spec=IScaraPlanCompiler)
        plan_exporter = MagicMock(spec=IScaraPlanExporter)
        validator = MagicMock(spec=IScaraDslValidator)
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
        '''Verifies that DslPipelineBundle is frozen and immutable.'''
        compiler = MagicMock(spec=IScaraCompiler)
        decompiler = MagicMock(spec=IScaraDecompiler)
        plan_compiler = MagicMock(spec=IScaraPlanCompiler)
        plan_exporter = MagicMock(spec=IScaraPlanExporter)
        validator = MagicMock(spec=IScaraDslValidator)
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
            bundle.compiler = MagicMock(spec=IScaraCompiler)  # type: ignore


if __name__ == '__main__':
    main()
