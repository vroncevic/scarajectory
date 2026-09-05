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

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.iscara_program import IScaraProgram
from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType
from scarajectory.core.model.dsl.scara_diagnostic import ScaraDiagnostic
from scarajectory.core.model.dsl.scara_diagnostic_severity import (
    ScaraDiagnosticSeverity,
)

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
        Static analyzer checking SCARA DSL AST programs for safety risks and sequencing issues.

        It defines:

            :attributes:
                | None.
            :methods:
                | __init__ - Initializes ScaraLinter instance.
                | lint - Performs static analysis and returns tuple of ScaraDiagnostic findings.
                | _check_pneumatics - Evaluates vacuum pump and blow-off valve state consistency.
                | _check_motion - Evaluates calibration prerequisites and duplicate trajectory moves.
    '''

    def __init__(self) -> None:
        '''
            Initializes ScaraLinter instance.

            :exceptions: None.
        '''
        pass

    def lint(
        self,
        *,
        program: IScaraProgram,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a SCARA DSL AST program.

            :param program: Parsed IScaraProgram AST root.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
        diagnostics: list[ScaraDiagnostic] = []
        instructions = program.instructions

        if not instructions:
            diagnostics.append(
                ScaraDiagnostic(
                    code='EMPTY_PROGRAM',
                    severity=ScaraDiagnosticSeverity.ERROR,
                    message='Program contains no executable instructions.',
                    line=1,
                    command='',
                )
            )
            return tuple(diagnostics)

        is_homed: bool = False
        motion_occurred: bool = False
        pump_on: bool = False
        valve_on: bool = False
        zone_mode: str = 'FINE'
        zone_radius: float = 0.0
        last_coords: tuple[float, float, float, float] | None = None

        for inst in instructions:
            cmd = inst.command_type
            params = inst.parameters
            line = inst.line_number

            match cmd:
                case ScaraCommandType.HOME:
                    is_homed = True
                    last_coords = None

                case ScaraCommandType.ZONE:
                    zone_mode = str(params.get('mode', 'FINE')).upper()
                    zone_radius = float(params.get('radius', 0.0))

                case (
                    ScaraCommandType.MOVE_L
                    | ScaraCommandType.MOVE_J
                    | ScaraCommandType.ARC_CW
                    | ScaraCommandType.ARC_CCW
                    | ScaraCommandType.JUMP
                    | ScaraCommandType.APPROACH
                    | ScaraCommandType.RETRACT
                    | ScaraCommandType.MOVE_PALLET
                ):
                    last_coords = self._check_motion(
                        inst=inst,
                        is_homed=is_homed,
                        motion_occurred=motion_occurred,
                        last_coords=last_coords,
                        diagnostics=diagnostics,
                    )
                    motion_occurred = True

                case ScaraCommandType.PUMP | ScaraCommandType.VALVE:
                    pump_on, valve_on = self._check_pneumatics(
                        inst=inst,
                        pump_on=pump_on,
                        valve_on=valve_on,
                        zone_mode=zone_mode,
                        zone_radius=zone_radius,
                        diagnostics=diagnostics,
                    )
                    last_coords = None

                case ScaraCommandType.WAIT_MS:
                    delay_ms: float = float(params.get('ms', 0.0))
                    if delay_ms <= 0.0:
                        diagnostics.append(
                            ScaraDiagnostic(
                                code='DEAD_WAIT',
                                severity=ScaraDiagnosticSeverity.INFO,
                                message=f'Dwell delay WAIT_MS {delay_ms:.0f} is non-positive and produces no pause.',
                                line=line,
                                command='WAIT_MS',
                            )
                        )
                    if zone_mode != 'FINE' and zone_radius > 0.0:
                        diagnostics.append(
                            ScaraDiagnostic(
                                code='TOOL_IN_FLYBY',
                                severity=ScaraDiagnosticSeverity.WARNING,
                                message='Dwell pause WAIT_MS issued during active continuous blend zone.',
                                line=line,
                                command='WAIT_MS',
                            )
                        )
                    last_coords = None

                case _:
                    pass

        return tuple(diagnostics)

    def _check_pneumatics(
        self,
        *,
        inst: IScaraInstruction,
        pump_on: bool,
        valve_on: bool,
        zone_mode: str,
        zone_radius: float,
        diagnostics: list[ScaraDiagnostic],
    ) -> tuple[bool, bool]:
        '''
            Evaluates vacuum pump and blow-off valve state consistency.

            :param inst: Current tool instruction node.
            :param pump_on: Active vacuum pump state.
            :param valve_on: Active blow-off valve state.
            :param zone_mode: Active zone mode ('FINE' or 'BLEND').
            :param zone_radius: Active blend corner radius.
            :param diagnostics: Accumulator list for diagnostic findings.
            :return: Tuple of updated (pump_on, valve_on) states.
            :exceptions: None.
        '''
        line = inst.line_number
        is_pump = inst.command_type == ScaraCommandType.PUMP
        target_state = str(inst.parameters.get('state', 'OFF')).upper() == 'ON'

        if zone_mode != 'FINE' and zone_radius > 0.0:
            diagnostics.append(
                ScaraDiagnostic(
                    code='TOOL_IN_FLYBY',
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message=f'Tool action {inst.command_type.value} issued during active continuous blend zone.',
                    line=line,
                    command=inst.command_type.value,
                )
            )

        if is_pump:
            if target_state and pump_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='REDUNDANT_TOOL_CMD',
                        severity=ScaraDiagnosticSeverity.WARNING,
                        message='PUMP is already ON. Redundant actuation command.',
                        line=line,
                        command='PUMP',
                    )
                )
            elif not target_state and not pump_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='REDUNDANT_TOOL_CMD',
                        severity=ScaraDiagnosticSeverity.WARNING,
                        message='PUMP is already OFF. Redundant actuation command.',
                        line=line,
                        command='PUMP',
                    )
                )
            if target_state and valve_on:
                diagnostics.append(
                    ScaraDiagnostic(
                        code='PNEUMATIC_CONFLICT',
                        severity=ScaraDiagnosticSeverity.ERROR,
                        message='Cannot turn PUMP ON while blow-off VALVE is active. Pneumatic contention detected.',
                        line=line,
                        command='PUMP',
                    )
                )
            return target_state, valve_on

        if target_state and valve_on:
            diagnostics.append(
                ScaraDiagnostic(
                    code='REDUNDANT_TOOL_CMD',
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message='VALVE is already ON. Redundant actuation command.',
                    line=line,
                    command='VALVE',
                )
            )
        elif not target_state and not valve_on:
            diagnostics.append(
                ScaraDiagnostic(
                    code='REDUNDANT_TOOL_CMD',
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message='VALVE is already OFF. Redundant actuation command.',
                    line=line,
                    command='VALVE',
                )
            )
        if target_state and pump_on:
            diagnostics.append(
                ScaraDiagnostic(
                    code='PNEUMATIC_CONFLICT',
                    severity=ScaraDiagnosticSeverity.ERROR,
                    message='Cannot turn blow-off VALVE ON while vacuum PUMP is active. Pneumatic contention detected.',
                    line=line,
                    command='VALVE',
                )
            )
        return pump_on, target_state

    def _check_motion(
        self,
        *,
        inst: IScaraInstruction,
        is_homed: bool,
        motion_occurred: bool,
        last_coords: tuple[float, float, float, float] | None,
        diagnostics: list[ScaraDiagnostic],
    ) -> tuple[float, float, float, float] | None:
        '''
            Evaluates calibration prerequisites and duplicate trajectory moves.

            :param inst: Current motion instruction node.
            :param is_homed: True if machine has been homed or calibrated.
            :param motion_occurred: True if a prior motion instruction was processed.
            :param last_coords: Coordinates of prior linear move or None.
            :param diagnostics: Accumulator list for diagnostic findings.
            :return: Updated target coordinates or None.
            :exceptions: None.
        '''
        line = inst.line_number
        cmd = inst.command_type
        params = inst.parameters

        if not is_homed and not motion_occurred:
            diagnostics.append(
                ScaraDiagnostic(
                    code='UNCALIBRATED_MOTION',
                    severity=ScaraDiagnosticSeverity.WARNING,
                    message='First motion instruction occurs before HOME or SETPOS calibration. Machine coordinates unreferenced.',
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
                if last_coords is not None and coords == last_coords:
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
                return coords

        return None
