# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_lint_rule.py
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
    Validates vacuum pump and blow-off valve state consistency, contention, and flyby safety.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.ast.scara_command_type import ScaraCommandType
from scarajectory.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scarajectory.core.model.dsl.diagnostic.scara_diagnostic_severity import (
    ScaraDiagnosticSeverity,
)
from scarajectory.core.service.dsl.linter.scara_lint_context import (
    ScaraLintContext,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PneumaticLintRule:
    '''
        Lint rule checking pneumatic pump/valve contention, redundant states, and zone blend violations.

        It defines:

            :methods:
                | check - Evaluates tool instruction against pneumatic state and blend configuration.
    '''

    def check(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraLintContext,
        diagnostics: list[ScaraDiagnostic],
    ) -> None:
        '''
            Evaluates pneumatic instructions, appending findings and updating context.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :param diagnostics: Accumulator list of diagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type
        if cmd not in (ScaraCommandType.PUMP, ScaraCommandType.VALVE):
            return

        line = instruction.line_number
        params = instruction.parameters
        is_pump = cmd == ScaraCommandType.PUMP
        target_state = str(params.get('state', 'OFF')).upper() == 'ON'

        if context.zone_mode != 'FINE' and context.zone_radius > 0.0:
            diagnostics.append(
                ScaraDiagnostic(
                    code='TOOL_IN_FLYBY',
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=(
                        f'Tool action {cmd.value} issued during '
                        f'active continuous blend zone.'
                    ),
                    line=line,
                    command=cmd.value,
                )
            )

        if is_pump:
            if target_state and context.pump_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='REDUNDANT_TOOL_CMD',
                        severity=ScaraDiagnosticSeverity.WARNING,
                        message='PUMP is already ON. Redundant actuation command.',
                        line=line,
                        command='PUMP',
                    )
                )
            elif not target_state and not context.pump_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='REDUNDANT_TOOL_CMD',
                        severity=ScaraDiagnosticSeverity.WARNING,
                        message='PUMP is already OFF. Redundant actuation command.',
                        line=line,
                        command='PUMP',
                    )
                )
            if target_state and context.valve_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='PNEUMATIC_CONFLICT',
                        severity=ScaraDiagnosticSeverity.ERROR,
                        message=(
                            'Cannot turn PUMP ON while blow-off VALVE is active. '
                            'Pneumatic contention detected.'
                        ),
                        line=line,
                        command='PUMP',
                    )
                )
            context.pump_on = target_state
        else:
            if target_state and context.valve_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='REDUNDANT_TOOL_CMD',
                        severity=ScaraDiagnosticSeverity.WARNING,
                        message='VALVE is already ON. Redundant actuation command.',
                        line=line,
                        command='VALVE',
                    )
                )
            elif not target_state and not context.valve_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='REDUNDANT_TOOL_CMD',
                        severity=ScaraDiagnosticSeverity.WARNING,
                        message='VALVE is already OFF. Redundant actuation command.',
                        line=line,
                        command='VALVE',
                    )
                )
            if target_state and context.pump_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='PNEUMATIC_CONFLICT',
                        severity=ScaraDiagnosticSeverity.ERROR,
                        message=(
                            'Cannot turn blow-off VALVE ON while vacuum PUMP is active. '
                            'Pneumatic contention detected.'
                        ),
                        line=line,
                        command='VALVE',
                    )
                )
            context.valve_on = target_state

        context.last_coords = None
