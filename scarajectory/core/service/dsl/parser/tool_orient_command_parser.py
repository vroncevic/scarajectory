# -*- coding: UTF-8 -*-

'''
Module
    tool_orient_command_parser.py
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
    Implementation of ICommandParser parsing TOOL_ORIENT wrist 4th-axis orientation commands.
'''

from __future__ import annotations

from typing import Any

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


class ToolOrientCommandParser:
    '''
        Command parser handler for wrist tool orientation mode instructions.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_parse - Checks whether command is TOOL_ORIENT.
                | parse - Parses tool orient statement tokens into ScaraInstruction.
    '''

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is TOOL_ORIENT.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == 'TOOL_ORIENT'

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> IScaraInstruction:
        '''
            Parses tool orient statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: IScaraInstruction node.
            :exceptions: ValueError on missing orientation mode.
        '''
        if len(tokens) < 2:
            raise ValueError(
                f'Invalid TOOL_ORIENT syntax at line {line_num}. Expected: TOOL_ORIENT <TANGENTIAL|FIXED|JOINT_LOCKED>'
            )

        mode = tokens[1].value.upper()
        sub_params = ParameterExtractor.extract_key_values(tokens=tokens[2:])
        params: dict[str, Any] = {'mode': mode}
        if 'PHI' in sub_params:
            params['phi'] = sub_params['PHI']

        return ScaraInstruction(
            command_type=ScaraCommandType.TOOL_ORIENT,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
