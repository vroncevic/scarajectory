# -*- coding: UTF-8 -*-

'''
Module
    protocol_parser.py
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
    Parser for ASCII communication packets and telemetry received from microcontroller.
'''

from __future__ import annotations

import re
from typing import ClassVar

from scarajectory.infrastructure.communication.protocol.robot_response_dto import RobotResponseDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolParser:
    '''
        Parser decoding incoming newline-terminated ASCII protocol responses.

        It defines:

            :methods:
                | parse_response - Parses raw response line into typed RobotResponseDTO.
                | parse_queue_depth - Extracts remote queue depth from ACK packet if present.
                | is_buffer_full - Checks if packet indicates microcontroller buffer saturation.
                | is_move_done - Checks if packet confirms completion of a waypoint move.
                | is_telemetry - Checks if packet contains real-time kinematic telemetry.
                | is_error - Checks if packet signals an error condition.
    '''

    _QUEUE_REGEX: ClassVar[re.Pattern[str]] = re.compile(r'QUEUE=(\d+)', re.IGNORECASE)

    @classmethod
    def parse_response(cls, line: str) -> RobotResponseDTO:
        '''
            Parses raw response line into typed RobotResponseDTO.

            :param line: Raw response text line.
            :return: Structured RobotResponseDTO.
            :exceptions: None.
        '''
        clean: str = line.strip()
        resp_type: str = 'UNKNOWN'
        q_depth: int | None = None
        msg: str = clean
        success: bool = True

        if clean.startswith('<RESP:ACK') or clean.startswith('<ACK'):
            resp_type = 'ACK'
            match = cls._QUEUE_REGEX.search(clean)
            if match:
                q_depth = int(match.group(1))
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif clean.startswith('<RESP:CONFIG') or clean.startswith('<CONFIG'):
            resp_type = 'CONFIG'
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif clean.startswith('<RESP:ELBOW') or clean.startswith('<ELBOW'):
            resp_type = 'ELBOW'
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif clean.startswith('<RESP:NACK') or clean.startswith('<NACK'):
            resp_type = 'NACK'
            success = False
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif 'MOVE_DONE' in clean or clean == '<DONE>':
            resp_type = 'DONE'
        elif 'MOVE_FAILED' in clean:
            resp_type = 'MOVE_FAILED'
            success = False
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif 'MOVE_START' in clean:
            resp_type = 'MOVE_START'
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif clean.startswith('<TELEM'):
            resp_type = 'TELEM'
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif 'BUFFER_FULL' in clean or clean == '<FULL>':
            resp_type = 'FULL'
            success = False
        elif 'ERR' in clean or clean.startswith('<ERR'):
            resp_type = 'ERR'
            success = False
        elif clean.startswith('<STATUS') or clean.startswith('<RESP:STATUS'):
            resp_type = 'STATUS'
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        elif clean.startswith('<POS') or clean.startswith('<RESP:POS'):
            resp_type = 'POS'
            msg = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean

        return RobotResponseDTO(
            response_type=resp_type,
            queue_depth=q_depth,
            message=msg,
            raw_line=clean,
            is_success=success
        )

    @classmethod
    def parse_queue_depth(cls, line: str) -> int | None:
        '''
            Extracts remote queue depth integer from ACK packet if present.

            :param line: Received line string.
            :return: Integer queue depth or None if line is not an ACK packet.
            :exceptions: None.
        '''
        resp: RobotResponseDTO = cls.parse_response(line)
        return resp.queue_depth if resp.response_type == 'ACK' else None

    @classmethod
    def is_buffer_full(cls, line: str) -> bool:
        '''
            Checks if packet indicates microcontroller buffer saturation.

            :param line: Received line string.
            :return: True if buffer full packet, False otherwise.
            :exceptions: None.
        '''
        resp: RobotResponseDTO = cls.parse_response(line)
        return resp.response_type in ('FULL', 'NACK') and 'BUFFER_FULL' in resp.raw_line

    @classmethod
    def is_move_done(cls, line: str) -> bool:
        '''
            Checks if packet confirms completion of a waypoint move.

            :param line: Received line string.
            :return: True if move completed confirmation, False otherwise.
            :exceptions: None.
        '''
        return cls.parse_response(line).response_type == 'DONE'

    @classmethod
    def is_move_failed(cls, line: str) -> bool:
        '''
            Checks if packet confirms failure of a waypoint move.

            :param line: Received line string.
            :return: True if move failed confirmation, False otherwise.
            :exceptions: None.
        '''
        return cls.parse_response(line).response_type == 'MOVE_FAILED'

    @classmethod
    def is_telemetry(cls, line: str) -> bool:
        '''
            Checks if packet contains real-time kinematic telemetry.

            :param line: Received line string.
            :return: True if telemetry packet, False otherwise.
            :exceptions: None.
        '''
        return cls.parse_response(line).response_type == 'TELEM'

    @classmethod
    def is_error(cls, line: str) -> bool:
        '''
            Checks if packet signals an error condition.

            :param line: Received line string.
            :return: True if error condition, False otherwise.
            :exceptions: None.
        '''
        resp: RobotResponseDTO = cls.parse_response(line)
        return resp.response_type in ('ERR', 'NACK', 'MOVE_FAILED') or not resp.is_success
