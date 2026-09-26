# -*- coding: UTF-8 -*-

'''
Module
    state_command_compiler.py
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
    Compiles machine state, kinematics configuration, and speed override DSL instructions into compiler context.
'''

from __future__ import annotations

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


class StateCommandCompiler:
    '''
        Sub-compiler handling state, speed, acceleration, elbow, and zone configuration instructions.

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled CommandType instances.
            :methods:
                | can_compile - Checks if command is a state configuration instruction.
                | compile - Updates ScaraCompilerContext with instruction parameters.
    '''

    _SUPPORTED: frozenset[CommandType] = frozenset({
        CommandType.SPEED,
        CommandType.ACCEL,
        CommandType.OVERRIDE,
        CommandType.CONFIG_ELBOW,
        CommandType.ZONE,
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
            Applies state configuration parameters to compiler context.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        params = instruction.parameters
        cmd_type = instruction.command_type

        match cmd_type:
            case CommandType.SPEED:
                mode = str(params.get('mode', 'WORK')).upper()
                spd = float(params.get('speed', 40.0))
                if mode == 'RAPID':
                    context.speed_rapid = spd
                else:
                    context.speed_work = spd
                    context.current_speed = spd
            case CommandType.ACCEL:
                context.active_accel = float(params.get('accel', 300.0))
            case CommandType.OVERRIDE:
                context.speed_override_pct = float(params.get('percent', 100.0))
            case CommandType.CONFIG_ELBOW:
                context.elbow_config = str(params.get('elbow', 'RIGHT')).upper()
            case CommandType.ZONE:
                context.zone_mode = str(params.get('mode', 'FINE')).upper()
                context.zone_radius = float(params.get('radius', 0.0))
            case _:
                pass
