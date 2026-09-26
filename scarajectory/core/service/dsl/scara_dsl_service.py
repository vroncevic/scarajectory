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
    High-level facade orchestrating SCARA DSL compilation, validation, linting, and binary framing.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.binary.program import Program
from scarajectory.core.model.dsl.diagnostic.diagnostic import Diagnostic
from scarajectory.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity
from scarajectory.core.service.dsl.diagnostic.scara_diagnostic_formatter import ScaraDiagnosticFormatter
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.dsl.binary.icompiler import ICompiler
from scarajectory.core.service.dsl.compiler.iscara_compiler import IScaraCompiler
from scarajectory.core.service.dsl.exporter.iscara_plan_exporter import IScaraPlanExporter
from scarajectory.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.parser.iscara_parser import IScaraParser

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
        High-level facade orchestrating SCARA DSL compilation, validation and binary serialization.

        It defines:

            :attributes:
                | _lexer - Dedicated lexical tokenizer protocol.
                | _parser - AST grammar parser orchestrator protocol.
                | _compiler - Macro expander and validator protocol.
                | _exporter - TrajectoryPlan to .scara code serializer protocol.
                | _binary_compiler - TrajectoryPlan to binary frame compiler protocol.
            :methods:
                | __init__ - Initializes DSL facade with injected component protocols.
                | compile_script - Compiles DSL source code into executable TrajectoryPlan.
                | validate_script - Checks syntax, static analysis rules, and kinematics of DSL script.
                | lint_script - Performs static analysis checks on DSL script string.
                | export_plan - Serializes active TrajectoryPlan to DSL source text.
                | compile_plan - Compiles TrajectoryPlan into Program package.
                | compile_to_bytes - Compiles DSL code directly to raw UART wire byte stream.
                | compile_to_binary - Compiles DSL source text into Program package.
    '''

    _lexer: IScaraLexer
    _parser: IScaraParser
    _compiler: IScaraCompiler
    _exporter: IScaraPlanExporter
    _binary_compiler: ICompiler

    def __init__(
        self,
        *,
        lexer: IScaraLexer,
        parser: IScaraParser,
        compiler: IScaraCompiler,
        exporter: IScaraPlanExporter,
        binary_compiler: ICompiler
    ) -> None:
        '''
            Initializes ScaraDslService with injected component protocols.

            :param lexer: Injected IScaraLexer protocol instance.
            :param parser: Injected IScaraParser protocol instance.
            :param compiler: Injected IScaraCompiler protocol instance.
            :param exporter: Injected IScaraPlanExporter protocol instance.
            :param binary_compiler: Injected ICompiler protocol instance.
            :exceptions: None.
        '''
        self._lexer = lexer
        self._parser = parser
        self._compiler = compiler
        self._exporter = exporter
        self._binary_compiler = binary_compiler

    def compile_script(self, *, source: str) -> TrajectoryPlan:
        '''
            Compiles DSL source code into an executable and validated TrajectoryPlan.

            :param source: Raw .scara script text.
            :return: Validated TrajectoryPlan instance.
            :exceptions: ValueError if syntax or static analysis errors occur.
        '''
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse_tokens(tokens=tokens)

        return self._compiler.compile(program=program)

    def validate_script(self, *, source: str) -> tuple[bool, list[str]]:
        '''
            Checks syntax, static analysis rules, and kinematics of a DSL script.

            :param source: Raw .scara script text.
            :return: Tuple of (is_valid boolean, list of error message strings).
            :exceptions: None.
        '''
        messages: list[str] = []

        try:
            tokens = self._lexer.tokenize(source=source)
            program = self._parser.parse_tokens(tokens=tokens)
            diagnostics = self._compiler.lint(program=program)

            for diag in diagnostics:
                messages.append(
                    ScaraDiagnosticFormatter.format_report(diagnostic=diag)
                )

            has_errors: bool = any(
                d.severity == DiagnosticSeverity.ERROR
                for d in diagnostics
            )

            if has_errors:
                return False, messages

            plan = self._compiler.compile(program=program)
            messages.append(
                f'✅ Validation PASSED: {len(program.instructions)} instructions, {plan.count} waypoints generated.'
            )

            return True, messages

        except Exception as exc:
            messages.append(f'❌ Validation failed: {exc}')
            return False, messages

    def lint_script(self, *, source: str) -> tuple[Diagnostic, ...]:
        '''
            Performs static analysis checks on a DSL script string.

            :param source: Raw .scara script text.
            :return: Tuple of Diagnostic findings.
            :exceptions: None.
        '''
        try:
            tokens = self._lexer.tokenize(source=source)
            program = self._parser.parse_tokens(tokens=tokens)
            return self._compiler.lint(program=program)
        except Exception as exc:
            return (
                Diagnostic(
                    code='SYNTAX_ERROR',
                    severity=DiagnosticSeverity.ERROR,
                    message=str(exc),
                    line=1,
                    command=''
                ),
            )

    def export_plan(self, *, plan: ITrajectoryReadOnly) -> str:
        '''
            Serializes active TrajectoryPlan into formatted .scara DSL source text.

            :param plan: Read-only trajectory plan instance to serialize.
            :return: Formatted SCARA DSL script.
            :exceptions: None.
        '''
        return self._exporter.export_plan(plan=plan)

    def compile_plan(self, *, plan: TrajectoryPlan) -> Program:
        '''
            Compiles TrajectoryPlan into Program package.

            :param plan: TrajectoryPlan instance.
            :return: Program instance.
            :exceptions: None.
        '''
        return self._binary_compiler.compile_plan(plan=plan)

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL code directly to raw UART wire byte stream.

            :param source: Raw .scara DSL source text.
            :return: Serialized wire byte stream.
            :exceptions: None.
        '''
        return self._binary_compiler.compile_to_bytes(source=source)

    def compile_to_binary(self, *, source: str) -> Program:
        '''
            Compiles DSL source text into Program package.

            :param source: Raw .scara DSL source text.
            :return: Program instance.
            :exceptions: None.
        '''
        return self._binary_compiler.compile_script(source=source)
