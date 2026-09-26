# -*- coding: UTF-8 -*-

'''
Module
    timing_lint_rule.py
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
    Validates dwell timing delays and pause compatibility with continuous blend zones.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.diagnostic.diagnostic import Diagnostic
from scarajectory.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity
from scarajectory.core.service.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TimingLintRule:
    '''
        Lint rule checking for non-positive dwell delays and dwell pauses during active blend zones.

        It defines:

            :methods:
                | check - Evaluates WAIT_MS instruction against dwell parameters and blend mode.
    '''

    def check(
        self,
        *,
        instruction: Instruction,
        context: ScaraLintContext,
        diagnostics: list[Diagnostic],
    ) -> None:
        '''
            Evaluates WAIT_MS instructions, reporting non-positive delays and blend flyby conflicts.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :param diagnostics: Accumulator list of diagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type != CommandType.WAIT_MS:
            return

        line = instruction.line_number
        params = instruction.parameters
        delay_ms: float = float(params.get('ms', 0.0))

        if delay_ms <= 0.0:
            diagnostics.append(
                Diagnostic(
                    code='DEAD_WAIT',
                    severity=DiagnosticSeverity.INFO,
                    message=(
                        f'Dwell delay WAIT_MS {delay_ms:.0f} is '
                        f'non-positive and produces no pause.'
                    ),
                    line=line,
                    command='WAIT_MS',
                )
            )

        if context.zone_mode != 'FINE' and context.zone_radius > 0.0:
            diagnostics.append(
                Diagnostic(
                    code='TOOL_IN_FLYBY',
                    severity=DiagnosticSeverity.WARNING,
                    message='Dwell pause WAIT_MS issued during active continuous blend zone.',
                    line=line,
                    command='WAIT_MS',
                )
            )

        context.last_coords = ()
