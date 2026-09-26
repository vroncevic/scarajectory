# -*- coding: UTF-8 -*-

'''
Module
    protocol_status_classifier.py
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
    Classifier evaluating microcontroller ASCII protocol responses for state transitions and safety events.
'''

from __future__ import annotations

from scarajectory.core.model.communication.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.communication.protocol.ascii.parser.response_parser import ResponseParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolStatusClassifier:
    '''
        Evaluates ASCII protocol wire packets against domain state and safety criteria.

        It defines:

            :methods:
                | is_buffer_full - Checks if packet indicates microcontroller buffer saturation.
                | is_move_done - Checks if packet confirms completion of a waypoint move.
                | is_move_failed - Checks if packet confirms failure of a waypoint move.
                | is_action_done - Checks if packet confirms completion of a tool or wait action.
                | is_complete - Checks if packet confirms completion of either a move or action.
                | is_homed_success - Checks if packet confirms successful robot homing.
                | is_homing_failed - Checks if packet confirms homing failure or timeout.
                | is_telemetry - Checks if packet contains real-time kinematic telemetry.
                | is_error - Checks if packet signals an error condition.
    '''

    @classmethod
    def is_buffer_full(cls, line: str) -> bool:
        '''
            Checks if packet indicates microcontroller buffer saturation.

            :param line: Received line string.
            :return: True if buffer full packet, False otherwise.
            :exceptions: None.
        '''
        resp: ScaraResponse = ResponseParser.parse_response(line)

        return resp.response_type in ('FULL', 'NACK') and 'BUFFER_FULL' in resp.raw_line

    @classmethod
    def is_move_done(cls, line: str) -> bool:
        '''
            Checks if packet confirms completion of a waypoint move.

            :param line: Received line string.
            :return: True if move completed confirmation, False otherwise.
            :exceptions: None.
        '''
        return ResponseParser.parse_response(line).response_type == 'DONE'

    @classmethod
    def is_move_failed(cls, line: str) -> bool:
        '''
            Checks if packet confirms failure of a waypoint move.

            :param line: Received line string.
            :return: True if move failed confirmation, False otherwise.
            :exceptions: None.
        '''
        return ResponseParser.parse_response(line).response_type == 'MOVE_FAILED'

    @classmethod
    def is_action_done(cls, line: str) -> bool:
        '''
            Checks if packet confirms completion of a tool, wait, or auxiliary action.

            :param line: Received line string.
            :return: True if action completion confirmation, False otherwise.
            :exceptions: None.
        '''
        clean: str = line.strip().upper()
        if 'WAIT_DONE' in clean or 'HOMED_SUCCESS' in clean:
            return True

        if clean.startswith('<RESP:ACK#') and any(
            act in clean for act in ('PUMP_', 'VALVE_', 'OVERRIDE=', 'ELBOW', 'MOTORS_')
        ):
            return True

        return False

    @classmethod
    def is_complete(cls, line: str) -> bool:
        '''
            Checks if packet confirms completion of either a waypoint move or action.

            :param line: Received line string.
            :return: True if move or action completed, False otherwise.
            :exceptions: None.
        '''
        return cls.is_move_done(line) or cls.is_action_done(line)

    @classmethod
    def is_homed_success(cls, line: str) -> bool:
        '''
            Checks if packet confirms successful robot homing.

            :param line: Received line string.
            :return: True if homing succeeded, False otherwise.
            :exceptions: None.
        '''
        return 'HOMED_SUCCESS' in line.strip().upper()

    @classmethod
    def is_homing_failed(cls, line: str) -> bool:
        '''
            Checks if packet confirms homing failure or timeout.

            :param line: Received line string.
            :return: True if homing failed, False otherwise.
            :exceptions: None.
        '''
        clean: str = line.strip().upper()

        return 'HOMING_FAILED' in clean or 'HOMED_FAIL' in clean

    @classmethod
    def is_telemetry(cls, line: str) -> bool:
        '''
            Checks if packet contains real-time kinematic telemetry.

            :param line: Received line string.
            :return: True if telemetry packet, False otherwise.
            :exceptions: None.
        '''
        return ResponseParser.parse_response(line).response_type == 'TELEM'

    @classmethod
    def is_error(cls, line: str) -> bool:
        '''
            Checks if packet signals an error condition.

            :param line: Received line string.
            :return: True if error condition, False otherwise.
            :exceptions: None.
        '''
        resp: ScaraResponse = ResponseParser.parse_response(line)

        return resp.response_type in ('ERR', 'NACK', 'MOVE_FAILED', 'HOMED_FAIL') or not resp.is_success
