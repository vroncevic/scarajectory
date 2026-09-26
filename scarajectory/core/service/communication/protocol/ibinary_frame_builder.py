# -*- coding: UTF-8 -*-

'''
Module
    ibinary_frame_builder.py
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
    Defines IBinaryFrameBuilder interface for packaging binary wire frames.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.joint_steps import JointSteps
from scarajectory.core.model.communication.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryFrameBuilder(Protocol):
    '''
        Structural protocol defining binary frame construction contracts.

        It defines:

            :methods:
                | build_frame - Assembles a generic binary frame with CRC16.
                | build_joint_move - Builds a MSG_CMD_MOVE_JOINT_STEPS motion frame.
                | build_system_cmd - Builds a parameterless system command frame.
                | build_tool_cmd - Builds a tool actuation command frame.
                | pack_frame - Serializes a BinaryFrame into raw wire bytes with delimiters.
    '''

    def build_frame(self, *, msg_id: MessageId, seq_num: int, payload: bytes = b'') -> BinaryFrame:
        '''
            Constructs and checksums a complete wire protocol BinaryFrame.

            :param msg_id: Command message identifier.
            :param seq_num: Cyclic sequence index (0 - 255).
            :param payload: Raw body bytes (0 to 64 bytes).
            :return: Fully assembled BinaryFrame with valid CRC16.
        '''

    def build_joint_move(self, *, seq_num: int, steps: JointSteps) -> BinaryFrame:
        '''
            Builds a joint step motion frame from JointSteps model.

            :param seq_num: Cyclic sequence index.
            :param steps: JointSteps target instance.
            :return: Assembled BinaryFrame with joint move payload.
        '''

    def build_system_cmd(self, *, msg_id: MessageId, seq_num: int) -> BinaryFrame:
        '''
            Builds a parameterless system command frame (ENABLE, ESTOP, PING, etc.).

            :param msg_id: Target command message identifier.
            :param seq_num: Cyclic sequence index.
            :return: Assembled parameterless BinaryFrame.
        '''

    def build_tool_cmd(self, *, seq_num: int, tool_id: int, state: bool) -> BinaryFrame:
        '''
            Builds a tool actuation command frame (PUMP, VALVE).

            :param seq_num: Cyclic sequence index.
            :param tool_id: Tool identifier (0=PUMP, 1=VALVE).
            :param state: True to activate, False to deactivate.
            :return: Assembled tool command BinaryFrame.
        '''

    def pack_frame(self, *, frame: BinaryFrame) -> bytes:
        '''
            Encodes the frame into a byte string according to wire format.

            :param frame: BinaryFrame instance.
            :return: Formatted bytes: SOF1 + SOF2 + MSG + SEQ + LEN + DATA + CRC + EOF.
        '''
