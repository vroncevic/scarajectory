# -*- coding: UTF-8 -*-

'''
Module
    parser_state.py
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
    Defines ParserState enumeration for binary stream parser finite state machine.
'''

from __future__ import annotations

from enum import IntEnum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParserState(IntEnum):
    '''
        Discrete states of the binary wire frame streaming parser FSM.

        It defines:

            :attributes:
                | SEARCH_SOF1 - Waiting for first synchronization byte SOF1 (0xAA).
                | SEARCH_SOF2 - Waiting for second synchronization byte SOF2 (0x55).
                | READ_MSG_ID - Reading message type identifier byte.
                | READ_SEQ_NUM - Reading cyclic sequence counter byte.
                | READ_PAYLOAD_LEN - Reading payload length byte.
                | READ_PAYLOAD - Accumulating variable payload data bytes.
                | READ_CRC_LO - Reading lower byte of CRC-16 checksum.
                | READ_CRC_HI - Reading higher byte of CRC-16 checksum.
                | READ_EOF - Verifying end-of-frame delimiter byte (0x0D).
    '''

    SEARCH_SOF1 = 0
    SEARCH_SOF2 = 1
    READ_MSG_ID = 2
    READ_SEQ_NUM = 3
    READ_PAYLOAD_LEN = 4
    READ_PAYLOAD = 5
    READ_CRC_LO = 6
    READ_CRC_HI = 7
    READ_EOF = 8
