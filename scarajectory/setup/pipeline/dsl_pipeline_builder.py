# -*- coding: UTF-8 -*-

'''
Module
    dsl_pipeline_builder.py
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

from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.compiler.plan.itrajectory_plan_compiler import ITrajectoryPlanCompiler
from scaralang.core.service.compiler.plan.scara_plan_compiler_factory import ScaraPlanCompilerFactory
from scaralang.core.service.compiler.plan.trajectory_plan_compiler_factory import TrajectoryPlanCompilerFactory
from scaralang.core.service.compiler.scara_compiler_factory import ScaraCompilerFactory
from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scaralang.core.service.decompiler.scara_decompiler_factory import ScaraDecompilerFactory
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.exporter.scara.scara_plan_exporter_factory import ScaraPlanExporterFactory
from scaralang.core.service.linter.diagnostic.scara_diagnostic_formatter_factory import ScaraDiagnosticFormatterFactory
from scaralang.core.service.linter.iscara_linter import IScaraLinter
from scaralang.core.service.linter.scara_linter_factory import ScaraLinterFactory
from scaralang.core.service.linter.script.iscara_dsl_validator import IScaraDslValidator
from scaralang.core.service.linter.script.scara_script_validator_factory import ScaraScriptValidatorFactory
from scaralang.core.service.parser.iscara_parser import IScaraParser
from scaralang.core.service.parser.lexer.scara_lexer_factory import ScaraLexerFactory
from scaralang.core.service.parser.scara_parser_factory import ScaraParserFactory
from scaralang.infrastructure.command.compile.error.compile_error_handler_factory import CompileErrorHandlerFactory
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scaralang.infrastructure.command.decompile.error.decompile_error_handler_factory import DecompileErrorHandlerFactory
from scaralang.infrastructure.command.export.error.export_error_handler_factory import ExportErrorHandlerFactory
from scaralang.infrastructure.command.lint.error.lint_error_handler_factory import LintErrorHandlerFactory
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
        parser: IScaraParser = ScaraParserFactory.create(
            lexer=ScaraLexerFactory.create()
        )
        compiler: ITrajectoryPlanCompiler = (
            TrajectoryPlanCompilerFactory.create(validator=validator)
        )
        linter: IScaraLinter = ScaraLinterFactory.create()

        plan_compiler: IScaraPlanCompiler = ScaraPlanCompilerFactory.create(
            parser=parser,
            compiler=compiler,
            linter=linter,
        )
        dsl_validator: IScaraDslValidator = (
            ScaraScriptValidatorFactory.create(
                parser=parser,
                compiler=compiler,
                linter=linter,
            )
        )
        plan_exporter: IScaraPlanExporter = ScaraPlanExporterFactory.create()

        wire_compiler: IScaraCompiler = (
            ScaraCompilerFactory.create_default()
        )
        decompiler: IScaraDecompiler = (
            ScaraDecompilerFactory.create_default()
        )
        diagnostics = DslDiagnosticBundle(
            compile_error_handler=CompileErrorHandlerFactory.create(),
            lint_error_handler=LintErrorHandlerFactory.create(),
            decompile_error_handler=DecompileErrorHandlerFactory.create(),
            export_error_handler=ExportErrorHandlerFactory.create(),
            diagnostic_formatter=ScaraDiagnosticFormatterFactory.create(),
        )

        return DslPipelineBundle(
            compiler=wire_compiler,
            decompiler=decompiler,
            plan_compiler=plan_compiler,
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
