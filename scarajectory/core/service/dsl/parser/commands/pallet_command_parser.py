# -*- coding: UTF-8 -*-

'''
Module
    pallet_command_parser.py
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
    Implementation of ICommandParser parsing PALLET_DEF and MOVE_PALLET commands.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.token.token import Token
from scarajectory.core.service.dsl.parser.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PalletCommandParser:
    '''
        Command parser handler for pallet matrix definition and navigation.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_parse - Checks whether command is PALLET_DEF or MOVE_PALLET.
                | parse - Parses pallet statement tokens into Instruction.
    '''

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is PALLET_DEF or MOVE_PALLET.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in ('PALLET_DEF', 'MOVE_PALLET')

    def parse(
        self,
        *,
        tokens: tuple[Token, ...],
        line_num: int,
        raw_text: str,
    ) -> Instruction:
        '''
            Parses pallet statement into Instruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: Instruction node.
            :exceptions: ValueError on missing pallet name argument.
        '''
        cmd = tokens[0].value.upper()

        if len(tokens) < 2:
            raise ValueError(
                f'Missing pallet name for {cmd} at line {line_num}'
            )

        pallet_name = tokens[1].value.upper()
        params = ParameterExtractor.extract_key_values(tokens=tokens[2:])
        params['name'] = pallet_name

        cmd_type = (
            CommandType.PALLET_DEF
            if cmd == 'PALLET_DEF'
            else CommandType.MOVE_PALLET
        )

        return Instruction(
            command_type=cmd_type,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
