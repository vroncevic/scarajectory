# -*- coding: UTF-8 -*-

'''
Module
    error_code.py
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
    Defines ErrorCode enumeration for protocol NACK error classifications.
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


class ErrorCode(IntEnum):
    '''
        Standardized binary protocol NACK rejection error codes.

        It defines:

            :attributes:
                | NONE - No error (0x00).
                | CRC_FAIL - Checksum validation failure (0x01).
                | UNKNOWN_CMD - Unrecognized or unsupported command ID (0x02).
                | INVALID_LENGTH - Frame payload length mismatch (0x03).
                | QUEUE_FULL - Motion queue buffer is full (0x04).
                | ESTOP_ACTIVE - Operation rejected because E-STOP is latched (0x05).
                | NOT_HELD - Resume called while not in hold state (0x06).
                | INVALID_JOINT - Invalid joint index specified (0x07).
                | HOMING_FAILED - Homing switch search timed out or failed (0x08).
                | EXECUTION_FAILED - Stepper actuator motion execution failure (0x09).
    '''

    NONE = 0x00
    CRC_FAIL = 0x01
    UNKNOWN_CMD = 0x02
    INVALID_LENGTH = 0x03
    QUEUE_FULL = 0x04
    ESTOP_ACTIVE = 0x05
    NOT_HELD = 0x06
    INVALID_JOINT = 0x07
    HOMING_FAILED = 0x08
    EXECUTION_FAILED = 0x09
