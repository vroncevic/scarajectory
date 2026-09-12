# -*- coding: UTF-8 -*-

'''
Module
    control_command_compiler.py
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
    Compiles workflow control, homing, dwell, and motor enable/disable DSL instructions into waypoints.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.ast.scara_command_type import ScaraCommandType
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.scara_compiler_context import (
    ScaraCompilerContext,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlCommandCompiler:
    '''
        Sub-compiler handling execution control instructions (HOME, WAIT_MS, HOLD, RESUME, ESTOP, ENABLE, DISABLE).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
            :methods:
                | can_compile - Checks if command is a workflow control instruction.
                | compile - Appends control command waypoints to the waypoint accumulator.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.HOME,
        ScaraCommandType.WAIT_MS,
        ScaraCommandType.HOLD,
        ScaraCommandType.RESUME,
        ScaraCommandType.ESTOP,
        ScaraCommandType.ENABLE,
        ScaraCommandType.DISABLE,
    })

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
            Processes control instructions and appends control command waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        params = instruction.parameters
        cmd_type = instruction.command_type

        match cmd_type:
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
                cmd_name = (
                    'ENABLE'
                    if cmd_type == ScaraCommandType.ENABLE
                    else 'DISABLE'
                )
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
            case _:
                pass
