# -*- coding: UTF-8 -*-

'''
Module
    command_compiler.py
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
    Compiles auxiliary hardware commands (PUMP, VALVE, WAIT, HOME) into binary frames and steps.
'''

from __future__ import annotations

from struct import pack

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.message_id import MessageId
from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.binary.step import Step
from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandCompiler:
    '''
        Compiles semantic hardware commands into binary wire frames and binary steps.

        It defines:

            :attributes:
                | _frame_builder - Binary frame assembler protocol.
            :methods:
                | __init__ - Initializes command step compiler with injected frame builder.
                | compile_command_step - Compiles a single hardware command into a binary step.
    '''

    _frame_builder: IBinaryFrameBuilder

    def __init__(self, *, frame_builder: IBinaryFrameBuilder) -> None:
        '''
            Initializes command step compiler with injected frame builder.

            :param frame_builder: Injected IBinaryFrameBuilder protocol.
            :exceptions: None.
        '''
        self._frame_builder = frame_builder

    def compile_command_step(self, *, command: str, seq_num: int, line_num: int) -> Step:
        '''
            Compiles a semantic command string into a binary command step.

            :param command: Command text (e.g. PUMP, VALVE, WAIT, HOME).
            :param seq_num: Cyclic sequence counter.
            :param line_num: Source line index.
            :return: Compiled Step.
            :exceptions: None.
        '''
        clean: str = command.strip().upper()
        normalized: str = clean.strip('<>').removeprefix('CMD:')
        parts: list[str] = normalized.replace('#', ' ').split()
        cmd_name: str = parts[0] if parts else ''
        arg: str = parts[1] if len(parts) > 1 else ''
        frame: BinaryFrame

        match cmd_name:
            case CommandType.PUMP:
                is_on: bool = arg in ('1', 'ON') if arg else ('1' in clean or 'ON' in clean)
                frame = self._frame_builder.build_tool_cmd(
                    seq_num=seq_num, tool_id=0, state=is_on
                )
            case CommandType.VALVE:
                is_on: bool = arg in ('1', 'ON') if arg else ('1' in clean or 'ON' in clean)
                frame = self._frame_builder.build_tool_cmd(
                    seq_num=seq_num, tool_id=1, state=is_on
                )
            case CommandType.WAIT | CommandType.WAIT_MS:
                ms: int = 100
                for part in parts[1:]:
                    if part.isdigit():
                        ms = int(part)
                        break
                frame = self._frame_builder.build_frame(
                    msg_id=MessageId.CMD_WAIT,
                    seq_num=seq_num,
                    payload=pack('<I', ms)
                )
            case CommandType.HOME:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_HOME, seq_num=seq_num
                )
            case CommandType.ENABLE:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_ENABLE, seq_num=seq_num
                )
            case CommandType.DISABLE:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_DISABLE, seq_num=seq_num
                )
            case CommandType.HOLD:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_HOLD, seq_num=seq_num
                )
            case CommandType.RESUME:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_RESUME, seq_num=seq_num
                )
            case CommandType.ESTOP:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_ESTOP, seq_num=seq_num
                )
            case _:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_PING, seq_num=seq_num
                )

        raw_bytes: bytes = self._frame_builder.pack_frame(frame=frame)

        return Step(
            frame=frame,
            raw_bytes=raw_bytes,
            duration_us=50000,
            target_steps=(0, 0, 0, 0),
            description=f'COMMAND: {command}',
            line_number=line_num
        )
