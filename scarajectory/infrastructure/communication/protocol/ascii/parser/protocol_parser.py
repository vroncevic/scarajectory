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
    Unified parser facade combining response decoding, queue extraction and status classification.
'''

from __future__ import annotations

from scarajectory.infrastructure.communication.protocol.ascii.parser.protocol_status_classifier import ProtocolStatusClassifier
from scarajectory.infrastructure.communication.protocol.ascii.parser.response_parser import ResponseParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolParser(ResponseParser, ProtocolStatusClassifier):
    '''
        Unified ASCII protocol parser decoding responses, queue depth and status predicates.

        Inherits raw response and queue depth extraction from ResponseParser,
        and domain state/safety classification from ProtocolStatusClassifier.

        It defines:

            :methods:
                | get_version - Returns protocol parser module version string.
                | is_valid_packet - Checks syntactic frame integrity of an ASCII packet.
    '''

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns protocol parser module version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__

    @classmethod
    def is_valid_packet(cls, line: str) -> bool:
        '''
            Checks syntactic frame integrity of an ASCII wire packet.

            :param line: Raw response line string.
            :return: True if line is a properly framed ASCII packet (<...>), False otherwise.
            :exceptions: None.
        '''
        clean: str = line.strip()

        return len(clean) >= 2 and clean.startswith('<') and clean.endswith('>')
