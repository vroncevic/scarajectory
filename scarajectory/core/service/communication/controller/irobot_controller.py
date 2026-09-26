# -*- coding: UTF-8 -*-

'''
Module
    irobot_controller.py
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
    Defines composite IRobotController port interface combining all controller operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.communication.controller.ijog_controller import IJogController
from scarajectory.core.service.communication.controller.imotion_controller import IMotionController
from scarajectory.core.service.communication.controller.iquery_controller import IQueryController
from scarajectory.core.service.communication.controller.itool_controller import IToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IRobotController(IMotionController, IJogController, IToolController, IQueryController, Protocol):
    '''
    Composite robot controller port combining motion, jogging, tooling, and query interfaces.

    It defines:

        :methods:
            | is_connected - Checks whether communication transport is active.
            | set_protocol_mode - Updates protocol mode dynamically.
            | send_command - Transmits formatted command string if connected.
            | send_binary_frame - Packs and transmits binary frame if connected.
    '''

    def is_connected(self) -> bool:
        '''
        Checks whether communication transport is active.

        :return: True if connected, False otherwise.
        '''

    def set_protocol_mode(self, mode: ProtocolMode) -> None:
        '''
        Updates protocol mode dynamically.

        :param mode: ProtocolMode enum value.
        '''

    def send_command(self, cmd: str) -> bool:
        '''
        Transmits formatted command string if connected.

        :param cmd: Formatted command string.
        :return: True if transmitted, False if disconnected.
        '''

    def send_binary_frame(self, frame: BinaryFrame) -> bool:
        '''
        Packs and transmits binary frame if connected.

        :param frame: BinaryFrame instance.
        :return: True if transmitted, False otherwise.
        '''
