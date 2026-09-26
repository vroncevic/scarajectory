# -*- coding: UTF-8 -*-

'''
Module
    binary_frame.py
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
    Defines BinaryFrame value object for assembled wire protocol packets.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.communication.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class BinaryFrame:
    '''
        Immutable wire protocol binary frame representation.

        It defines:

            :attributes:
                | msg_id - Message type identifier.
                | seq_num - Cyclic sequence counter (0 - 255).
                | payload - Binary body bytes (up to 64 bytes).
                | crc16 - 16-bit CRC checksum.
    '''

    msg_id: MessageId
    seq_num: int
    payload: bytes
    crc16: int
