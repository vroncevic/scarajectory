# -*- coding: UTF-8 -*-

'''
Module
    serial_console.py
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
    Dedicated Tkinter serial terminal console output with color syntax tagging.
'''

from __future__ import annotations

from datetime import datetime
from tkinter import END, INSERT, SEL, SEL_FIRST, SEL_LAST, TclError, Text, Widget
from tkinter.ttk import LabelFrame

from scarajectory.infrastructure.gui.console.serial_console_builder import SerialConsoleBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialConsole(LabelFrame):
    '''
        Serial terminal console component providing colorized log output and scrolling.

        It defines:

            :attributes:
                | _txt_log - Text widget rendering log stream.
            :methods:
                | __init__ - Initializes console panel and text widget.
                | append_log - Appends timestamped log message with syntax coloring.
                | select_all - Selects all text content in the log text area.
                | copy_log - Copies selected or entire log content to system clipboard.
                | clear_log - Clears console contents.
    '''

    _txt_log: Text

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes console panel and text widget.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text=' [ Serial Terminal / Microcontroller Log ] ',
            padding=4,
        )
        self._txt_log = SerialConsoleBuilder.build_widgets(self)

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends timestamped log message with syntax coloring.

            :param text: Message string to append.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        tag: str = 'tx' if is_outgoing else ('err' if 'ERR' in text.upper() else 'rx')
        prefix: str = '>>> TX' if is_outgoing else '<<< RX'
        self._txt_log.insert(END, f'[{ts}] {prefix}: {text}\n', tag)
        self._txt_log.see(END)

    def select_all(self) -> None:
        '''
            Selects all text content in the log text area.

            :exceptions: None.
        '''
        self._txt_log.tag_add(SEL, '1.0', END)
        self._txt_log.mark_set(INSERT, '1.0')
        self._txt_log.see(INSERT)
        self._txt_log.focus_set()

    def copy_log(self) -> None:
        '''
            Copies selected or entire log content to system clipboard.

            :exceptions: None.
        '''
        try:
            content: str = self._txt_log.get(SEL_FIRST, SEL_LAST)

        except TclError:
            content = self._txt_log.get('1.0', END).strip()

        if content:
            self.clipboard_clear()
            self.clipboard_append(content)

    def clear_log(self) -> None:
        '''
            Clears console contents.

            :exceptions: None.
        '''
        self._txt_log.delete('1.0', END)
