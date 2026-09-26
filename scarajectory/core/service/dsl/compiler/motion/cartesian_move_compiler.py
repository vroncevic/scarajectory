# -*- coding: UTF-8 -*-

'''
Module
    cartesian_move_compiler.py
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
    Compiles Cartesian linear and joint motion DSL instructions (MOVE_L, MOVE_J) into waypoints.
'''

from __future__ import annotations

from typing import Any

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scarajectory.core.service.dsl.macro.tangent_macro_expander import TangentMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CartesianMoveCompiler:
    '''
        Sub-compiler handling Cartesian linear and joint motion instructions (MOVE_L, MOVE_J).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled CommandType instances.
                | _tangent_helper - Tangent heading angle calculator helper.
            :methods:
                | __init__ - Initializes Cartesian move compiler with injected tangent helper.
                | can_compile - Checks if command is a Cartesian motion instruction.
                | compile - Transforms coordinate frames and appends motion waypoints.
    '''

    _SUPPORTED: frozenset[CommandType] = frozenset({
        CommandType.MOVE_L,
        CommandType.MOVE_J,
    })

    def __init__(
        self,
        *,
        tangent_helper: TangentMacroExpander,
    ) -> None:
        '''
            Initializes CartesianMoveCompiler with injected tangent helper.

            :param tangent_helper: Injected TangentMacroExpander helper for heading calculation.
            :exceptions: None.
        '''
        self._tangent_helper: TangentMacroExpander = tangent_helper

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
            Processes Cartesian linear and joint motion instructions and appends computed waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        params: Any = instruction.parameters
        raw_x: float = float(params.get('X', context.current_x))
        raw_y: float = float(params.get('Y', context.current_y))
        target_z: float = float(params.get('Z', context.current_z))
        target_spd: float = float(params.get('SPEED', context.current_speed))

        global_x, global_y = context.transform_point(x=raw_x, y=raw_y)

        if context.tool_orient_mode == 'TANGENTIAL':
            target_phi: float = self._tangent_helper.calculate_tangent_angle(
                current_x=context.current_x,
                current_y=context.current_y,
                target_x=global_x,
                target_y=global_y,
                fallback_phi=context.current_phi,
            )
        else:
            target_phi = float(params.get('PHI', context.current_phi))

        effective_spd: float = target_spd * (context.speed_override_pct / 100.0)

        waypoints.append(
            Waypoint(
                x=global_x,
                y=global_y,
                z=target_z,
                phi=target_phi,
                speed=effective_spd,
                name='',
                command='',
            )
        )

        context.current_x = global_x
        context.current_y = global_y
        context.current_z = target_z
        context.current_phi = target_phi
