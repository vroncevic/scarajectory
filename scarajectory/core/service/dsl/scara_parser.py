# -*- coding: UTF-8 -*-

'''
Module
    scara_parser.py
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
    Implementation of IScaraParser orchestrating modular command parser handlers into an AST program.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.model.dsl.iscara_program import IScaraProgram
from scarajectory.core.model.dsl.scara_program import ScaraProgram
from scarajectory.core.model.dsl.scara_token import ScaraToken
from scarajectory.core.model.dsl.scara_token_type import ScaraTokenType
from scarajectory.core.service.dsl.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.parser.approach_retract_parser import ApproachRetractParser
from scarajectory.core.service.dsl.parser.arc_command_parser import ArcCommandParser
from scarajectory.core.service.dsl.parser.config_command_parser import ConfigCommandParser
from scarajectory.core.service.dsl.parser.flow_command_parser import FlowCommandParser
from scarajectory.core.service.dsl.parser.frame_command_parser import FrameCommandParser
from scarajectory.core.service.dsl.parser.icommand_parser import ICommandParser
from scarajectory.core.service.dsl.parser.jog_command_parser import JogCommandParser
from scarajectory.core.service.dsl.parser.jump_command_parser import JumpCommandParser
from scarajectory.core.service.dsl.parser.motion_command_parser import MotionCommandParser
from scarajectory.core.service.dsl.parser.pallet_command_parser import PalletCommandParser
from scarajectory.core.service.dsl.parser.probe_command_parser import ProbeCommandParser
from scarajectory.core.service.dsl.parser.tool_command_parser import ToolCommandParser
from scarajectory.core.service.dsl.parser.tool_orient_command_parser import ToolOrientCommandParser
from scarajectory.core.service.dsl.parser.zone_command_parser import ZoneCommandParser
from scarajectory.core.service.dsl.scara_lexer import ScaraLexer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraParser:
    '''
        Orchestrator parser coordinating modular command handlers into a ScaraProgram AST.

        It defines:

            :attributes:
                | _lexer - Injected IScaraLexer tokenizer instance.
                | _handlers - Tuple of registered ICommandParser handlers.
            :methods:
                | __init__ - Initializes ScaraParser with optional lexer and command handlers.
                | parse - Parses raw DSL source string into an IScaraProgram AST.
                | parse_tokens - Parses a sequence of lexical tokens into an IScaraProgram AST.
    '''

    def __init__(
        self,
        *,
        lexer: IScaraLexer | None = None,
        handlers: Sequence[ICommandParser] | None = None,
    ) -> None:
        '''
            Initializes ScaraParser constructor with injected components.

            :param lexer: Optional injected IScaraLexer component.
            :param handlers: Optional sequence of custom ICommandParser handlers.
            :exceptions: None.
        '''
        self._lexer: IScaraLexer = lexer if lexer is not None else ScaraLexer()
        if handlers is not None:
            self._handlers: tuple[ICommandParser, ...] = tuple(handlers)
        else:
            self._handlers = (
                MotionCommandParser(),
                JumpCommandParser(),
                ArcCommandParser(),
                ApproachRetractParser(),
                ConfigCommandParser(),
                PalletCommandParser(),
                FrameCommandParser(),
                ToolCommandParser(),
                FlowCommandParser(),
                JogCommandParser(),
                ProbeCommandParser(),
                ZoneCommandParser(),
                ToolOrientCommandParser(),
            )

    def parse(self, *, source: str) -> IScaraProgram:
        '''
            Parses raw SCARA DSL code string into an immutable AST program representation.

            :param source: Raw source code text.
            :return: IScaraProgram instance.
            :exceptions: ValueError on syntactic parse error.
        '''
        tokens: tuple[ScaraToken, ...] = self._lexer.tokenize(source=source)
        return self.parse_tokens(tokens=tokens)

    def parse_tokens(self, *, tokens: Sequence[ScaraToken]) -> IScaraProgram:
        '''
            Parses a sequence of lexical tokens into an immutable AST program representation.

            :param tokens: Sequence of ScaraToken instances.
            :return: IScaraProgram instance.
            :exceptions: ValueError on syntactic parse error.
        '''
        instructions: list[IScaraInstruction] = []
        current_line_tokens: list[ScaraToken] = []

        for token in tokens:
            if token.token_type in (ScaraTokenType.NEWLINE, ScaraTokenType.EOF):
                if current_line_tokens:
                    inst = self._parse_instruction_line(
                        tokens=tuple(current_line_tokens)
                    )
                    if inst is not None:
                        instructions.append(inst)
                    current_line_tokens.clear()
            else:
                current_line_tokens.append(token)

        return ScaraProgram.from_instructions(instructions)

    def _parse_instruction_line(
        self, *, tokens: tuple[ScaraToken, ...]
    ) -> IScaraInstruction | None:
        '''
            Delegates statement tokens to registered command handlers.

            :param tokens: Statement token tuple.
            :return: IScaraInstruction node or None.
            :exceptions: ValueError if no registered handler recognizes the command.
        '''
        if not tokens:
            return None

        first_tok = tokens[0]
        cmd_name = first_tok.value.upper()
        line_num = first_tok.line
        raw_text = ' '.join(t.value for t in tokens)

        for handler in self._handlers:
            if handler.can_parse(command_name=cmd_name):
                return handler.parse(
                    tokens=tokens, line_num=line_num, raw_text=raw_text
                )

        raise ValueError(
            f'Unknown SCARA DSL command {cmd_name!r} at line {line_num}'
        )
