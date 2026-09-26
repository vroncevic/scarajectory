# -*- coding: UTF-8 -*-

'''
Module
    binary_struct_format.py
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
    Defines BinaryStructFormat enumeration for binary struct packing and unpacking layouts.
'''

from __future__ import annotations

from enum import StrEnum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStructFormat(StrEnum):
    '''
        Struct pack/unpack format strings for binary wire protocol frames and payloads.

        It defines:

            :attributes:
                | HEADER - 3-byte wire frame header (<BBB: msg_id, seq_num, len).
                | TRAILER - 3-byte wire frame trailer (<HB: crc16, eof).
                | JOINT_STEPS - 22-byte joint step target payload (<iiiiIH).
                | TOOL_CMD - 2-byte tool command payload (<BB: tool_id, state).
                | STATUS - 19-byte consolidated robot status payload (<BBBiiii).
                | MOVE_EVENT - 5-byte motion execution event payload (<BI).
                | FAULT_EVENT - 6-byte system fault event payload (<BBI).
                | ACK - 2-byte positive acknowledgment payload (<BB: acked_id, q_count).
                | NACK - 2-byte negative rejection payload (<BB: rejected_id, error_code).
                | DIAGNOSTICS - 56-byte extended diagnostics report payload (<IIIIBBIIIIiiiiBBI).
    '''

    HEADER = '<BBB'
    TRAILER = '<HB'
    JOINT_STEPS = '<iiiiIH'
    TOOL_CMD = '<BB'
    STATUS = '<BBBiiii'
    MOVE_EVENT = '<BI'
    FAULT_EVENT = '<BBI'
    ACK = '<BB'
    NACK = '<BB'
    DIAGNOSTICS = '<IIIIBBIIIIiiiiBBI'
