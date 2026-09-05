# -*- coding: UTF-8 -*-

'''
Module
    jump_command_parser.py
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
    Implementation of ICommandParser parsing 3D parabolic JUMP commands.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType
from scarajectory.core.model.dsl.scara_instruction import ScaraInstruction
from scarajectory.core.model.dsl.scara_token import ScaraToken
from scarajectory.core.service.dsl.parser.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JumpCommandParser:
    '''
        Command parser handler for JUMP arch pick-and-place instructions.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_parse - Checks whether command is JUMP.
                | parse - Parses JUMP statement tokens into ScaraInstruction.
    '''

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is JUMP.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == 'JUMP'

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> IScaraInstruction:
        '''
            Parses JUMP statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: IScaraInstruction node.
        '''
        params = ParameterExtractor.extract_key_values(tokens=tokens[1:])
        return ScaraInstruction(
            command_type=ScaraCommandType.JUMP,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
