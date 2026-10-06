# -*- coding: UTF-8 -*-

'''
Module
    ibinary_stream_frame_handler.py
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
    Structural protocol defining binary frame response handling operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.state.stream_session import StreamSession

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryStreamFrameHandler(Protocol):
    '''
        Structural protocol defining binary frame response handling operations.

        It defines:

            :methods:
                | can_handle - Checks if message ID is supported by frame handler.
                | handle_frame - Processes parsed BinaryFrame and updates session state.
    '''

    def can_handle(self, msg_id: int) -> bool:
        '''
            Checks whether inbound message ID is supported by frame handler.

            :param msg_id: Message ID byte integer.
            :return: True if supported, False otherwise.
            :exceptions: None.
        '''

    def handle_frame(self, frame: BinaryFrame, session: StreamSession) -> bool:
        '''
            Processes inbound frame, updates session, and checks if critical stop is required.

            :param frame: Decoded BinaryFrame from transport.
            :param session: Active StreamSession instance.
            :return: True if critical fault requires immediate stop, False otherwise.
            :exceptions: None.
        '''
