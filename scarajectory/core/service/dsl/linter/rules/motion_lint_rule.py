# -*- coding: UTF-8 -*-

'''
Module
    motion_lint_rule.py
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
    Validates calibration prerequisites and duplicate moves for motion instructions.
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


class MotionLintRule:
    '''
        Lint rule checking for uncalibrated moves and consecutive duplicate targets.

        It defines:

            :attributes:
                | _MOTION_COMMANDS - Frozenset of instructions representing robot motion.
            :methods:
                | check - Analyzes motion instruction against current simulation context.
    '''

    _MOTION_COMMANDS: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.MOVE_L,
        ScaraCommandType.MOVE_J,
        ScaraCommandType.ARC_CW,
        ScaraCommandType.ARC_CCW,
        ScaraCommandType.JUMP,
        ScaraCommandType.APPROACH,
        ScaraCommandType.RETRACT,
        ScaraCommandType.MOVE_PALLET,
    })

    def check(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraLintContext,
        diagnostics: list[ScaraDiagnostic],
    ) -> None:
        '''
            Evaluates motion calibration and duplicate move findings.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :param diagnostics: Accumulator list of diagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type
        if cmd not in self._MOTION_COMMANDS:
            return

        line = instruction.line_number
        params = instruction.parameters

        if not context.is_homed and not context.motion_occurred:
            diagnostics.append(
                ScaraDiagnostic(
                    code='UNCALIBRATED_MOTION',
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=(
                        'First motion instruction occurs before HOME or '
                        'SETPOS calibration. Machine coordinates unreferenced.'
                    ),
                    line=line,
                    command=cmd.value,
                )
            )

        if cmd in (ScaraCommandType.MOVE_L, ScaraCommandType.MOVE_J):
            x_val = params.get('X', params.get('x'))
            y_val = params.get('Y', params.get('y'))
            z_val = params.get('Z', params.get('z'))
            phi_val = params.get('PHI', params.get('phi', 0.0))
            if x_val is not None and y_val is not None and z_val is not None:
                coords = (
                    float(x_val),
                    float(y_val),
                    float(z_val),
                    float(phi_val),
                )
                if context.last_coords is not None and coords == context.last_coords:
                    diagnostics.append(
                        ScaraDiagnostic(
                            code='DUPLICATE_MOTION',
                            severity=ScaraDiagnosticSeverity.INFO,
                            message=(
                                f'Consecutive move to identical target coordinates '
                                f'({coords[0]:.1f}, {coords[1]:.1f}, {coords[2]:.1f}, {coords[3]:.1f}).'
                            ),
                            line=line,
                            command=cmd.value,
                        )
                    )
                context.last_coords = coords
            else:
                context.last_coords = None
        else:
            context.last_coords = None

        context.motion_occurred = True
