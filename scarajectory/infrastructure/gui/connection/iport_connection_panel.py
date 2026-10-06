# -*- coding: UTF-8 -*-

'''
Module
    iport_connection_panel.py
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
    Defines structural protocol IPortConnectionPanel for port connection controls.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPortConnectionPanel(Protocol):
    '''
        Structural protocol for port connection UI panel operations.

        It defines:

            :methods:
                | set_connected_state - Updates UI indicators according to connection state.
                | get_selected_port - Returns the currently selected communication port.
    '''

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates button styling and label according to connection status.

            :param connected: True if connected, False if disconnected.
            :exceptions: None.
        '''

    def get_selected_port(self) -> str:
        '''
            Returns the currently selected communication port identifier.

            :return: String port name or address.
            :exceptions: None.
        '''
