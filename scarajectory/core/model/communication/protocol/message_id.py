# -*- coding: UTF-8 -*-

'''
Module
    message_id.py
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
    Defines MessageId enumeration for binary protocol message identifiers.
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


class MessageId(IntEnum):
    '''
        Binary protocol message type identifiers.

        It defines:

            :attributes:
                | CMD_NONE - No operation (0x00).
                | CMD_MOVE_JOINT_STEPS - Joint step target move (0x01).
                | CMD_ENABLE - Enable stepper motors (0x03).
                | CMD_DISABLE - Disable stepper motors (0x04).
                | CMD_ESTOP - Emergency stop (0x05).
                | CMD_HOME - Joint homing routine (0x06).
                | CMD_HOLD - Motion feed hold (0x07).
                | CMD_RESUME - Motion resume (0x08).
                | CMD_JOG_JOINT - Single joint relative jog (0x09).
                | CMD_SETPOS_STEPS - Set absolute joint step position (0x0A).
                | CMD_TOOL_PUMP - Vacuum pump tool actuation (0x0B).
                | CMD_TOOL_VALVE - Release valve tool actuation (0x0C).
                | CMD_WAIT - Dwell delay in milliseconds (0x0D).
                | CMD_OVERRIDE - Feedrate speed override percentage (0x0E).
                | CMD_GET_STATUS - Query system status (0x20).
                | CMD_GET_STEPS - Query joint step counters (0x21).
                | CMD_GET_DIAGNOSTICS - Query diagnostics report (0x22).
                | CMD_CLEAR_FAULT - Reset latched fault condition (0x23).
                | CMD_PING - Heartbeat keepalive ping (0x24).
                | CMD_BOOTLOADER - Reboot into Pico BOOTSEL mode (0x30).
                | RESP_ACK - Positive command acknowledgment (0x80).
                | RESP_NACK - Negative command rejection (0x81).
                | RESP_STATUS - Consolidated robot status (0x82).
                | RESP_STEPS - Consolidated joint step coordinates (0x83).
                | RESP_PONG - Heartbeat keepalive pong response (0x84).
                | RESP_MOVE_EVENT - Motion execution event notification (0x85).
                | RESP_HOMING_EVENT - Homing execution event notification (0x86).
                | RESP_DIAGNOSTICS - Extended system diagnostics report (0x88).
                | RESP_FAULT_EVENT - Critical system fault alert (0x89).
    '''

    CMD_NONE = 0x00
    CMD_MOVE_JOINT_STEPS = 0x01
    CMD_ENABLE = 0x03
    CMD_DISABLE = 0x04
    CMD_ESTOP = 0x05
    CMD_HOME = 0x06
    CMD_HOLD = 0x07
    CMD_RESUME = 0x08
    CMD_JOG_JOINT = 0x09
    CMD_SETPOS_STEPS = 0x0A
    CMD_TOOL_PUMP = 0x0B
    CMD_TOOL_VALVE = 0x0C
    CMD_WAIT = 0x0D
    CMD_OVERRIDE = 0x0E

    CMD_GET_STATUS = 0x20
    CMD_GET_STEPS = 0x21
    CMD_GET_DIAGNOSTICS = 0x22
    CMD_CLEAR_FAULT = 0x23
    CMD_PING = 0x24
    CMD_BOOTLOADER = 0x30

    RESP_ACK = 0x80
    RESP_NACK = 0x81
    RESP_STATUS = 0x82
    RESP_STEPS = 0x83
    RESP_PONG = 0x84
    RESP_MOVE_EVENT = 0x85
    RESP_HOMING_EVENT = 0x86
    RESP_DIAGNOSTICS = 0x88
    RESP_FAULT_EVENT = 0x89
