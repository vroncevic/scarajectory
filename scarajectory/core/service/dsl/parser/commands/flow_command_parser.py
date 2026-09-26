# -*- coding: UTF-8 -*-

'''
Module
    flow_command_parser.py
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
    Implementation of ICommandParser parsing execution flow control and safety commands.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.token.token import Token
from scarajectory.core.service.dsl.ast.iinstruction_factory import IInstructionFactory
from scarajectory.core.service.dsl.ast.instruction_factory import InstructionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowCommandParser:
    '''
        Command parser handler for flow control, pauses, delays and safety aborts.

        It defines:

            :attributes:
                | _instruction_factory - Injected IInstructionFactory instance.
            :methods:
                | __init__ - Initializes FlowCommandParser with injected factory.
                | can_parse - Checks whether command is WAIT_MS, SYNC, HOLD, PAUSE, RESUME, or ESTOP.
                | parse - Parses flow control statement tokens into Instruction.
    '''

    _instruction_factory: IInstructionFactory

    def __init__(self, *, instruction_factory: IInstructionFactory = InstructionFactory()) -> None:
        '''
            Initializes FlowCommandParser constructor.

            :param instruction_factory: Injected IInstructionFactory instance.
        '''
        self._instruction_factory = instruction_factory

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is WAIT, WAIT_MS, SYNC, HOLD, PAUSE, RESUME, or ESTOP.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in (
            'WAIT',
            'WAIT_MS',
            'SYNC',
            'HOLD',
            'PAUSE',
            'RESUME',
            'ESTOP',
            'ENABLE',
            'DISABLE',
        )

    def parse(
        self,
        *,
        tokens: tuple[Token, ...],
        line_num: int,
        raw_text: str,
    ) -> Instruction:
        '''
            Parses flow control statement into Instruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: Instruction node.
            :exceptions: ValueError on missing WAIT/WAIT_MS delay argument.
        '''
        cmd = tokens[0].value.upper()

        match cmd:
            case 'WAIT' | 'WAIT_MS':
                if len(tokens) < 2:
                    raise ValueError(
                        f'Missing millisecond argument for {cmd} at line {line_num}'
                    )
                ms_val = float(tokens[1].value)

                return self._instruction_factory.create(
                    command_type=CommandType.WAIT_MS,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={'ms': ms_val},
                )
            case 'SYNC':
                return self._instruction_factory.create(
                    command_type=CommandType.SYNC,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={},
                )
            case 'HOLD' | 'PAUSE':
                return self._instruction_factory.create(
                    command_type=CommandType.HOLD,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={},
                )
            case 'RESUME':
                return self._instruction_factory.create(
                    command_type=CommandType.RESUME,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={},
                )
            case 'ENABLE':
                return self._instruction_factory.create(
                    command_type=CommandType.ENABLE,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={},
                )
            case 'DISABLE':
                return self._instruction_factory.create(
                    command_type=CommandType.DISABLE,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={},
                )
            case _:
                return self._instruction_factory.create(
                    command_type=CommandType.ESTOP,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={},
                )

