# -*- coding: UTF-8 -*-

'''
Module
    config_command_parser.py
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
    Implementation of ICommandParser parsing CONFIG, SPEED, ACCEL, and OVERRIDE commands.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType
from scarajectory.core.model.dsl.scara_instruction import ScaraInstruction
from scarajectory.core.model.dsl.scara_token import ScaraToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigCommandParser:
    '''
        Command parser handler for configuration and dynamics instructions.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_parse - Checks whether command is CONFIG, SPEED, ACCEL, or OVERRIDE.
                | parse - Parses configuration statement tokens into ScaraInstruction.
    '''

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is CONFIG, SPEED, ACCEL, or OVERRIDE.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in ('CONFIG', 'SPEED', 'ACCEL', 'OVERRIDE')

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> IScaraInstruction:
        '''
            Parses configuration statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: IScaraInstruction node.
            :exceptions: ValueError on invalid parameter syntax.
        '''
        cmd = tokens[0].value.upper()
        match cmd:
            case 'CONFIG':
                if len(tokens) < 3:
                    raise ValueError(
                        f'Invalid CONFIG syntax at line {line_num}. Expected: CONFIG ELBOW <LEFT|RIGHT>'
                    )
                sub = tokens[1].value.upper()
                if sub != 'ELBOW':
                    raise ValueError(
                        f'Unknown CONFIG property {sub!r} at line {line_num}'
                    )
                val = tokens[2].value.upper()
                if val not in ('LEFT', 'RIGHT'):
                    raise ValueError(
                        f'Invalid elbow configuration {val!r} at line {line_num}. Must be LEFT or RIGHT'
                    )
                return ScaraInstruction(
                    command_type=ScaraCommandType.CONFIG_ELBOW,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={'elbow': val},
                )
            case 'SPEED':
                if len(tokens) < 3:
                    raise ValueError(
                        f'Invalid SPEED syntax at line {line_num}. Expected: SPEED <RAPID|WORK> <val>'
                    )
                mode = tokens[1].value.upper()
                val = float(tokens[2].value)
                return ScaraInstruction(
                    command_type=ScaraCommandType.SPEED,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={'mode': mode, 'speed': val},
                )
            case 'ACCEL':
                if len(tokens) < 2:
                    raise ValueError(
                        f'Missing argument for ACCEL at line {line_num}'
                    )
                return ScaraInstruction(
                    command_type=ScaraCommandType.ACCEL,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={'accel': float(tokens[1].value)},
                )
            case _:
                if len(tokens) < 2:
                    raise ValueError(
                        f'Missing argument for OVERRIDE at line {line_num}'
                    )
                return ScaraInstruction(
                    command_type=ScaraCommandType.OVERRIDE,
                    line_number=line_num,
                    raw_text=raw_text,
                    parameters={'percent': float(tokens[1].value)},
                )
