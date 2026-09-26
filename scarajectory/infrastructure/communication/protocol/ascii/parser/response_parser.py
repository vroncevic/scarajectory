# -*- coding: UTF-8 -*-

'''
Module
    response_parser.py
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
    Parser decoding raw ASCII response lines and queue metadata into structured ScaraResponse models.
'''

from __future__ import annotations

from re import IGNORECASE, Pattern, compile
from typing import ClassVar

from scarajectory.core.model.communication.protocol.scara_response import ScaraResponse

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseParser:
    '''
        Decodes incoming raw newline-terminated ASCII protocol responses into structured models.

        It defines:

            :methods:
                | parse_response - Parses raw response line into typed ScaraResponse.
                | parse_queue_depth - Extracts remote queue depth from ACK packet if present.
    '''

    _QUEUE_REGEX: ClassVar[Pattern[str]] = compile(r'QUEUE=(\d+)', IGNORECASE)

    @classmethod
    def parse_response(cls, line: str) -> ScaraResponse:
        '''
            Parses raw response line into typed ScaraResponse.

            :param line: Raw response text line.
            :return: Structured ScaraResponse.
            :exceptions: None.
        '''
        clean: str = line.strip()
        stripped: str = clean[1:-1] if clean.startswith('<') and clean.endswith('>') else clean
        resp_type: str = 'UNKNOWN'
        msg: str = stripped
        success: bool = True

        match clean:
            case s if s.startswith(('<RESP:ACK', '<ACK')):
                resp_type = 'ACK'
            case s if s.startswith(('<RESP:CONFIG', '<CONFIG')):
                resp_type = 'CONFIG'
            case s if s.startswith(('<RESP:ELBOW', '<ELBOW')):
                resp_type = 'ELBOW'
            case s if s.startswith(('<RESP:NACK', '<NACK')):
                resp_type = 'NACK'
                success = False
            case s if 'MOVE_DONE' in s or s == '<DONE>':
                resp_type = 'DONE'
                msg = clean
            case s if 'MOVE_FAILED' in s:
                resp_type = 'MOVE_FAILED'
                success = False
            case s if 'MOVE_START' in s:
                resp_type = 'MOVE_START'
            case s if s.startswith('<TELEM'):
                resp_type = 'TELEM'
            case s if 'BUFFER_FULL' in s or s == '<FULL>':
                resp_type = 'FULL'
                success = False
                msg = clean
            case s if 'ERR' in s or s.startswith('<ERR'):
                resp_type = 'ERR'
                success = False
                msg = clean
            case s if 'HOMED_SUCCESS' in s:
                resp_type = 'HOMED'
            case s if 'HOMED_FAIL' in s or 'HOMING_FAILED' in s:
                resp_type = 'HOMED_FAIL'
                success = False
            case s if s.startswith(('<STATUS', '<RESP:STATUS')):
                resp_type = 'STATUS'
            case s if s.startswith(('<POS', '<RESP:POS')):
                resp_type = 'POS'
            case _:
                msg = clean

        return ScaraResponse(
            response_type=resp_type,
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
        clean: str = line.strip()
        if not (clean.startswith('<RESP:ACK') or clean.startswith('<ACK')):
            return None

        match = cls._QUEUE_REGEX.search(clean)

        return int(match.group(1)) if match else None
