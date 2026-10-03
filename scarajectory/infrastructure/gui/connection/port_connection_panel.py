# -*- coding: UTF-8 -*-

'''
Module
    port_connection_panel.py
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
from tkinter.ttk import Button, Combobox, Frame, Label
from typing import Final

from scarajectory.core.model.preferences.connection_preference import ConnectionPreference
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.infrastructure.transport.driver.serial_port_scanner import SerialPortScanner
from scarajectory.infrastructure.gui.connection.null_port_connection_delegate import NullPortConnectionDelegate
from scarajectory.infrastructure.gui.connection.iport_connection_delegate import IPortConnectionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

NULL_CONNECTION_DELEGATE: Final[IPortConnectionDelegate] = NullPortConnectionDelegate()


class PortConnectionPanel(Frame):
    '''
        Serial port scanning and connection control panel.

        It defines:

            :attributes:
                | _cbo_ports - Dropdown list of detected serial communication ports.
                | _btn_connect - Connect and disconnect action toggle button.
                | _connection_delegate - Action delegate handling port connection toggle.
                | _connection_repository - Injected hardware connection preferences repository.
            :methods:
                | __init__ - Initializes the port connection controls layout.
                | set_connection_delegate - Injects active action delegate for connection toggle.
                | on_toggle_connect - Handles click event on connection toggle button.
                | refresh_ports - Scans available serial/USB ports and selects preference.
                | get_selected_port - Returns the currently selected port identifier.
                | set_connected_state - Updates button styling and label according to connection.
                | save_preference - Persists active serial port selection to storage.
    '''

    _cbo_ports: Combobox
    _btn_connect: Button
    _connection_delegate: IPortConnectionDelegate
    _connection_repository: IConnectionRepository

    def __init__(
        self,
        parent: Widget,
        *,
        connection_repository: IConnectionRepository,
        connection_delegate: IPortConnectionDelegate = NULL_CONNECTION_DELEGATE,
    ) -> None:
        '''
            Initializes the port connection controls layout.

            :param parent: Parent container widget.
            :param connection_repository: Injected IConnectionRepository instance.
            :param connection_delegate: Action delegate handling port connection toggle.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._connection_delegate = connection_delegate
        self._connection_repository: Final[IConnectionRepository] = connection_repository

        Label(self, text='Port:').pack(side=LEFT)
        self._cbo_ports = Combobox(self, width=16)
        self._cbo_ports.pack(side=LEFT, padx=4)
        self._cbo_ports.bind('<<ComboboxSelected>>', lambda e: self.save_preference())

        Button(self, text='Refresh', command=self.refresh_ports).pack(side=LEFT, padx=2)

        self._btn_connect = Button(
            self,
            text='Connect',
            style='Accent.TButton',
            command=self.on_toggle_connect,
        )
        self._btn_connect.pack(side=LEFT, padx=6)
        self.refresh_ports()

    def set_connection_delegate(
        self,
        connection_delegate: IPortConnectionDelegate,
    ) -> None:
        '''
            Injects active action delegate for connection toggle commands.

            :param connection_delegate: IPortConnectionDelegate instance.
            :exceptions: None.
        '''
        self._connection_delegate = connection_delegate

    def on_toggle_connect(self) -> None:
        '''
            Handles click event on connection toggle button.

            :exceptions: None.
        '''
        self._connection_delegate.toggle_connection()

    def refresh_ports(self) -> None:
        '''
            Scans available serial/USB ports on the host system and restores preference.

            :exceptions: None.
        '''
        current_selection: str = self._cbo_ports.get()
        preference: ConnectionPreference = self._connection_repository.load_preference()
        ports: list[str] = ['127.0.0.1:8888 (Digital Twin)'] + SerialPortScanner.scan_ports()
        self._cbo_ports['values'] = ports

        if current_selection in ports:
            self._cbo_ports.set(current_selection)
        elif preference.port:
            matching_ports = [p for p in ports if p.startswith(preference.port)]
            if matching_ports:
                self._cbo_ports.set(matching_ports[0])
            elif ports:
                self._cbo_ports.current(0)
            else:
                self._cbo_ports.set('')
        elif ports:
            self._cbo_ports.current(0)
        else:
            self._cbo_ports.set('')

    def get_selected_port(self) -> str:
        '''
            Returns the currently selected port identifier string.

            :return: Clean port identifier string.
            :exceptions: None.
        '''
        port_val: str = self._cbo_ports.get()

        if not port_val:
            return ''

        return port_val.split(' ')[0] if ' ' in port_val else port_val

    def set_selected_port(self, port: str) -> None:
        '''
            Sets port value in ports combobox.

            :param port: Port name string.
            :exceptions: None.
        '''
        self._cbo_ports.set(port)

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates button styling and label according to connection status.

            :param connected: True if connected, False if disconnected.
            :exceptions: None.
        '''
        if connected:
            self.save_preference()
            self._btn_connect.configure(text='Disconnect', style='Danger.TButton')
        else:
            self._btn_connect.configure(text='Connect', style='Accent.TButton')

    def save_preference(self) -> None:
        '''
            Persists active serial port selection to storage.

            :exceptions: None.
        '''
        port: str = self.get_selected_port()

        if port and not port.startswith('127.0.0.1:8888'):
            preference: ConnectionPreference = ConnectionPreference(
                port=port,
                baud=115200,
            )
            self._connection_repository.save_preference(preference)

    @property
    def connect_button_text(self) -> str:
        '''
            Returns text of connection toggle button.

            :return: String button text.
            :exceptions: None.
        '''
        return str(self._btn_connect['text'])
