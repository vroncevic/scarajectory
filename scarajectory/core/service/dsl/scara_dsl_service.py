# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_service.py
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
    Implementation of IScaraDslService coordinating lexing, parsing, compiling and exporting.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.scara_diagnostic import ScaraDiagnostic
from scarajectory.core.model.dsl.scara_diagnostic_severity import (
    ScaraDiagnosticSeverity,
)
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.dsl.iscara_compiler import IScaraCompiler
from scarajectory.core.service.dsl.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.iscara_parser import IScaraParser
from scarajectory.core.service.dsl.iscara_plan_exporter import IScaraPlanExporter
from scarajectory.core.service.dsl.scara_compiler import ScaraCompiler
from scarajectory.core.service.dsl.scara_lexer import ScaraLexer
from scarajectory.core.service.dsl.scara_parser import ScaraParser
from scarajectory.core.service.dsl.scara_plan_exporter import ScaraPlanExporter
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.trajectory_validator import TrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDslService:
    '''
        High-level facade orchestrating SCARA DSL compilation, validation and serialization.

        It defines:

            :attributes:
                | _lexer - Dedicated lexical tokenizer.
                | _parser - AST grammar parser orchestrator.
                | _compiler - Macro expander, arc interpolator and validator.
                | _exporter - TrajectoryPlan to .scara code serializer.
            :methods:
                | __init__ - Initializes DSL facade with injected or default components.
                | compile_script - Compiles DSL source code into executable TrajectoryPlan.
                | validate_script - Checks syntax, static analysis rules, and kinematics of DSL script.
                | lint_script - Performs static analysis checks on DSL script string.
                | export_plan - Serializes active TrajectoryPlan to DSL source text.
    '''

    def __init__(
        self,
        *,
        lexer: IScaraLexer | None = None,
        parser: IScaraParser | None = None,
        compiler: IScaraCompiler | None = None,
        exporter: IScaraPlanExporter | None = None,
        validator: ITrajectoryValidator | None = None,
    ) -> None:
        '''
            Initializes ScaraDslService with optional injected dependencies.

            :param lexer: Optional IScaraLexer instance.
            :param parser: Optional IScaraParser instance.
            :param compiler: Optional IScaraCompiler instance.
            :param exporter: Optional IScaraPlanExporter instance.
            :param validator: Optional ITrajectoryValidator instance.
            :exceptions: None.
        '''
        self._lexer: IScaraLexer = lexer if lexer is not None else ScaraLexer()
        self._parser: IScaraParser = (
            parser if parser is not None else ScaraParser()
        )
        active_validator = (
            validator if validator is not None else TrajectoryValidator()
        )
        self._compiler: IScaraCompiler = (
            compiler
            if compiler is not None
            else ScaraCompiler(validator=active_validator)
        )
        self._exporter: IScaraPlanExporter = (
            exporter if exporter is not None else ScaraPlanExporter()
        )

    def compile_script(
        self,
        *,
        source: str,
        bounds: ScaraBounds | None = None,
    ) -> TrajectoryPlan:
        '''
            Compiles DSL source code into an executable and validated TrajectoryPlan.

            :param source: Raw .scara script text.
            :param bounds: Optional robot kinematic boundary constraints.
            :return: Validated TrajectoryPlan instance.
            :exceptions: ValueError if parsing or kinematic validation fails.
        '''
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse_tokens(tokens=tokens)
        return self._compiler.compile(program=program, bounds=bounds)

    def validate_script(
        self,
        *,
        source: str,
        bounds: ScaraBounds | None = None,
    ) -> tuple[bool, list[str]]:
        '''
            Validates syntax, static analysis rules, and kinematics of a DSL script.

            :param source: Raw .scara script text.
            :param bounds: Optional robot kinematic boundary constraints.
            :return: Tuple of (is_valid, messages_list).
            :exceptions: None.
        '''
        messages: list[str] = []
        try:
            tokens = self._lexer.tokenize(source=source)
            program = self._parser.parse_tokens(tokens=tokens)
            diagnostics = self._compiler.lint(program=program)

            for diag in diagnostics:
                messages.append(diag.format_report())

            has_errors: bool = any(
                d.severity == ScaraDiagnosticSeverity.ERROR
                for d in diagnostics
            )
            if has_errors:
                return False, messages

            plan = self._compiler.compile(program=program, bounds=bounds)
            messages.append(
                f'✅ Validation PASSED: {len(program.instructions)} instructions, {plan.count} waypoints generated.'
            )
            return True, messages
        except Exception as exc:
            messages.append(f'❌ Validation failed: {exc}')
            return False, messages

    def lint_script(
        self,
        *,
        source: str,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a DSL script string.

            :param source: Raw .scara script text.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
        try:
            tokens = self._lexer.tokenize(source=source)
            program = self._parser.parse_tokens(tokens=tokens)
            return self._compiler.lint(program=program)
        except Exception as exc:
            return (
                ScaraDiagnostic(
                    code='SYNTAX_ERROR',
                    severity=ScaraDiagnosticSeverity.ERROR,
                    message=str(exc),
                    line=1,
                    command='',
                ),
            )

    def export_plan(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes active TrajectoryPlan into formatted .scara DSL source text.

            :param plan: TrajectoryPlan instance to serialize.
            :return: Formatted SCARA DSL script.
            :exceptions: None.
        '''
        return self._exporter.export_plan(plan=plan)
