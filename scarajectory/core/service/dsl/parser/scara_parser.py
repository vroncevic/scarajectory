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

from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.ast.program import Program
from scarajectory.core.model.dsl.token.token import Token
from scarajectory.core.model.dsl.token.token_type import TokenType
from scarajectory.core.service.dsl.ast.iprogram_factory import IProgramFactory
from scarajectory.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.parser.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraParser:
    '''
        Orchestrator parser coordinating modular command handlers into a Program AST.

        It defines:

            :attributes:
                | _lexer - Injected IScaraLexer tokenizer instance.
                | _handlers - Tuple of registered ICommandParser handlers.
            :methods:
                | __init__ - Initializes ScaraParser with injected lexer and command handlers.
                | parse - Parses raw DSL source string into a Program AST.
                | parse_tokens - Parses a sequence of lexical tokens into a Program AST.
    '''

    def __init__(
        self,
        *,
        lexer: IScaraLexer,
        handlers: Sequence[ICommandParser],
        program_factory: IProgramFactory,
    ) -> None:
        '''
            Initializes ScaraParser constructor with injected components.

            :param lexer: Injected IScaraLexer component.
            :param handlers: Sequence of custom ICommandParser handlers.
            :param program_factory: Injected IProgramFactory component.
            :exceptions: None.
        '''
        self._lexer: IScaraLexer = lexer
        self._program_factory: IProgramFactory = program_factory
        self._handlers: tuple[ICommandParser, ...] = tuple(handlers)

    def parse(self, *, source: str) -> Program:
        '''
            Parses raw SCARA DSL code string into an immutable AST program representation.

            :param source: Raw source code text.
            :return: Program instance.
            :exceptions: ValueError on syntactic parse error.
        '''
        tokens: tuple[Token, ...] = self._lexer.tokenize(source=source)
        return self.parse_tokens(tokens=tokens)

    def parse_tokens(self, *, tokens: Sequence[Token]) -> Program:
        '''
            Parses a sequence of lexical tokens into an immutable AST program representation.

            :param tokens: Sequence of Token instances.
            :return: Program instance.
            :exceptions: ValueError on syntactic parse error.
        '''
        instructions: list[Instruction] = []
        current_line_tokens: list[Token] = []

        for token in tokens:
            if token.token_type in (TokenType.NEWLINE, TokenType.EOF):
                if current_line_tokens:
                    inst = self._parse_instruction_line(
                        tokens=tuple(current_line_tokens)
                    )
                    if inst is not None:
                        instructions.append(inst)
                    current_line_tokens.clear()
            else:
                current_line_tokens.append(token)

        return self._program_factory.create(instructions=instructions)

    def _parse_instruction_line(
        self, *, tokens: tuple[Token, ...]
    ) -> Instruction | None:
        '''
            Delegates statement tokens to registered command handlers.

            :param tokens: Statement token tuple.
            :return: Instruction node or None.
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
