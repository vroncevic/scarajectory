# -*- coding: UTF-8 -*-

'''
Module
    dsl_syntax_highlighter.py
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
    Syntax highlighter component applying color styles to SCARA DSL source text in Tkinter Text.
'''

from __future__ import annotations

from re import compile as re_compile, Pattern
from tkinter import END, Text

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxHighlighter:
    '''
        Syntax highlighting engine applying color tags to SCARA DSL source code.

        It defines:

            :attributes:
                | _commands - Set of recognized DSL command words.
                | _keywords - Set of recognized secondary keyword values.
                | _re_comment - Compiled regex for comments.
                | _re_param - Compiled regex for key=value parameters.
                | _re_number - Compiled regex for numerical constants.
                | _re_word - Compiled regex for general word identifiers.
            :methods:
                | __init__ - Configures style tags on the target text widget.
                | highlight - Performs complete syntax color update on text widget.
    '''

    _commands: frozenset[str] = frozenset({
        'MOVE_L', 'MOVE_J', 'HOME', 'JUMP', 'ARC_CW', 'ARC_CCW',
        'SPLINE_BEGIN', 'SPLINE_END', 'POINT', 'SPEED', 'ACCEL', 'OVERRIDE',
        'FRAME_SET', 'FRAME_RESET', 'PALLET_DEF', 'MOVE_PALLET', 'PROBE',
        'TOOL', 'PUMP', 'VALVE', 'WAIT_MS', 'SYNC', 'HOLD', 'RESUME',
        'ESTOP', 'ZONE', 'TOOL_ORIENT', 'APPROACH', 'RETRACT', 'JOG_AXIS',
        'JOG_JOINT', 'CONFIG', 'ENABLE', 'DISABLE',
    })

    _keywords: frozenset[str] = frozenset({
        'RIGHT', 'LEFT', 'TANGENTIAL', 'FIXED', 'JOINT_LOCKED', 'FINE',
        'BLEND', 'ON', 'OFF', 'UP', 'DOWN', 'RAPID', 'WORK', 'ELBOW',
    })

    _re_comment: Pattern[str] = re_compile(r'#.*$')
    _re_param: Pattern[str] = re_compile(r'\b([A-Za-z_][A-Za-z0-9_]*)=')
    _re_number: Pattern[str] = re_compile(r'\b[-+]?[0-9]*\.?[0-9]+\b')
    _re_word: Pattern[str] = re_compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')

    def __init__(self, text_widget: Text) -> None:
        '''
            Configures syntax color tags on the target Tkinter Text widget.

            :param text_widget: Target text widget to format.
            :exceptions: None.
        '''
        text_widget.tag_configure('dsl_comment', foreground='#5c6370', font=('DejaVu Sans Mono', 9, 'italic'))
        text_widget.tag_configure('dsl_command', foreground='#61afef', font=('DejaVu Sans Mono', 9, 'bold'))
        text_widget.tag_configure('dsl_keyword', foreground='#c678dd', font=('DejaVu Sans Mono', 9, 'bold'))
        text_widget.tag_configure('dsl_param', foreground='#e5c07b', font=('DejaVu Sans Mono', 9))
        text_widget.tag_configure('dsl_number', foreground='#98c379', font=('DejaVu Sans Mono', 9))

    def highlight(self, text_widget: Text) -> None:
        '''
            Performs complete syntax color update on text widget contents.

            :param text_widget: Target text widget.
            :exceptions: None.
        '''
        content: str = text_widget.get('1.0', END)
        for tag in ('dsl_comment', 'dsl_command', 'dsl_keyword', 'dsl_param', 'dsl_number'):
            text_widget.tag_remove(tag, '1.0', END)

        lines: list[str] = content.split('\n')
        for line_idx, line in enumerate(lines, start=1):
            if not line:
                continue

            comment_start = line.find('#')
            code_part = line if comment_start == -1 else line[:comment_start]

            # Highlight numbers in code
            for match in self._re_number.finditer(code_part):
                start = f'{line_idx}.{match.start()}'
                end = f'{line_idx}.{match.end()}'
                text_widget.tag_add('dsl_number', start, end)

            # Highlight parameters (e.g. X=, SPEED=)
            for match in self._re_param.finditer(code_part):
                start = f'{line_idx}.{match.start(1)}'
                end = f'{line_idx}.{match.end(1)}'
                text_widget.tag_add('dsl_param', start, end)

            # Highlight commands and keywords
            for match in self._re_word.finditer(code_part):
                word = match.group(0).upper()
                start = f'{line_idx}.{match.start()}'
                end = f'{line_idx}.{match.end()}'
                if word in self._commands:
                    text_widget.tag_add('dsl_command', start, end)
                elif word in self._keywords:
                    text_widget.tag_add('dsl_keyword', start, end)

            # Highlight comment
            if comment_start != -1:
                start = f'{line_idx}.{comment_start}'
                end = f'{line_idx}.{len(line)}'
                text_widget.tag_add('dsl_comment', start, end)
