# -*- coding: UTF-8 -*-

'''
Module
    console_view.py
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
    Status and compiler diagnostics console view component for SCARA DSL.
'''

from __future__ import annotations

from tkinter import BOTH, DISABLED, END, NORMAL, Text, Widget
from tkinter.ttk import LabelFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslConsoleView(LabelFrame):
    '''
        Compiler diagnostic log console displaying multi-level formatted messages.

        It defines:

            :attributes:
                | _txt_console - Read-only Text console widget.
            :methods:
                | __init__ - Initializes console layout and text buffer.
                | append_log - Appends message string with syntax-colored level tag.
                | log - Backward-compatible log call delegating to append_log.
                | clear - Clears the console output.
                | get_text - Returns current console buffer content.
    '''

    _txt_console: Text

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes console layout and text buffer.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, text=' Compilation & Diagnostics ', padding=2)

        self._txt_console = Text(
            self,
            width=1,
            height=5,
            bg='#1a1d23',
            fg='#abb2bf',
            font=('DejaVu Sans Mono', 8),
            wrap='word',
            state=DISABLED,
        )
        self._txt_console.pack(fill=BOTH, expand=True)

        self._txt_console.tag_config('info', foreground='#61afef')
        self._txt_console.tag_config('success', foreground='#98c379')
        self._txt_console.tag_config('warning', foreground='#e5c07b')
        self._txt_console.tag_config('error', foreground='#e06c75')
        self._txt_console.tag_config('neutral', foreground='#abb2bf')

    def append_log(self, text: str, level: str = 'info') -> None:
        '''
            Appends message string with syntax-colored level tag and auto-scrolls.

            :param text: Message string to log.
            :param level: Severity level tag ('info', 'success', 'warning', 'error', 'neutral').
            :exceptions: None.
        '''
        valid_tags: tuple[str, ...] = ('info', 'success', 'warning', 'error', 'neutral')
        tag: str = level if level in valid_tags else 'info'
        self._txt_console.config(state=NORMAL)
        self._txt_console.insert(END, f'{text}\n', tag)
        self._txt_console.see(END)
        self._txt_console.config(state=DISABLED)

    def log(self, text: str, is_error: bool = False) -> None:
        '''
            Logs message string with success or error color formatting.

            :param text: Message string.
            :param is_error: True if message indicates failure.
            :exceptions: None.
        '''
        level: str = 'error' if is_error else 'success'
        self.append_log(text=text, level=level)

    def clear(self) -> None:
        '''
            Clears the console output.

            :exceptions: None.
        '''
        self._txt_console.config(state=NORMAL)
        self._txt_console.delete('1.0', END)
        self._txt_console.config(state=DISABLED)

    def get_text(self) -> str:
        '''
            Returns current console buffer content.

            :return: String content of the console buffer.
            :exceptions: None.
        '''
        return self._txt_console.get('1.0', END).strip()
