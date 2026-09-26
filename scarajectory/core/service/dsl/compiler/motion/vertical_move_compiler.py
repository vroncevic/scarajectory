# -*- coding: UTF-8 -*-

'''
Module
    vertical_move_compiler.py
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
    Compiles vertical approach and retract motion DSL instructions (APPROACH, RETRACT) into waypoints.
'''

from __future__ import annotations

from typing import Any

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.scara_compiler_context import ScaraCompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VerticalMoveCompiler:
    '''
        Sub-compiler handling vertical motion instructions (APPROACH, RETRACT).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled CommandType instances.
            :methods:
                | can_compile - Checks if command is an APPROACH or RETRACT instruction.
                | compile - Adjusts height coordinates and appends vertical motion waypoints.
    '''

    _SUPPORTED: frozenset[CommandType] = frozenset({
        CommandType.APPROACH,
        CommandType.RETRACT,
    })

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
            Processes APPROACH and RETRACT instructions and appends computed waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        params: Any = instruction.parameters
        cmd_type: CommandType = instruction.command_type
        dist: float = float(params.get('DIST', 10.0))

        if cmd_type == CommandType.APPROACH:
            spd: float = float(params.get('SPEED', context.speed_work))
            target_z: float = max(0.0, context.current_z - dist)
            name: str = 'APPROACH'
        else:
            spd = float(params.get('SPEED', context.speed_rapid))
            target_z = context.current_z + dist
            name = 'RETRACT'

        context.current_z = target_z
        waypoints.append(
            Waypoint(
                x=context.current_x,
                y=context.current_y,
                z=target_z,
                phi=context.current_phi,
                speed=spd,
                name=name,
                command='',
            )
        )
