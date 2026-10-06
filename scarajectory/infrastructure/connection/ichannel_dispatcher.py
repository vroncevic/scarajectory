# -*- coding: UTF-8 -*-

'''
Module
    ichannel_dispatcher.py
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
    Structural protocol defining channel dispatcher contracts.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IChannelDispatcher(Protocol):
    '''
        Structural protocol defining channel dispatcher operations.

        It defines:

            :attributes:
                | protocol_mode - Active wire protocol mode enum value.

            :methods:
                | is_connected - Checks if communication transport is active.
                | next_seq - Increments and returns next cyclic sequence counter.
                | send_command - Transmits ASCII formatted command string over transport.
                | send_frame - Serializes and transmits binary frame over transport.
    '''

    @property
    def protocol_mode(self) -> ProtocolMode:
        '''
            Returns active wire protocol mode.

            :return: ProtocolMode enum value.
        '''

    @protocol_mode.setter
    def protocol_mode(self, mode: ProtocolMode) -> None:
        '''
            Updates active wire protocol mode dynamically.

            :param mode: ProtocolMode enum value.
        '''

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
        '''

    def next_seq(self) -> int:
        '''
            Increments and returns next cyclic sequence counter.

            :return: Cyclic sequence counter value (0-255).
        '''

    def send_command(self, cmd: str) -> bool:
        '''
            Transmits raw command string if streamer transport is connected.

            :param cmd: Formatted command string.
            :return: True if command transmitted, False otherwise.
        '''

    def send_frame(self, frame: BinaryFrame) -> bool:
        '''
            Packs and transmits binary frame if streamer transport is connected.

            :param frame: BinaryFrame instance.
            :return: True if frame transmitted, False otherwise.
        '''
