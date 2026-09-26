# -*- coding: UTF-8 -*-

'''
Module
    token_type.py
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
    Defines TokenType enumeration representing lexical tokens of the SCARA DSL.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class TokenType(StrEnum):
    '''
        Lexical token types of the SCARA Domain-Specific Language (DSL).

        It defines:

        :attributes:
            | KEYWORD - Command keyword.
            | IDENTIFIER - Variable, parameter name, or identifier.
            | NUMBER - Numeric literal (integer or floating-point).
            | STRING - String literal.
            | EQUALS - Assignment or key-value delimiter ('=').
            | COMMA - Argument separator (',').
            | LPAREN - Opening parenthesis ('(').
            | RPAREN - Closing parenthesis (')').
            | COMMENT - Comment text ('#').
            | NEWLINE - End-of-line marker.
            | EOF - End-of-input marker.
    '''

    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    EQUALS = 'EQUALS'
    COMMA = 'COMMA'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    COMMENT = 'COMMENT'
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'
