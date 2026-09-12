# -*- coding: UTF-8 -*-

'''
Module
    dsl_console_view.py
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

from tkinter import BOTH, DISABLED, END, NORMAL, Widget, Text
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
        Compiler diagnostic log console displaying formatted success and error messages.

        It defines:

            :attributes:
                | _txt_console - Read-only Text console widget.
            :methods:
                | __init__ - Initializes console layout and text buffer.
                | log - Logs message string with success/error color formatting.
                | clear - Clears the console output.
    '''

    _txt_console: Text

    def __init__(self, parent: Widget, **kwargs: object) -> None:
        '''
            Initializes console layout and text buffer.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, text=' Compilation & Diagnostics ', padding=2, **kwargs)

        self._txt_console = Text(
            self,
            width=1,
            height=4,
            bg='#1a1d23',
            fg='#98c379',
            font=('DejaVu Sans Mono', 8),
            wrap='word',
            state=DISABLED,
        )
        self._txt_console.pack(fill=BOTH, expand=True)

    def log(self, text: str, is_error: bool = False) -> None:
        '''
            Logs message string with success or error color formatting.

            :param text: Message string.
            :param is_error: True if message indicates failure.
            :exceptions: None.
        '''
        self._txt_console.config(state=NORMAL)
        self._txt_console.delete('1.0', END)
        self._txt_console.config(fg='#e06c75' if is_error else '#98c379')
        self._txt_console.insert(END, text)
        self._txt_console.config(state=DISABLED)

    def clear(self) -> None:
        '''
            Clears the console output.

            :exceptions: None.
        '''
        self._txt_console.config(state=NORMAL)
        self._txt_console.delete('1.0', END)
        self._txt_console.config(state=DISABLED)
