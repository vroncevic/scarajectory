# -*- coding: UTF-8 -*-

'''
Module
    raw_command_panel.py
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
    Raw micro-command entry and transmission subcomponent for manual jog controls.
'''

from __future__ import annotations

from tkinter import END, LEFT, Widget, X
from tkinter.ttk import Button, Entry, Frame, Label
from typing import Final

from scarajectory.core.service.connection.iraw_channel import IRawChannel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogRawCommandPanel(Frame):
    '''
        Panel providing raw ASCII command input and transmission over the communication channel.

        It defines:

            :attributes:
                | _raw_channel - Injected raw communication transport channel.
                | _entry_raw - Text entry widget for command string input.
            :methods:
                | __init__ - Initializes the command text entry and send button.
                | send_raw - Transmits text command from entry field over raw channel.
                | get_command - Returns current text from the command entry buffer.
                | clear_command - Clears the command entry text buffer.
                | set_command - Sets the text into the command entry buffer.
    '''

    _raw_channel: IRawChannel
    _entry_raw: Entry

    def __init__(
        self,
        parent: Widget,
        *,
        raw_channel: IRawChannel,
    ) -> None:
        '''
            Initializes the command text entry and send button.

            :param parent: Parent container widget.
            :param raw_channel: Injected IRawChannel collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._raw_channel: Final[IRawChannel] = raw_channel

        Label(self, text='Raw:').pack(side=LEFT)
        self._entry_raw = Entry(self, width=20)
        self._entry_raw.pack(side=LEFT, fill=X, expand=True, padx=2)
        self._entry_raw.bind('<Return>', lambda _e: self.send_raw())
        Button(self, text='Send', command=self.send_raw).pack(side=LEFT)

    def send_raw(self) -> None:
        '''
            Transmits raw command from text input to microcontroller.

            :exceptions: None.
        '''
        cmd: str = self.get_command().strip()

        if cmd:
            self._raw_channel.send_raw_command(cmd)
            self.clear_command()

    def get_command(self) -> str:
        '''
            Returns current text from the command entry buffer.

            :return: String command from entry buffer.
            :exceptions: None.
        '''
        return self._entry_raw.get()

    def clear_command(self) -> None:
        '''
            Clears the command entry text buffer.

            :exceptions: None.
        '''
        self._entry_raw.delete(0, END)

    def set_command(self, cmd: str) -> None:
        '''
            Sets the command entry text buffer.

            :param cmd: Command string to insert into entry buffer.
            :exceptions: None.
        '''
        self.clear_command()
        self._entry_raw.insert(0, cmd)
