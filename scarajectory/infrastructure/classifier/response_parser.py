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
    Parser decoding raw ASCII response lines and queue metadata into models.
'''

from __future__ import annotations

from re import IGNORECASE, Pattern, compile as re_compile
from typing import ClassVar, Final

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.response_classification_registry import ResponseClassificationRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseParser:
    '''
        Decodes incoming raw ASCII protocol responses into structured models.

        It defines:

            :attributes:
                | _registry - The classification registry for matching response patterns.
            :methods:
                | __init__ - Initializes ResponseParser with classification registry.
                | parse_response - Parses raw line into typed response.
                | has_queue_depth - Checks if packet reports queue depth.
                | parse_queue_depth - Extracts remote queue depth integer.
    '''

    _QUEUE_REGEX: ClassVar[Pattern[str]] = re_compile(r'QUEUE=(\d+)', IGNORECASE)
    _registry: ResponseClassificationRegistry

    def __init__(self, registry: ResponseClassificationRegistry) -> None:
        '''
            Initializes ResponseParser with classification registry.

            :param registry: ResponseClassificationRegistry instance.
            :exceptions: None.
        '''
        self._registry: Final[ResponseClassificationRegistry] = registry

    def parse_response(self, line: str) -> ScaraResponse:
        '''
            Parses raw response line into typed ScaraResponse.

            :param line: Raw response text line.
            :return: Structured ScaraResponse.
            :exceptions: None.
        '''
        clean: str = line.strip()

        return self._registry.classify(clean)

    def has_queue_depth(self, line: str) -> bool:
        '''
            Checks if packet reports remote queue depth.

            :param line: Received line string.
            :return: True if line contains queue depth metadata.
            :exceptions: None.
        '''
        clean: str = line.strip()

        if not (clean.startswith('<RESP:ACK') or clean.startswith('<ACK')):
            return False

        return self._QUEUE_REGEX.search(clean) is not None

    def parse_queue_depth(self, line: str) -> int:
        '''
            Extracts remote queue depth integer from ACK packet.

            :param line: Received line string.
            :return: Integer queue depth count (0 if not present).
            :exceptions: None.
        '''
        clean: str = line.strip()

        if not (clean.startswith('<RESP:ACK') or clean.startswith('<ACK')):
            return 0

        match = self._QUEUE_REGEX.search(clean)

        return int(match.group(1)) if match else 0
