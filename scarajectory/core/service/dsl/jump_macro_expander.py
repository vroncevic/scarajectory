# -*- coding: UTF-8 -*-

'''
Module
    jump_macro_expander.py
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
    Implementation of IMacroExpander expanding high-speed JUMP arch pick-and-place trajectories.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType
from scarajectory.core.model.dsl.scara_instruction import ScaraInstruction
from scarajectory.core.service.dsl.scara_compiler_context import ScaraCompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JumpMacroExpander:
    '''
        Macro expander generating 3D parabolic clearance trajectories for JUMP commands.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if instruction is of type JUMP.
                | expand - Expands JUMP instruction into vertical lift, horizontal transit, and descent.
    '''

    def can_expand(self, *, instruction: IScaraInstruction) -> bool:
        '''
            Checks whether this expander handles JUMP instructions.

            :param instruction: Instruction node to check.
            :return: True if instruction is JUMP, False otherwise.
        '''
        return instruction.command_type == ScaraCommandType.JUMP

    def expand(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[IScaraInstruction, ...]:
        '''
            Expands JUMP into 3-phase 3D clearance motion.

            :param instruction: JUMP instruction node.
            :param context: Active compiler context.
            :return: Tuple of expanded motion instructions.
        '''
        params = instruction.parameters
        target_x: float = float(params.get('X', context.current_x))
        target_y: float = float(params.get('Y', context.current_y))
        target_z: float = float(params.get('Z', 0.0))
        target_phi: float = float(params.get('PHI', context.current_phi))
        arch_height: float = float(params.get('ARCH', 20.0))
        speed: float = float(params.get('SPEED', context.speed_rapid))

        clearance_z = max(context.current_z, target_z) + arch_height
        line_num = instruction.line_number

        lift_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=line_num,
            raw_text=f'# JUMP phase 1 (Lift): Z={clearance_z:.2f}',
            parameters={
                'X': context.current_x,
                'Y': context.current_y,
                'Z': clearance_z,
                'PHI': context.current_phi,
                'SPEED': speed,
            },
        )

        transit_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_J,
            line_number=line_num,
            raw_text=f'# JUMP phase 2 (Transit): X={target_x:.2f} Y={target_y:.2f}',
            parameters={
                'X': target_x,
                'Y': target_y,
                'Z': clearance_z,
                'PHI': target_phi,
                'SPEED': speed,
            },
        )

        descend_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=line_num,
            raw_text=f'# JUMP phase 3 (Descent): Z={target_z:.2f}',
            parameters={
                'X': target_x,
                'Y': target_y,
                'Z': target_z,
                'PHI': target_phi,
                'SPEED': speed,
            },
        )

        context.current_x = target_x
        context.current_y = target_y
        context.current_z = target_z
        context.current_phi = target_phi

        return lift_inst, transit_inst, descend_inst
