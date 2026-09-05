# -*- coding: UTF-8 -*-

'''
Module
    pallet_macro_expander.py
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
    Implementation of IMacroExpander resolving pallet matrix definitions into discrete coordinates.
'''

from __future__ import annotations

from typing import Any

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


class PalletMacroExpander:
    '''
        Macro expander managing pallet matrix layout definitions and calculating cell index targets.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if instruction is PALLET_DEF or MOVE_PALLET.
                | expand - Registers pallet metadata or translates MOVE_PALLET into Cartesian motion.
    '''

    def can_expand(self, *, instruction: IScaraInstruction) -> bool:
        '''
            Checks whether this expander handles pallet instructions.

            :param instruction: Instruction node to check.
            :return: True if PALLET_DEF or MOVE_PALLET, False otherwise.
        '''
        return instruction.command_type in (
            ScaraCommandType.PALLET_DEF,
            ScaraCommandType.MOVE_PALLET,
        )

    def expand(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[IScaraInstruction, ...]:
        '''
            Processes PALLET_DEF or calculates cell coordinate for MOVE_PALLET.

            :param instruction: Pallet instruction node.
            :param context: Active compiler context.
            :return: Tuple of resulting instructions.
            :exceptions: KeyError if MOVE_PALLET references undefined pallet name.
        '''
        params = instruction.parameters
        line_num = instruction.line_number

        if instruction.command_type == ScaraCommandType.PALLET_DEF:
            name: str = str(params.get('name', 'DEFAULT')).upper()
            pallet_info: dict[str, Any] = {
                'rows': int(params.get('ROWS', 1)),
                'cols': int(params.get('COLS', 1)),
                'dx': float(params.get('DX', 20.0)),
                'dy': float(params.get('DY', 20.0)),
                'start_x': float(params.get('START_X', context.current_x)),
                'start_y': float(params.get('START_Y', context.current_y)),
            }
            context.pallets[name] = pallet_info
            return ()

        name = str(params.get('name', 'DEFAULT')).upper()
        if name not in context.pallets:
            raise KeyError(
                f'Error at line {line_num}: Pallet {name!r} is not defined before MOVE_PALLET'
            )

        p_info = context.pallets[name]
        index = int(params.get('INDEX', 0))
        cols = int(p_info['cols'])
        row = index // cols
        col = index % cols

        local_x = float(p_info['start_x']) + col * float(p_info['dx'])
        local_y = float(p_info['start_y']) + row * float(p_info['dy'])
        global_x, global_y = context.transform_point(x=local_x, y=local_y)
        target_z = float(params.get('Z', context.current_z))

        context.current_x = global_x
        context.current_y = global_y
        context.current_z = target_z

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=line_num,
            raw_text=f'# MOVE_PALLET: {name}[{index}] -> X={global_x:.2f} Y={global_y:.2f} Z={target_z:.2f}',
            parameters={
                'X': global_x,
                'Y': global_y,
                'Z': target_z,
                'PHI': context.current_phi,
                'SPEED': context.current_speed,
            },
        )
        return (move_inst,)
