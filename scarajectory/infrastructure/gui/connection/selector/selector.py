# -*- coding: UTF-8 -*-

'''
Module
    selector.py
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
    Serial port selection and preference persistence component.
'''

from __future__ import annotations

from tkinter import LEFT, Widget
from tkinter.ttk import Button, Combobox, Frame, Label
from typing import ClassVar, Final

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.preference.preference import SerialPreference
from scaracom.transport.scanner.factory import PortScannerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortSelector(Frame):
    '''
        Serial port scanning and dropdown selection component.

        It defines:

            :attributes:
                | DEFAULT_BAUD - Default communication baud rate.
                | DIGITAL_TWIN_PORT - Default network emulator address prefix.
                | DIGITAL_TWIN_LABEL - Formatted dropdown entry for digital twin.
                | _cbo_ports - Dropdown list of detected serial communication ports.
                | _connection_repository - Injected hardware connection preferences repository.
            :methods:
                | __init__ - Initializes the port selector layout and scans ports.
                | refresh_ports - Scans available serial/USB ports and selects preference.
                | get_selected_port - Returns the currently selected port identifier.
                | set_selected_port - Sets port value in ports combobox.
                | save_preference - Persists active serial port selection to storage.
    '''

    DEFAULT_BAUD: ClassVar[int] = 115200
    DIGITAL_TWIN_PORT: ClassVar[str] = '127.0.0.1:8888'
    DIGITAL_TWIN_LABEL: ClassVar[str] = '127.0.0.1:8888 (Digital Twin)'

    _cbo_ports: Combobox
    _connection_repository: ISerialPreferenceRepository

    def __init__(
        self,
        parent: Widget,
        *,
        connection_repository: ISerialPreferenceRepository,
    ) -> None:
        '''
            Initializes the port selector layout and scans ports.

            :param parent: Parent container widget.
            :param connection_repository: Injected ISerialPreferenceRepository instance.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._connection_repository: Final[ISerialPreferenceRepository] = (
            connection_repository
        )

        Label(self, text='Port:').pack(side=LEFT)
        self._cbo_ports = Combobox(self, width=16)
        self._cbo_ports.pack(side=LEFT, padx=4)
        self._cbo_ports.bind('<<ComboboxSelected>>', lambda _: self.save_preference())

        Button(self, text='Refresh', command=self.refresh_ports).pack(side=LEFT, padx=2)
        self.refresh_ports()

    def refresh_ports(self) -> None:
        '''
            Scans available serial/USB ports on the host system and restores preference.

            :exceptions: None.
        '''
        current_selection: str = self._cbo_ports.get()
        preference: SerialPreference = self._connection_repository.load_preference()
        scanned_ports: list[str] = PortScannerFactory.create().scan_ports()
        ports: list[str] = [self.DIGITAL_TWIN_LABEL] + scanned_ports
        self._cbo_ports['values'] = ports

        if current_selection in ports:
            self._cbo_ports.set(current_selection)
        elif preference.port:
            matching_ports: list[str] = [
                p for p in ports if p.startswith(preference.port)
            ]
            if matching_ports:
                self._cbo_ports.set(matching_ports[0])
            else:
                self._cbo_ports.current(0)
        else:
            self._cbo_ports.current(0)

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

    def save_preference(self) -> None:
        '''
            Persists active serial port selection to storage.

            :exceptions: None.
        '''
        port: str = self.get_selected_port()

        if port and not port.startswith(self.DIGITAL_TWIN_PORT):
            preference: SerialPreference = SerialPreference(
                port=port,
                baud=self.DEFAULT_BAUD,
            )
            self._connection_repository.save_preference(preference)
