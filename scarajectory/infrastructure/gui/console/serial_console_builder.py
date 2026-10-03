# -*- coding: UTF-8 -*-

'''
Module
    serial_console_builder.py
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
    Widget builder component for SerialConsole terminal log view and controls.
'''

from __future__ import annotations

from tkinter import BOTH, RIGHT, Text, X
from tkinter.ttk import Button, Frame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scarajectory.infrastructure.gui.console.serial_console import SerialConsole

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialConsoleBuilder:
    '''
        Builds toolbar buttons and scrollable text display for SerialConsole.

        It defines:

            :methods:
                | build_widgets - Builds scrollable log text area and action buttons.
    '''

    @classmethod
    def build_widgets(cls, console: SerialConsole) -> Text:
        '''
            Builds scrollable log text area and clear button.

            :param console: Parent SerialConsole widget container.
            :return: Created Text widget.
            :exceptions: None.
        '''
        top: Frame = Frame(console)
        top.pack(fill=X, pady=(0, 2))
        Button(top, text='Clear Log', command=console.clear_log).pack(side=RIGHT, padx=(4, 0))
        Button(top, text='Copy', command=console.copy_log).pack(side=RIGHT, padx=(4, 0))
        Button(top, text='Select All', command=console.select_all).pack(side=RIGHT, padx=(4, 0))

        txt_log = Text(
            console,
            height=6,
            bg='#14161a',
            fg='#abb2bf',
            font=('DejaVu Sans Mono', 8),
            wrap='none'
        )
        txt_log.pack(fill=BOTH, expand=True)

        txt_log.bind('<Control-a>', lambda e: (console.select_all(), 'break')[1])
        txt_log.bind('<Control-c>', lambda e: (console.copy_log(), 'break')[1])

        txt_log.tag_config('tx', foreground='#61afef')
        txt_log.tag_config('rx', foreground='#98c379')
        txt_log.tag_config('err', foreground='#e06c75')

        return txt_log
