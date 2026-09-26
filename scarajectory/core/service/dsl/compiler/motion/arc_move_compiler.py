# -*- coding: UTF-8 -*-

'''
Module
    arc_move_compiler.py
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
    Compiles circular arc DSL instructions (ARC_CW, ARC_CCW) using injected arc interpolator.
'''

from __future__ import annotations

from typing import Any

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.motion.iarc_interpolator import IArcInterpolator
from scarajectory.core.service.dsl.compiler.scara_compiler_context import ScaraCompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcMoveCompiler:
    '''
        Sub-compiler handling circular arc motion instructions (ARC_CW, ARC_CCW).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled CommandType instances.
                | _arc_interpolator - Circular arc interpolator collaborator.
            :methods:
                | __init__ - Initializes ArcMoveCompiler with injected arc interpolator.
                | can_compile - Checks if command is an arc motion instruction.
                | compile - Interpolates circular arc and appends interpolated waypoints.
    '''

    _SUPPORTED: frozenset[CommandType] = frozenset({
        CommandType.ARC_CW,
        CommandType.ARC_CCW,
    })

    def __init__(
        self,
        *,
        arc_interpolator: IArcInterpolator,
    ) -> None:
        '''
            Initializes ArcMoveCompiler with injected interpolator.

            :param arc_interpolator: Injected IArcInterpolator component.
            :exceptions: None.
        '''
        self._arc_interpolator: IArcInterpolator = arc_interpolator

    def can_compile(self, *, instruction: Instruction) -> bool:
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
        instruction: Instruction,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''
            Processes circular arc motion instructions and appends interpolated waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        params: Any = instruction.parameters
        is_clockwise: bool = (instruction.command_type == CommandType.ARC_CW)
        start_x: float = context.current_x
        start_y: float = context.current_y
        target_x_raw: float = float(params.get('X', start_x))
        target_y_raw: float = float(params.get('Y', start_y))
        target_z: float = float(params.get('Z', context.current_z))
        spd: float = float(params.get('SPEED', context.current_speed))
        offset_i: float = float(params.get('I', 0.0))
        offset_j: float = float(params.get('J', 0.0))

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

        effective_spd: float = spd * (context.speed_override_pct / 100.0)
        for px, py, tangent_deg in arc_points:
            phi: float = (
                tangent_deg
                if context.tool_orient_mode == 'TANGENTIAL'
                else context.current_phi
            )
            waypoints.append(
                Waypoint(
                    x=px,
                    y=py,
                    z=target_z,
                    phi=phi,
                    speed=effective_spd,
                    name='',
                    command='',
                )
            )

        context.current_x = end_x
        context.current_y = end_y
        context.current_z = target_z
