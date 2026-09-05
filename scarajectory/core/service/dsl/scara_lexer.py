# -*- coding: UTF-8 -*-

'''
Module
    scara_lexer.py
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
    Implementation of IScaraLexer converting SCARA DSL source text into atomic tokens.
'''

from __future__ import annotations

from re import compile as re_compile, Pattern
from typing import ClassVar

from scarajectory.core.model.dsl.scara_token import ScaraToken
from scarajectory.core.model.dsl.scara_token_type import ScaraTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraLexer:
    '''
        Concrete lexer implementation converting SCARA DSL text into stream of tokens.

        It defines:

            :attributes:
                | _TOKEN_REGEX - Compiled regular expression pattern matching DSL lexical entities.
            :methods:
                | tokenize - Tokenizes raw source code into an immutable tuple of lexical tokens.
    '''

    _TOKEN_REGEX: ClassVar[Pattern[str]] = re_compile(
        r'(?P<COMMENT>[#;].*$)|'
        r'(?P<NUMBER>[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)|'
        r'(?P<STRING>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'
        r'(?P<EQUALS>=)|'
        r'(?P<COMMA>,)|'
        r'(?P<LPAREN>\()|'
        r'(?P<RPAREN>\))|'
        r'(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)|'
        r'(?P<WHITESPACE>[^\S\n\r]+)|'
        r'(?P<MISMATCH>.)'
    )

    def tokenize(self, *, source: str) -> tuple[ScaraToken, ...]:
        '''
            Tokenizes source text into a tuple of ScaraToken instances.

            :param source: Raw source code string.
            :return: Immutable tuple of ScaraToken tokens.
            :exceptions: ValueError if an illegal/unrecognized character is encountered.
        '''
        tokens: list[ScaraToken] = []
        lines: list[str] = source.splitlines()

        for line_idx, line in enumerate(lines, start=1):
            col = 1
            line_has_tokens = False

            for match in self._TOKEN_REGEX.finditer(line):
                kind = match.lastgroup
                val = match.group()
                col = match.start() + 1

                if kind == 'WHITESPACE' or kind == 'COMMENT':
                    continue
                if kind == 'MISMATCH':
                    raise ValueError(
                        f'Syntax error: Unexpected character {val!r} at line {line_idx}, column {col}'
                    )

                token_type = ScaraTokenType.IDENTIFIER
                match kind:
                    case 'NUMBER':
                        token_type = ScaraTokenType.NUMBER
                    case 'STRING':
                        token_type = ScaraTokenType.STRING
                    case 'EQUALS':
                        token_type = ScaraTokenType.EQUALS
                    case 'COMMA':
                        token_type = ScaraTokenType.COMMA
                    case 'LPAREN':
                        token_type = ScaraTokenType.LPAREN
                    case 'RPAREN':
                        token_type = ScaraTokenType.RPAREN
                    case _:
                        token_type = ScaraTokenType.IDENTIFIER

                tokens.append(
                    ScaraToken(
                        token_type=token_type,
                        value=val,
                        line=line_idx,
                        column=col,
                    )
                )
                line_has_tokens = True

            if line_has_tokens:
                tokens.append(
                    ScaraToken(
                        token_type=ScaraTokenType.NEWLINE,
                        value='\n',
                        line=line_idx,
                        column=len(line) + 1,
                    )
                )

        tokens.append(
            ScaraToken(
                token_type=ScaraTokenType.EOF,
                value='',
                line=len(lines) + 1,
                column=1,
            )
        )
        return tuple(tokens)
