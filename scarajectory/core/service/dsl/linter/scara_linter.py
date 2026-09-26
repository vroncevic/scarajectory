# -*- coding: UTF-8 -*-

'''
Module
    scara_linter.py
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
    Static analysis and diagnostic linter verifying safety, sequencing, and coherence in SCARA DSL programs.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.model.dsl.ast.program import Program
from scarajectory.core.model.dsl.diagnostic.diagnostic import Diagnostic
from scarajectory.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity
from scarajectory.core.service.dsl.linter.rules.iscara_lint_rule import IScaraLintRule
from scarajectory.core.service.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraLinter:
    '''
        Static analyzer orchestrating rule evaluations across SCARA DSL AST programs.

        It defines:

            :attributes:
                | _rules - Sequence of registered IScaraLintRule components.
            :methods:
                | __init__ - Initializes ScaraLinter with injected lint rules.
                | lint - Performs static analysis and returns tuple of Diagnostic findings.
    '''

    def __init__(self, *, rules: Sequence[IScaraLintRule]) -> None:
        '''
            Initializes ScaraLinter with injected lint rules.

            :param rules: Sequence of IScaraLintRule components.
            :exceptions: None.
        '''
        self._rules: tuple[IScaraLintRule, ...] = tuple(rules)

    def lint(self, *, program: Program) -> tuple[Diagnostic, ...]:
        '''
            Performs static analysis checks on a SCARA DSL AST program.

            :param program: Parsed Program AST root.
            :return: Tuple of Diagnostic findings.
            :exceptions: None.
        '''
        diagnostics: list[Diagnostic] = []
        instructions = program.instructions

        if not instructions:
            diagnostics.append(
                Diagnostic(
                    code='EMPTY_PROGRAM',
                    severity=DiagnosticSeverity.ERROR,
                    message='Program contains no executable instructions.',
                    line=1,
                    command='',
                )
            )

            return tuple(diagnostics)

        context = ScaraLintContext()

        for inst in instructions:
            for rule in self._rules:
                rule.check(
                    instruction=inst,
                    context=context,
                    diagnostics=diagnostics,
                )

        return tuple(diagnostics)
