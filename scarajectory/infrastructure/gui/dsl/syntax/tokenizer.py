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

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
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
        Pure token scanning engine parsing SCARA DSL text into token spans.

        It defines:

            :methods:
                | tokenize - Scans DSL source text into typed syntax tokens.
                | get_supported_tags - Returns tuple of supported tag names.
    '''

    _COMMANDS: frozenset[str] = frozenset(
        {cmd.value.split()[0] for cmd in ScaraCommandType}
        | {
            'CONFIG', 'ENABLE', 'DISABLE', 'SPLINE_BEGIN', 'SPLINE_END',
            'POINT'
        }
    )

    _KEYWORDS: frozenset[str] = frozenset({
        'RIGHT', 'LEFT', 'TANGENTIAL', 'FIXED', 'JOINT_LOCKED', 'FINE',
        'BLEND', 'ON', 'OFF', 'UP', 'DOWN', 'RAPID', 'WORK', 'ELBOW',
    })

    _SUPPORTED_TAGS: tuple[str, ...] = (
        'dsl_comment',
        'dsl_command',
        'dsl_keyword',
        'dsl_param',
        'dsl_number',
    )

    _RE_PARAM: Pattern[str] = re_compile(r'\b([A-Za-z_][A-Za-z0-9_]*)=')
    _RE_NUMBER: Pattern[str] = re_compile(r'\b[-+]?[0-9]*\.?[0-9]+\b')
    _RE_WORD: Pattern[str] = re_compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')

    def tokenize(self, content: str) -> tuple[SyntaxToken, ...]:
        '''
            Scans DSL source code and yields typed syntax token spans.

            :param content: DSL source code content string.
            :return: Tuple of SyntaxToken instances.
        '''
        tokens: list[SyntaxToken] = []
        lines: list[str] = content.split('\n')

        for line_idx, line in enumerate(lines, start=1):
            if not line:
                continue

            comment_start: int = line.find('#')
            code_part: str = (
                line if comment_start == -1 else line[:comment_start]
            )

            for match in self._RE_NUMBER.finditer(code_part):
                tokens.append(SyntaxToken(
                    tag='dsl_number',
                    start_idx=f'{line_idx}.{match.start()}',
                    end_idx=f'{line_idx}.{match.end()}',
                ))

            for match in self._RE_PARAM.finditer(code_part):
                tokens.append(SyntaxToken(
                    tag='dsl_param',
                    start_idx=f'{line_idx}.{match.start(1)}',
                    end_idx=f'{line_idx}.{match.end(1)}',
                ))

            for match in self._RE_WORD.finditer(code_part):
                word: str = match.group(0).upper()
                if word in self._COMMANDS:
                    tokens.append(SyntaxToken(
                        tag='dsl_command',
                        start_idx=f'{line_idx}.{match.start()}',
                        end_idx=f'{line_idx}.{match.end()}',
                    ))
                elif word in self._KEYWORDS:
                    tokens.append(SyntaxToken(
                        tag='dsl_keyword',
                        start_idx=f'{line_idx}.{match.start()}',
                        end_idx=f'{line_idx}.{match.end()}',
                    ))

            if comment_start != -1:
                tokens.append(SyntaxToken(
                    tag='dsl_comment',
                    start_idx=f'{line_idx}.{comment_start}',
                    end_idx=f'{line_idx}.{len(line)}',
                ))

        return tuple(tokens)

    def get_supported_tags(self) -> tuple[str, ...]:
        '''
            Returns tuple of supported syntax tag names.

            :return: Tuple of tag names.
        '''
        return self._SUPPORTED_TAGS
