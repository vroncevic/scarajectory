# -*- coding: UTF-8 -*-

'''
Module
    console.py
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
from typing import ClassVar

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
                | TITLE_FRAME - Header label for console frame.
                | PADDING_FRAME - Outer padding for frame container.
                | COLOR_BG - Console background hex color.
                | COLOR_FG - Default text foreground hex color.
                | FONT_FAMILY - Monospace font family name.
                | FONT_SIZE - Font size in points.
                | TAG_INFO - Diagnostic info tag name.
                | TAG_SUCCESS - Operation success tag name.
                | TAG_WARNING - Warning severity tag name.
                | TAG_ERROR - Error severity tag name.
                | TAG_NEUTRAL - Neutral severity tag name.
                | COLOR_INFO - Info text foreground color.
                | COLOR_SUCCESS - Success text foreground color.
                | COLOR_WARNING - Warning text foreground color.
                | COLOR_ERROR - Error text foreground color.
                | COLOR_NEUTRAL - Neutral text foreground color.
                | VALID_TAGS - Tuple of allowed diagnostic severity tags.
                | _txt_console - Read-only Text console widget.
            :methods:
                | __init__ - Initializes console layout and text buffer.
                | append_log - Appends message string with syntax-colored level tag.
                | log - Logs message string with success or error color formatting.
                | clear - Clears the console output buffer.
                | get_text - Returns current console buffer content.
                | get_version - Returns console component version string.
    '''

    TITLE_FRAME: ClassVar[str] = ' Compilation & Diagnostics '
    PADDING_FRAME: ClassVar[int] = 2
    COLOR_BG: ClassVar[str] = '#1a1d23'
    COLOR_FG: ClassVar[str] = '#abb2bf'
    FONT_FAMILY: ClassVar[str] = 'DejaVu Sans Mono'
    FONT_SIZE: ClassVar[int] = 8

    TAG_INFO: ClassVar[str] = 'info'
    TAG_SUCCESS: ClassVar[str] = 'success'
    TAG_WARNING: ClassVar[str] = 'warning'
    TAG_ERROR: ClassVar[str] = 'error'
    TAG_NEUTRAL: ClassVar[str] = 'neutral'

    COLOR_INFO: ClassVar[str] = '#61afef'
    COLOR_SUCCESS: ClassVar[str] = '#98c379'
    COLOR_WARNING: ClassVar[str] = '#e5c07b'
    COLOR_ERROR: ClassVar[str] = '#e06c75'
    COLOR_NEUTRAL: ClassVar[str] = '#abb2bf'

    VALID_TAGS: ClassVar[tuple[str, ...]] = (
        TAG_INFO,
        TAG_SUCCESS,
        TAG_WARNING,
        TAG_ERROR,
        TAG_NEUTRAL,
    )

    _txt_console: Text

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes console layout and text buffer.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, text=self.TITLE_FRAME, padding=self.PADDING_FRAME)

        self._txt_console = Text(
            self,
            width=1,
            height=5,
            bg=self.COLOR_BG,
            fg=self.COLOR_FG,
            font=(self.FONT_FAMILY, self.FONT_SIZE),
            wrap='word',
            state=DISABLED,
        )
        self._txt_console.pack(fill=BOTH, expand=True)

        self._txt_console.tag_config(self.TAG_INFO, foreground=self.COLOR_INFO)
        self._txt_console.tag_config(self.TAG_SUCCESS, foreground=self.COLOR_SUCCESS)
        self._txt_console.tag_config(self.TAG_WARNING, foreground=self.COLOR_WARNING)
        self._txt_console.tag_config(self.TAG_ERROR, foreground=self.COLOR_ERROR)
        self._txt_console.tag_config(self.TAG_NEUTRAL, foreground=self.COLOR_NEUTRAL)

    def append_log(self, text: str, level: str = 'info') -> None:
        '''
            Appends message string with syntax-colored level tag and auto-scrolls.

            :param text: Message string to log.
            :param level: Severity level tag ('info', 'success', 'warning', 'error', 'neutral').
            :exceptions: None.
        '''
        tag: str = level if level in self.VALID_TAGS else self.TAG_INFO
        self._txt_console.config(state=NORMAL)
        self._txt_console.insert(END, f'{text}\n', tag)
        self._txt_console.see(END)
        self._txt_console.config(state=DISABLED)

    def log(self, text: str, is_error: bool = False) -> None:
        '''
            Logs message string with success or error color formatting.

            :param text: Message string to log.
            :param is_error: When True, logs in error style; otherwise in success style.
            :exceptions: None.
        '''
        level: str = self.TAG_ERROR if is_error else self.TAG_SUCCESS
        self.append_log(text, level=level)

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

            :return: Console log text.
            :exceptions: None.
        '''
        return self._txt_console.get('1.0', END)

    def get_version(self) -> str:
        '''
            Returns console component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
