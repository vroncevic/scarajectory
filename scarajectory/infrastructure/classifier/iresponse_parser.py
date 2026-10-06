# -*- coding: UTF-8 -*-

'''
Module
    iresponse_parser.py
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
    Defines IResponseParser protocol interface for decoding raw ASCII wire packets and queue metrics.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.protocol.scara_response import ScaraResponse

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IResponseParser(Protocol):
    '''
        Protocol contract for decoding incoming ASCII protocol responses from robot firmware.

        It defines:

            :methods:
                | parse_response - Parses raw response line into typed ScaraResponse.
                | has_queue_depth - Checks if packet reports remote queue depth.
                | parse_queue_depth - Extracts remote queue depth integer from ACK packet.
    '''

    def parse_response(self, line: str) -> ScaraResponse:
        '''
            Parses raw response line into typed ScaraResponse.

            :param line: Raw response text line.
            :return: Structured ScaraResponse.
        '''

    def has_queue_depth(self, line: str) -> bool:
        '''
            Checks if packet reports remote queue depth.

            :param line: Received line string.
            :return: True if line contains queue depth metadata, False otherwise.
        '''

    def parse_queue_depth(self, line: str) -> int:
        '''
            Extracts remote queue depth integer from ACK packet.

            :param line: Received line string.
            :return: Integer queue depth count.
        '''
