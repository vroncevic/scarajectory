# -*- coding: UTF-8 -*-

'''
Module
    flow_status_classifier.py
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
    Classifier evaluating microcontroller ASCII protocol responses for buffer throttling and fault events.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.core.service.classifier.iresponse_parser import IResponseParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowStatusClassifier:
    '''
        Evaluates ASCII protocol packets against queue buffer capacity and channel safety criteria.

        It defines:

            :attributes:
                | _response_parser - The parser for decoding raw ASCII wire packets.
            :methods:
                | __init__ - Initializes FlowStatusClassifier with response parser.
                | is_buffer_full - Checks if packet indicates microcontroller buffer saturation.
                | is_error - Checks if packet signals an error or fault condition.
                | is_telemetry - Checks if packet contains real-time kinematic telemetry.
    '''

    _response_parser: IResponseParser

    def __init__(self, response_parser: IResponseParser) -> None:
        '''
            Initializes FlowStatusClassifier with response parser.

            :param response_parser: IResponseParser instance for decoding wire packets.
            :exceptions: None.
        '''
        self._response_parser: Final[IResponseParser] = response_parser

    def is_buffer_full(self, line: str) -> bool:
        '''
            Checks if packet indicates microcontroller buffer saturation.

            :param line: Received line string.
            :return: True if buffer full packet, False otherwise.
            :exceptions: None.
        '''
        resp: ScaraResponse = self._response_parser.parse_response(line)

        return resp.response_type in ('FULL', 'NACK') and 'BUFFER_FULL' in resp.raw_line

    def is_error(self, line: str) -> bool:
        '''
            Checks if packet signals an error or fault condition.

            :param line: Received line string.
            :return: True if error condition, False otherwise.
            :exceptions: None.
        '''
        resp: ScaraResponse = self._response_parser.parse_response(line)

        return resp.response_type in ('ERR', 'NACK', 'MOVE_FAILED', 'HOMED_FAIL') or not resp.is_success

    def is_telemetry(self, line: str) -> bool:
        '''
            Checks if packet contains real-time kinematic telemetry.

            :param line: Received line string.
            :return: True if telemetry packet, False otherwise.
            :exceptions: None.
        '''
        return self._response_parser.parse_response(line).response_type == 'TELEM'
