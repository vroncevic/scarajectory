# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler.py
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
    Implementation of IScaraCompiler transforming SCARA DSL programs into validated trajectory plans.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.iscara_program import IScaraProgram
from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType
from scarajectory.core.model.dsl.scara_diagnostic import ScaraDiagnostic
from scarajectory.core.model.dsl.scara_diagnostic_severity import (
    ScaraDiagnosticSeverity,
)
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.arc_interpolator import (
    ArcInterpolator,
)
from scarajectory.core.service.dsl.compiler.iarc_interpolator import (
    IArcInterpolator,
)
from scarajectory.core.service.dsl.frame_macro_expander import (
    FrameMacroExpander,
)
from scarajectory.core.service.dsl.imacro_expander import IMacroExpander
from scarajectory.core.service.dsl.jump_macro_expander import JumpMacroExpander
from scarajectory.core.service.dsl.linter.iscara_linter import IScaraLinter
from scarajectory.core.service.dsl.linter.scara_linter import ScaraLinter
from scarajectory.core.service.dsl.pallet_macro_expander import (
    PalletMacroExpander,
)
from scarajectory.core.service.dsl.scara_compiler_context import (
    ScaraCompilerContext,
)
from scarajectory.core.service.dsl.tangent_macro_expander import (
    TangentMacroExpander,
)
from scarajectory.core.service.itrajectory_validator import (
    ITrajectoryValidator,
)
from scarajectory.core.service.trajectory_validator import (
    TrajectoryValidator,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompiler:
    '''
        Compiler orchestrator coordinating macro expansion, arc interpolation, and kinematic validation.

        It defines:

            :attributes:
                | _macro_expanders - Tuple of registered IMacroExpander plugins.
                | _validator - Kinematic reachability validator.
                | _tangent_helper - Helper calculating heading angles.
                | _arc_interpolator - Dedicated circular arc interpolator.
                | _linter - Static analysis and safety linter.
            :methods:
                | __init__ - Initializes compiler with optional custom expanders, validator, interpolator, and linter.
                | compile - Compiles IScaraProgram into validated TrajectoryPlan.
                | lint - Lints IScaraProgram and returns diagnostic findings.
    '''

    def __init__(
        self,
        *,
        macro_expanders: Sequence[IMacroExpander] | None = None,
        validator: ITrajectoryValidator | None = None,
        arc_interpolator: IArcInterpolator | None = None,
        linter: IScaraLinter | None = None,
    ) -> None:
        '''
            Initializes ScaraCompiler with injected components.

            :param macro_expanders: Optional custom sequence of IMacroExpander components.
            :param validator: Optional ITrajectoryValidator instance.
            :param arc_interpolator: Optional IArcInterpolator component.
            :param linter: Optional IScaraLinter component.
            :exceptions: None.
        '''
        if macro_expanders is not None:
            self._macro_expanders: tuple[IMacroExpander, ...] = tuple(
                macro_expanders
            )
        else:
            self._macro_expanders = (
                JumpMacroExpander(),
                FrameMacroExpander(),
                PalletMacroExpander(),
                TangentMacroExpander(),
            )
        self._validator: ITrajectoryValidator = (
            validator if validator is not None else TrajectoryValidator()
        )
        self._tangent_helper: TangentMacroExpander = TangentMacroExpander()
        self._arc_interpolator: IArcInterpolator = (
            arc_interpolator
            if arc_interpolator is not None
            else ArcInterpolator()
        )
        self._linter: IScaraLinter = (
            linter if linter is not None else ScaraLinter()
        )

    def lint(
        self,
        *,
        program: IScaraProgram,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Lints a SCARA DSL program and returns diagnostic warnings and errors.

            :param program: Parsed IScaraProgram AST root.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
        return self._linter.lint(program=program)

    def compile(
        self,
        *,
        program: IScaraProgram,
        bounds: ScaraBounds | None = None,
    ) -> TrajectoryPlan:
        '''
            Compiles a SCARA DSL program into an executable and validated TrajectoryPlan.

            :param program: Parsed IScaraProgram AST root.
            :param bounds: Optional kinematic boundary constraints.
            :return: Validated TrajectoryPlan instance.
            :exceptions: ValueError if static analysis or kinematic validation fails.
        '''
        diagnostics = self.lint(program=program)
        errors = [
            d for d in diagnostics
            if d.severity == ScaraDiagnosticSeverity.ERROR
        ]
        if errors:
            err_details = '; '.join(d.format_report() for d in errors)
            raise ValueError(
                f'Compilation aborted due to static analysis errors: {err_details}'
            )

        context = ScaraCompilerContext()
        waypoints: list[Waypoint] = []
        for inst in program.instructions:
            expanded = False
            for expander in self._macro_expanders:
                if expander.can_expand(instruction=inst):
                    for new_inst in expander.expand(
                        instruction=inst, context=context
                    ):
                        self._process_primitive(
                            instruction=new_inst,
                            context=context,
                            waypoints=waypoints,
                        )
                    expanded = True
                    break

            if not expanded:
                self._process_primitive(
                    instruction=inst,
                    context=context,
                    waypoints=waypoints,
                )

        plan = TrajectoryPlan()
        plan.set_waypoints(waypoints)

        active_bounds = bounds if bounds is not None else ScaraBounds()
        validator = (
            TrajectoryValidator(bounds=active_bounds)
            if bounds is not None
            else self._validator
        )
        is_valid, messages = validator.validate_plan(plan=plan)

        if not is_valid:
            err_msg = '; '.join(messages)
            raise ValueError(
                f'Compilation failed kinematic validation: {err_msg}'
            )

        return plan

    def _process_primitive(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''
            Processes primitive non-macro instructions and updates context/waypoints.

            :param instruction: Primitive instruction node.
            :param context: Stateful compiler context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
        '''
        params = instruction.parameters
        cmd_type = instruction.command_type

        match cmd_type:
            case ScaraCommandType.SPEED:
                mode = str(params.get('mode', 'WORK')).upper()
                spd = float(params.get('speed', 40.0))
                if mode == 'RAPID':
                    context.speed_rapid = spd
                else:
                    context.speed_work = spd
                    context.current_speed = spd
            case ScaraCommandType.ACCEL:
                context.active_accel = float(params.get('accel', 300.0))
            case ScaraCommandType.OVERRIDE:
                context.speed_override_pct = float(params.get('percent', 100.0))
            case ScaraCommandType.CONFIG_ELBOW:
                context.elbow_config = str(params.get('elbow', 'RIGHT')).upper()
            case ScaraCommandType.ZONE:
                context.zone_mode = str(params.get('mode', 'FINE')).upper()
                context.zone_radius = float(params.get('radius', 0.0))
            case ScaraCommandType.HOME:
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=0.0,
                        speed=context.speed_rapid,
                        name='HOME',
                        command='<CMD:HOME>',
                    )
                )
            case ScaraCommandType.PUMP:
                pump_on = str(params.get('state', 'OFF')).upper() == 'ON'
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=context.current_phi,
                        speed=context.current_speed,
                        name='PUMP_ON' if pump_on else 'PUMP_OFF',
                        command='<CMD:PUMP#1>' if pump_on else '<CMD:PUMP#0>',
                    )
                )
            case ScaraCommandType.VALVE:
                valve_on = str(params.get('state', 'OFF')).upper() == 'ON'
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=context.current_phi,
                        speed=context.current_speed,
                        name='VALVE_ON' if valve_on else 'VALVE_OFF',
                        command='<CMD:VALVE#1>' if valve_on else '<CMD:VALVE#0>',
                    )
                )
            case ScaraCommandType.WAIT_MS:
                delay_ms = max(0, int(float(params.get('ms', 0.0))))
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=context.current_phi,
                        speed=context.current_speed,
                        name=f'WAIT_{delay_ms}MS',
                        command=f'<CMD:WAIT#{delay_ms}>',
                    )
                )
            case ScaraCommandType.HOLD:
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=context.current_phi,
                        speed=context.current_speed,
                        name='HOLD',
                        command='<CMD:HOLD>',
                    )
                )
            case ScaraCommandType.RESUME:
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=context.current_phi,
                        speed=context.current_speed,
                        name='RESUME',
                        command='<CMD:RESUME>',
                    )
                )
            case ScaraCommandType.ESTOP:
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=context.current_phi,
                        speed=context.current_speed,
                        name='ESTOP',
                        command='<CMD:ESTOP>',
                    )
                )
            case ScaraCommandType.ENABLE | ScaraCommandType.DISABLE:
                cmd_name = 'ENABLE' if cmd_type == ScaraCommandType.ENABLE else 'DISABLE'
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=context.current_z,
                        phi=context.current_phi,
                        speed=context.current_speed,
                        name=cmd_name,
                        command=f'<CMD:{cmd_name}>',
                    )
                )
            case ScaraCommandType.MOVE_L | ScaraCommandType.MOVE_J:
                self._compile_cartesian_move(
                    params=params, context=context, waypoints=waypoints
                )
            case ScaraCommandType.APPROACH:
                dist = float(params.get('DIST', 10.0))
                spd = float(params.get('SPEED', context.speed_work))
                target_z = max(0.0, context.current_z - dist)
                context.current_z = target_z
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=target_z,
                        phi=context.current_phi,
                        speed=spd,
                        name='APPROACH',
                    )
                )
            case ScaraCommandType.RETRACT:
                dist = float(params.get('DIST', 10.0))
                spd = float(params.get('SPEED', context.speed_rapid))
                target_z = context.current_z + dist
                context.current_z = target_z
                waypoints.append(
                    Waypoint(
                        x=context.current_x,
                        y=context.current_y,
                        z=target_z,
                        phi=context.current_phi,
                        speed=spd,
                        name='RETRACT',
                    )
                )
            case ScaraCommandType.ARC_CW | ScaraCommandType.ARC_CCW:
                self._compile_arc_move(
                    is_clockwise=(cmd_type == ScaraCommandType.ARC_CW),
                    params=params,
                    context=context,
                    waypoints=waypoints,
                )
            case _:
                pass

    def _compile_cartesian_move(
        self,
        *,
        params: Any,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''Compiles MOVE_L / MOVE_J with frame translation and tangential heading.'''
        raw_x = float(params.get('X', context.current_x))
        raw_y = float(params.get('Y', context.current_y))
        target_z = float(params.get('Z', context.current_z))
        target_spd = float(params.get('SPEED', context.current_speed))

        global_x, global_y = context.transform_point(x=raw_x, y=raw_y)

        if context.tool_orient_mode == 'TANGENTIAL':
            target_phi = self._tangent_helper.calculate_tangent_angle(
                current_x=context.current_x,
                current_y=context.current_y,
                target_x=global_x,
                target_y=global_y,
                fallback_phi=context.current_phi,
            )
        else:
            target_phi = float(params.get('PHI', context.current_phi))

        effective_spd = target_spd * (context.speed_override_pct / 100.0)

        waypoints.append(
            Waypoint(
                x=global_x,
                y=global_y,
                z=target_z,
                phi=target_phi,
                speed=effective_spd,
            )
        )

        context.current_x = global_x
        context.current_y = global_y
        context.current_z = target_z
        context.current_phi = target_phi

    def _compile_arc_move(
        self,
        *,
        is_clockwise: bool,
        params: Any,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''Interpolates circular arc using injected IArcInterpolator.'''
        start_x = context.current_x
        start_y = context.current_y
        target_x_raw = float(params.get('X', start_x))
        target_y_raw = float(params.get('Y', start_y))
        target_z = float(params.get('Z', context.current_z))
        spd = float(params.get('SPEED', context.current_speed))
        offset_i = float(params.get('I', 0.0))
        offset_j = float(params.get('J', 0.0))

        end_x, end_y = context.transform_point(x=target_x_raw, y=target_y_raw)

        arc_points = self._arc_interpolator.interpolate(
            start_x=start_x,
            start_y=start_y,
            target_x=end_x,
            target_y=end_y,
            offset_i=offset_i,
            offset_j=offset_j,
            is_clockwise=is_clockwise,
        )

        effective_spd = spd * (context.speed_override_pct / 100.0)
        for px, py, tangent_deg in arc_points:
            phi = (
                tangent_deg
                if context.tool_orient_mode == 'TANGENTIAL'
                else context.current_phi
            )
            waypoints.append(
                Waypoint(x=px, y=py, z=target_z, phi=phi, speed=effective_spd)
            )

        context.current_x = end_x
        context.current_y = end_y
        context.current_z = target_z
