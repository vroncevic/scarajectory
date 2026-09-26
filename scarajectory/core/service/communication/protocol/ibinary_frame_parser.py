# -*- coding: UTF-8 -*-

'''
Module
    ibinary_frame_parser.py
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
    Defines IBinaryFrameParser Protocol for streaming binary protocol decoding.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryFrameParser(Protocol):
    '''
        Structural protocol defining binary frame decoding contracts.

        It defines:

            :methods:
                | feed_byte - Processes a single incoming stream byte.
                | feed_bytes - Processes multiple stream bytes and yields frames.
                | reset - Clears parser state machine and internal buffers.
    '''

    def feed_byte(self, byte: int) -> BinaryFrame | None:
        '''
            Processes a single incoming byte through the FSM.

            :param byte: Integer byte value (0 - 255).
            :return: Assembled BinaryFrame if completed and valid, None otherwise.
        '''

    def feed_bytes(self, data: bytes) -> tuple[BinaryFrame, ...]:
        '''
            Processes an incoming block of bytes and returns all complete frames.

            :param data: Contiguous input bytes.
            :return: Tuple of assembled BinaryFrame instances.
        '''

    def reset(self) -> None:
        '''
            Resets the internal state machine back to start of frame search.
        '''
