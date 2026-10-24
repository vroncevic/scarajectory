# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Serial port selection and connection management panel component.
'''

from __future__ import annotations

from tkinter import LEFT, Widget
from tkinter.ttk import Frame
from typing import Final

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scarajectory.infrastructure.gui.connection.action.action import PortConnectionAction
from scarajectory.infrastructure.gui.connection.action.iaction import IPortConnectionAction
from scarajectory.infrastructure.gui.connection.action.idelegate import IPortConnectionDelegate
from scarajectory.infrastructure.gui.connection.selector.iselector import IPortSelector
from scarajectory.infrastructure.gui.connection.selector.selector import PortSelector

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortConnectionPanel(Frame):
    '''
        Serial port scanning and connection control panel.

        It defines:

            :attributes:
                | _selector - Injected port selector component.
                | _action - Injected connection action button component.
            :methods:
                | __init__ - Initializes the port connection controls layout.
                | on_toggle_connect - Handles click event on connection toggle button.
                | refresh_ports - Scans available serial/USB ports on the host.
                | get_selected_port - Returns the currently selected port identifier.
                | set_connected_state - Updates button styling and label according to connection.
                | connect_button_text - Returns text of connection toggle button.
    '''

    _selector: IPortSelector
    _action: IPortConnectionAction

    def __init__(
        self,
        parent: Widget,
        *,
        connection_repository: ISerialPreferenceRepository,
        connection_delegate: IPortConnectionDelegate,
    ) -> None:
        '''
            Initializes the port connection controls layout.

            :param parent: Parent container widget.
            :param connection_repository: Injected ISerialPreferenceRepository instance.
            :param connection_delegate: Action delegate handling port connection toggle.
            :exceptions: None.
        '''
        super().__init__(parent)
        selector: PortSelector = PortSelector(
            self,
            connection_repository=connection_repository,
        )
        selector.pack(side=LEFT)
        self._selector: Final[IPortSelector] = selector

        action: PortConnectionAction = PortConnectionAction(
            self,
            connection_delegate=connection_delegate,
            selector=selector,
        )
        action.pack(side=LEFT)
        self._action: Final[IPortConnectionAction] = action

    def on_toggle_connect(self) -> None:
        '''
            Handles click event on connection toggle button.

            :exceptions: None.
        '''
        self._action.on_toggle_connect()

    def refresh_ports(self) -> None:
        '''
            Scans available serial/USB ports on the host system and restores preference.

            :exceptions: None.
        '''
        self._selector.refresh_ports()

    def get_selected_port(self) -> str:
        '''
            Returns the currently selected port identifier string.

            :return: Clean port identifier string.
            :exceptions: None.
        '''
        return self._selector.get_selected_port()

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates button styling and label according to connection status.

            :param connected: True if connected, False if disconnected.
            :exceptions: None.
        '''
        self._action.set_connected_state(connected)

    @property
    def connect_button_text(self) -> str:
        '''
            Returns text of connection toggle button.

            :return: String button text.
            :exceptions: None.
        '''
        return self._action.connect_button_text
