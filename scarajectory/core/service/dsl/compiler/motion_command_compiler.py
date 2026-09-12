# -*- coding: UTF-8 -*-

'''
Module
    motion_command_compiler.py
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
    Compiles Cartesian linear, joint, approach, retract, and circular arc DSL instructions into waypoints.
'''

from __future__ import annotations

from typing import Any

from scarajectory.core.model.dsl.ast.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.ast.scara_command_type import ScaraCommandType
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.arc_interpolator import (
    ArcInterpolator,
)
from scarajectory.core.service.dsl.compiler.iarc_interpolator import (
    IArcInterpolator,
)
from scarajectory.core.service.dsl.compiler.scara_compiler_context import (
    ScaraCompilerContext,
)
from scarajectory.core.service.dsl.macro.tangent_macro_expander import (
    TangentMacroExpander,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandCompiler:
    '''
        Sub-compiler handling motion instructions (MOVE_L, MOVE_J, APPROACH, RETRACT, ARC_CW, ARC_CCW).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
                | _arc_interpolator - Circular arc interpolator collaborator.
                | _tangent_helper - Tangent heading angle calculator helper.
            :methods:
                | __init__ - Initializes motion compiler with optional arc interpolator and tangent helper.
                | can_compile - Checks if command is a motion instruction.
                | compile - Interpolates path, transforms frames, and appends motion waypoints.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.MOVE_L,
        ScaraCommandType.MOVE_J,
        ScaraCommandType.APPROACH,
        ScaraCommandType.RETRACT,
        ScaraCommandType.ARC_CW,
        ScaraCommandType.ARC_CCW,
    })

    def __init__(
        self,
        *,
        arc_interpolator: IArcInterpolator | None = None,
        tangent_helper: TangentMacroExpander | None = None,
    ) -> None:
        '''
            Initializes MotionCommandCompiler with injected interpolator and tangent helper.

            :param arc_interpolator: Optional IArcInterpolator component.
            :param tangent_helper: Optional TangentMacroExpander helper for heading calculation.
            :exceptions: None.
        '''
        self._arc_interpolator: IArcInterpolator = (
            arc_interpolator
            if arc_interpolator is not None
            else ArcInterpolator()
        )
        self._tangent_helper: TangentMacroExpander = (
            tangent_helper
            if tangent_helper is not None
            else TangentMacroExpander()
        )

    def can_compile(self, *, instruction: IScaraInstruction) -> bool:
        '''
            Determines whether this sub-compiler handles the specified instruction.

            :param instruction: Primitive AST instruction node.
            :return: True if handled, False otherwise.
            :exceptions: None.
        '''
        return instruction.command_type in self._SUPPORTED

    def compile(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''
            Processes motion instructions and appends computed waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        params = instruction.parameters
        cmd_type = instruction.command_type

        match cmd_type:
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
