# -*- coding: UTF-8 -*-

'''
Module
    action.py
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
    Connection toggle button action component.
'''

from __future__ import annotations

from tkinter import LEFT, Widget
from tkinter.ttk import Button, Frame
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.connection.action.idelegate import IPortConnectionDelegate
from scarajectory.infrastructure.gui.connection.selector.iselector import IPortSelector

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortConnectionAction(Frame):
    '''
        Connect and disconnect action button component.

        It defines:

            :attributes:
                | STYLE_CONNECTED - Button style class when connected.
                | STYLE_DISCONNECTED - Button style class when disconnected.
                | TEXT_CONNECTED - Button label text when connected.
                | TEXT_DISCONNECTED - Button label text when disconnected.
                | _btn_connect - Connect and disconnect action toggle button.
                | _connection_delegate - Action delegate handling port connection toggle.
                | _selector - Injected port selector interface.
            :methods:
                | __init__ - Initializes the connection action button.
                | on_toggle_connect - Handles click event on connection toggle button.
                | set_connected_state - Updates button styling and label according to state.
                | connect_button_text - Returns text of connection toggle button.
    '''

    STYLE_CONNECTED: ClassVar[str] = 'Danger.TButton'
    STYLE_DISCONNECTED: ClassVar[str] = 'Accent.TButton'
    TEXT_CONNECTED: ClassVar[str] = 'Disconnect'
    TEXT_DISCONNECTED: ClassVar[str] = 'Connect'

    _btn_connect: Button
    _connection_delegate: IPortConnectionDelegate
    _selector: IPortSelector

    def __init__(
        self,
        parent: Widget,
        *,
        connection_delegate: IPortConnectionDelegate,
        selector: IPortSelector,
    ) -> None:
        '''
            Initializes the connection action button.

            :param parent: Parent container widget.
            :param connection_delegate: Action delegate handling port connection toggle.
            :param selector: Injected IPortSelector collaborator.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._connection_delegate: Final[IPortConnectionDelegate] = (
            connection_delegate
        )
        self._selector: Final[IPortSelector] = selector

        self._btn_connect = Button(
            self,
            text=self.TEXT_DISCONNECTED,
            style=self.STYLE_DISCONNECTED,
            command=self.on_toggle_connect,
        )
        self._btn_connect.pack(side=LEFT, padx=6)

    def on_toggle_connect(self) -> None:
        '''
            Handles click event on connection toggle button.

            :exceptions: None.
        '''
        port: str = self._selector.get_selected_port()
        self._connection_delegate.toggle_connection(port)
        self.set_connected_state(self._connection_delegate.is_connected())

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates button styling and label according to connection status.

            :param connected: True if connected, False if disconnected.
            :exceptions: None.
        '''
        if connected:
            self._selector.save_preference()
            self._btn_connect.configure(
                text=self.TEXT_CONNECTED, style=self.STYLE_CONNECTED
            )
        else:
            self._btn_connect.configure(
                text=self.TEXT_DISCONNECTED, style=self.STYLE_DISCONNECTED
            )

    @property
    def connect_button_text(self) -> str:
        '''
            Returns text of connection toggle button.

            :return: String button text.
            :exceptions: None.
        '''
        return str(self._btn_connect['text'])
