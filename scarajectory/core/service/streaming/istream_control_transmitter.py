# -*- coding: UTF-8 -*-

'''
Module
    istream_control_transmitter.py
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
    Defines structural protocol IStreamControlTransmitter for lifecycle wire commands.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamControlTransmitter(Protocol):
    '''
        Structural protocol defining lifecycle wire command transmission.

        It defines:

            :methods:
                | send_enable - Transmits motion enable command.
                | send_hold - Transmits feed hold or pause command.
                | send_resume - Transmits motion resume command.
                | send_estop - Transmits emergency stop command.
    '''

    def send_enable(self, mode: ProtocolMode) -> None:
        '''
            Transmits motion enable command.

            :param mode: Active ProtocolMode enum value.
        '''

    def send_hold(self, mode: ProtocolMode) -> None:
        '''
            Transmits feed hold or pause command.

            :param mode: Active ProtocolMode enum value.
        '''

    def send_resume(self, mode: ProtocolMode) -> None:
        '''
            Transmits motion resume command.

            :param mode: Active ProtocolMode enum value.
        '''

    def send_estop(self, mode: ProtocolMode) -> None:
        '''
            Transmits emergency stop command.

            :param mode: Active ProtocolMode enum value.
        '''
