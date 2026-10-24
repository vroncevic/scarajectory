# -*- coding: UTF-8 -*-

'''
Module
    tokenizer.py
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
    Pure token scanning engine parsing SCARA DSL text into syntax token spans.
'''

from __future__ import annotations

from re import Pattern, compile as re_compile
from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.ast.tool_position import ToolPosition
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.token.pattern_kind import LexerPatternKind
from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.motor.mode import MotorDriveMode

from scarajectory.infrastructure.gui.dsl.syntax.token import SyntaxToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxTokenizer:
    '''
        Token scanning engine parsing SCARA DSL text into typed syntax tokens.

        It defines:

            :attributes:
                | TAG_COMMENT - Tag identifier for comments.
                | TAG_COMMAND - Tag identifier for primary commands.
                | TAG_KEYWORD - Tag identifier for secondary keywords.
                | TAG_PARAM - Tag identifier for named parameters.
                | TAG_NUMBER - Tag identifier for numeric literals.
                | SUPPORTED_TAGS - Tuple of all registered syntax category tags.
                | CHAR_EQUALS - Delimiter character for parameter assignments.
                | TOKEN_REGEX - Compiled regular expression matching DSL tokens.
                | COMMANDS - Frozenset of valid primary command identifiers.
                | KEYWORDS - Frozenset of valid secondary keyword identifiers.
            :methods:
                | __init__ - Initializes the syntax tokenizer instance.
                | tokenize - Scans DSL source text into typed syntax tokens.
                | get_supported_tags - Returns tuple of supported tag names.
                | get_version - Returns tokenizer component version string.
    '''

    TAG_COMMENT: ClassVar[str] = 'dsl_comment'
    TAG_COMMAND: ClassVar[str] = 'dsl_command'
    TAG_KEYWORD: ClassVar[str] = 'dsl_keyword'
    TAG_PARAM: ClassVar[str] = 'dsl_param'
    TAG_NUMBER: ClassVar[str] = 'dsl_number'
    SUPPORTED_TAGS: ClassVar[tuple[str, ...]] = (
        TAG_COMMENT,
        TAG_COMMAND,
        TAG_KEYWORD,
        TAG_PARAM,
        TAG_NUMBER,
    )
    CHAR_EQUALS: ClassVar[str] = '='

    TOKEN_REGEX: ClassVar[Pattern[str]] = re_compile(
        rf'(?P<{LexerPatternKind.COMMENT.value}>[#;].*$)|'
        rf'(?P<{LexerPatternKind.NUMBER.value}>[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)|'
        rf'(?P<{LexerPatternKind.STRING.value}>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'
        rf'(?P<{LexerPatternKind.EQUALS.value}>=)|'
        rf'(?P<{LexerPatternKind.COMMA.value}>,)|'
        rf'(?P<{LexerPatternKind.LPAREN.value}>\()|'
        rf'(?P<{LexerPatternKind.RPAREN.value}>\))|'
        rf'(?P<{LexerPatternKind.IDENTIFIER.value}>[A-Za-z_][A-Za-z0-9_]*)|'
        rf'(?P<{LexerPatternKind.WHITESPACE.value}>[^\S\n\r]+)|'
        rf'(?P<{LexerPatternKind.MISMATCH.value}>.)'
    )

    COMMANDS: ClassVar[frozenset[str]] = frozenset(
        {cmd.value for cmd in ScaraCommandType}
        | {cmd.name for cmd in ScaraCommandType}
    )

    KEYWORDS: ClassVar[frozenset[str]] = frozenset(
        {item.value for item in ElbowConfig}
        | {item.value for item in ToolOrientMode}
        | {item.value for item in ZoneMode}
        | {item.value for item in PneumaticState}
        | {item.value for item in ToolPosition}
        | {item.value for item in SpeedMode}
        | {item.value for item in MotorDriveMode}
        | {'MOTOR', 'ELBOW'}
        | {ScaraInstructionParam.ELBOW.value}
    )

    def __init__(self) -> None:
        '''
            Initializes the syntax tokenizer instance.

            :exceptions: None.
        '''

    def tokenize(self, content: str) -> tuple[SyntaxToken, ...]:
        '''
            Scans DSL source code and yields typed syntax token spans.

            :param content: DSL source code content string.
            :return: Tuple of SyntaxToken instances.
            :exceptions: None.
        '''
        tokens: list[SyntaxToken] = []
        lines: list[str] = content.split('\n')

        for line_idx, line in enumerate(lines, start=1):
            if not line:
                continue

            for match in self.TOKEN_REGEX.finditer(line):
                if match.lastgroup is None:
                    continue

                pattern_kind: LexerPatternKind = LexerPatternKind(match.lastgroup)
                start: int = match.start()
                end: int = match.end()
                tag: str

                match pattern_kind:
                    case LexerPatternKind.COMMENT:
                        tag = self.TAG_COMMENT
                    case LexerPatternKind.NUMBER:
                        tag = self.TAG_NUMBER
                    case LexerPatternKind.IDENTIFIER:
                        val: str = match.group()

                        if end < len(line) and line[end] == self.CHAR_EQUALS:
                            tag = self.TAG_PARAM
                        elif val.upper() in self.COMMANDS:
                            tag = self.TAG_COMMAND
                        elif val.upper() in self.KEYWORDS:
                            tag = self.TAG_KEYWORD
                        else:
                            continue
                    case _:
                        continue

                tokens.append(SyntaxToken(
                    tag=tag,
                    start_idx=f'{line_idx}.{start}',
                    end_idx=f'{line_idx}.{end}',
                ))

        return tuple(tokens)

    def get_supported_tags(self) -> tuple[str, ...]:
        '''
            Returns sequence of supported syntax tag categories.

            :return: Tuple of tag category name strings.
            :exceptions: None.
        '''
        return self.SUPPORTED_TAGS

    def get_version(self) -> str:
        '''
            Returns tokenizer component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
