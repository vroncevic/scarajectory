# -*- coding: UTF-8 -*-

'''
Module
    motion_command_parser.py
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
    Implementation of ICommandParser parsing Cartesian MOVE_L, MOVE_J and HOME commands.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.token.token import Token
from scarajectory.core.service.dsl.ast.iinstruction_factory import IInstructionFactory
from scarajectory.core.service.dsl.ast.instruction_factory import InstructionFactory
from scarajectory.core.service.dsl.parser.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandParser:
    '''
        Command parser handler for MOVE_L, MOVE_J and HOME motion instructions.

        It defines:

            :attributes:
                | _instruction_factory - Injected IInstructionFactory instance.
            :methods:
                | __init__ - Initializes MotionCommandParser with injected factory.
                | can_parse - Checks whether command is MOVE_L, MOVE_J or HOME.
                | parse - Parses motion statement tokens into Instruction.
    '''

    _instruction_factory: IInstructionFactory

    def __init__(self, *, instruction_factory: IInstructionFactory = InstructionFactory()) -> None:
        '''
            Initializes MotionCommandParser constructor.

            :param instruction_factory: Injected IInstructionFactory instance.
        '''
        self._instruction_factory = instruction_factory

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is MOVE_L, MOVE_J or HOME.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in ('MOVE_L', 'MOVE_J', 'HOME')

    def parse(
        self,
        *,
        tokens: tuple[Token, ...],
        line_num: int,
        raw_text: str,
    ) -> Instruction:
        '''
            Parses MOVE_L, MOVE_J, or HOME statement into Instruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: Instruction node.
        '''
        cmd = tokens[0].value.upper()
        if cmd == 'HOME':
            return self._instruction_factory.create(
                command_type=CommandType.HOME,
                line_number=line_num,
                raw_text=raw_text,
                parameters={},
            )

        cmd_type = (
            CommandType.MOVE_L if cmd == 'MOVE_L' else CommandType.MOVE_J
        )
        params = ParameterExtractor.extract_key_values(tokens=tokens[1:])

        return self._instruction_factory.create(
            command_type=cmd_type,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
