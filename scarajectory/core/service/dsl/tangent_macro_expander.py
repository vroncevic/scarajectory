# -*- coding: UTF-8 -*-

'''
Module
    tangent_macro_expander.py
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
    Implementation of IMacroExpander adjusting 4th-axis tool orientation to follow path tangent.
'''

from __future__ import annotations

from math import atan2, degrees, hypot

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType
from scarajectory.core.service.dsl.scara_compiler_context import ScaraCompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TangentMacroExpander:
    '''
        Macro expander computing tangential orientation for the 4th wrist roll axis along path.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if instruction configures tool orient or is motion requiring tangential Phi.
                | expand - Updates orientation mode or calculates tangent angle for motion target.
    '''

    def can_expand(self, *, instruction: IScaraInstruction) -> bool:
        '''
            Checks whether this expander handles TOOL_ORIENT instructions.

            :param instruction: Instruction node to check.
            :return: True if TOOL_ORIENT, False otherwise.
        '''
        return instruction.command_type == ScaraCommandType.TOOL_ORIENT

    def expand(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[IScaraInstruction, ...]:
        '''
            Configures tool orientation mode in compiler context.

            :param instruction: TOOL_ORIENT instruction node.
            :param context: Active compiler context.
            :return: Informational marker instruction.
        '''
        params = instruction.parameters
        mode = str(params.get('mode', 'FIXED')).upper()
        context.tool_orient_mode = mode
        if 'phi' in params:
            context.current_phi = float(params['phi'])

        return ()

    def calculate_tangent_angle(
        self,
        *,
        current_x: float,
        current_y: float,
        target_x: float,
        target_y: float,
        fallback_phi: float,
    ) -> float:
        '''
            Computes tangent heading angle in degrees between two 2D points.

            :param current_x: Source X coordinate.
            :param current_y: Source Y coordinate.
            :param target_x: Destination X coordinate.
            :param target_y: Destination Y coordinate.
            :param fallback_phi: Heading to return if travel distance is zero.
            :return: Heading angle in degrees [-180, +180].
        '''
        dx = target_x - current_x
        dy = target_y - current_y
        dist = hypot(dx, dy)
        if dist < 1e-4:
            return fallback_phi
        return degrees(atan2(dy, dx))
