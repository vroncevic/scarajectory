# -*- coding: UTF-8 -*-

'''
Module
    assembler.py
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
    Builder assembling fine-grained DSL role services into DslPipelineBundle.
'''

from __future__ import annotations

from scaralang.core.service.compiler.icompiler import IScaraCompiler
from scaralang.core.service.compiler.plan.dependencies import PlanDependencies
from scaralang.core.service.compiler.plan.factory import PlanFactory
from scaralang.infrastructure.compiler.factory import DefaultCompilerFactory
from scaralang.core.service.decompiler.idecompiler import IScaraDecompiler
from scaralang.infrastructure.decompiler.factory import DefaultDecompilerFactory
from scaralang.core.service.exporter.scara.factory import ScaraPlanExporterFactory
from scaralang.core.service.exporter.scara.iexporter import IScaraPlanExporter
from scaralang.core.service.linter.diagnostic.factory import DiagnosticFactory
from scaralang.core.service.linter.factory import LinterFactory
from scaralang.core.service.linter.ilinter import ILinter
from scaralang.core.service.linter.validator.dependencies import ValidatorDependencies
from scaralang.core.service.linter.validator.factory import ValidatorFactory
from scaralang.core.service.linter.validator.ivalidator import IScriptValidator
from scaralang.core.service.parser.iparser import IScaraParser
from scaralang.infrastructure.parser.factory import DefaultParserFactory
from scaralang.infrastructure.command.compile.error.factory import ErrorFactory as CompileErrorFactory
from scaralang.infrastructure.command.decompile.error.factory import ErrorFactory as DecompileErrorFactory
from scaralang.infrastructure.command.export.error.factory import ErrorFactory as ExportErrorFactory
from scaralang.infrastructure.command.lint.error.factory import ErrorFactory as LintErrorFactory

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
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


class DslPipelineBuilder:
    '''
        Builder assembling fine-grained DSL role services into DslPipelineBundle.

        It defines:

            :methods:
                | build - Assembles DSL compiler, validator, and exporter services.
                | get_version - Returns builder version string.
    '''

    @classmethod
    def build(
        cls,
        *,
        validator: ITrajectoryValidator,
    ) -> DslPipelineBundle:
        '''
            Assembles parser, compiler, linter, validator and exporter services.

            :param validator: Injected ITrajectoryValidator instance.
            :return: Fully assembled DslPipelineBundle instance.
            :exceptions: None.
        '''
        parser: IScaraParser = DefaultParserFactory.create().parser
        linter: ILinter = LinterFactory.create().linter

        plan_subsystem = PlanFactory.create(
            dependencies=PlanDependencies(
                validator=validator,
                parser=parser,
                linter=linter,
            )
        )
        dsl_validator: IScriptValidator = (
            ValidatorFactory.create(
                dependencies=ValidatorDependencies(
                    parser=parser,
                    compiler=plan_subsystem.ast_compiler,
                    linter=linter,
                )
            ).validator
        )
        plan_exporter: IScaraPlanExporter = ScaraPlanExporterFactory.create()

        wire_compiler: IScaraCompiler = DefaultCompilerFactory.create()
        decompiler: IScaraDecompiler = DefaultDecompilerFactory.create()
        diagnostics = DslDiagnosticBundle(
            compile_error_handler=CompileErrorFactory.create().handler,
            lint_error_handler=LintErrorFactory.create().handler,
            decompile_error_handler=DecompileErrorFactory.create().handler,
            export_error_handler=ExportErrorFactory.create().handler,
            diagnostic_formatter=DiagnosticFactory.create().formatter,
        )

        return DslPipelineBundle(
            compiler=wire_compiler,
            decompiler=decompiler,
            plan_compiler=plan_subsystem.script_compiler,
            plan_exporter=plan_exporter,
            validator=dsl_validator,
            diagnostics=diagnostics,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the builder version string representation.

            :return: Builder version string.
            :exceptions: None.
        '''
        return __version__
