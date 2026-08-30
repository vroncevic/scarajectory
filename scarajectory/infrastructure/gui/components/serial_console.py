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

import datetime
import tkinter as tk
from tkinter import ttk

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialConsole(ttk.LabelFrame):
    '''
        Serial terminal console component providing colorized log output and scrolling.

        It defines:

            :attributes:
                | _txt_log - Text widget rendering log stream.
            :methods:
                | __init__ - Initializes console panel and text widget.
                | append_log - Appends timestamped log message with syntax coloring.
                | clear_log - Clears console contents.
    '''

    _txt_log: tk.Text

    def __init__(self, parent: tk.Widget, **kwargs: object) -> None:
        '''
            Initializes console panel and text widget.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, text=' [ Serial Terminal / Microcontroller Log ] ', padding=4, **kwargs)
        self._create_widgets()

    def _create_widgets(self) -> None:
        '''
            Builds scrollable log text area and clear button.

            :exceptions: None.
        '''
        top = ttk.Frame(self)
        top.pack(fill=tk.X, pady=(0, 2))
        ttk.Button(top, text='Clear Log', command=self.clear_log).pack(side=tk.RIGHT)

        self._txt_log = tk.Text(
            self,
            height=6,
            bg='#14161a',
            fg='#abb2bf',
            font=('DejaVu Sans Mono', 8),
            wrap='none'
        )
        self._txt_log.pack(fill=tk.BOTH, expand=True)

        self._txt_log.tag_config('tx', foreground='#61afef')
        self._txt_log.tag_config('rx', foreground='#98c379')
        self._txt_log.tag_config('err', foreground='#e06c75')

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends timestamped log message with syntax coloring.

            :param text: Message string to append.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        ts: str = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        tag: str = 'tx' if is_outgoing else ('err' if 'ERR' in text.upper() else 'rx')
        prefix: str = '>>> TX' if is_outgoing else '<<< RX'
        self._txt_log.insert(tk.END, f'[{ts}] {prefix}: {text}\n', tag)
        self._txt_log.see(tk.END)

    def clear_log(self) -> None:
        '''
            Clears console contents.

            :exceptions: None.
        '''
        self._txt_log.delete('1.0', tk.END)
