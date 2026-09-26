# -*- coding: UTF-8 -*-

'''
Module
    state_lint_rule.py
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
    Tracks homing state and blend zone configurations during DSL static analysis.
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


class StateLintRule:
    '''
        Lint rule updating simulation state context on HOME and ZONE configuration instructions.

        It defines:

            :methods:
                | check - Updates context state for homing and zone mode/radius.
    '''

    def check(
        self,
        *,
        instruction: Instruction,
        context: ScaraLintContext,
        diagnostics: list[Diagnostic],
    ) -> None:
        '''
            Evaluates homing and zone configuration instructions, updating context.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :param diagnostics: Accumulator list of diagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type
        params = instruction.parameters

        match cmd:
            case CommandType.HOME:
                context.is_homed = True
                context.last_coords = ()
            case CommandType.ZONE:
                raw_mode = str(params.get('mode', 'FINE')).upper()
                radius = float(params.get('radius', 0.0))
                if raw_mode not in ('FINE', 'BLEND'):
                    diagnostics.append(
                        Diagnostic(
                            code='INVALID_ZONE_MODE',
                            severity=DiagnosticSeverity.WARNING,
                            message=(
                                f"Unknown zone mode '{raw_mode}'. "
                                "Expected 'FINE' or 'BLEND'."
                            ),
                            line=instruction.line_number,
                            command='ZONE',
                        )
                    )
                if radius < 0.0:
                    diagnostics.append(
                        Diagnostic(
                            code='INVALID_ZONE_RADIUS',
                            severity=DiagnosticSeverity.WARNING,
                            message=(
                                f'Zone radius {radius:.1f} is negative. '
                                'Expected non-negative radius.'
                            ),
                            line=instruction.line_number,
                            command='ZONE',
                        )
                    )
                context.zone_mode = raw_mode
                context.zone_radius = radius
            case _:
                pass
