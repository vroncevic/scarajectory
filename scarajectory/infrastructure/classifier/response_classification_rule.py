# -*- coding: UTF-8 -*-

'''
Module
    response_classification_rule.py
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
    Predicate-based response classification rule building ScaraResponse models.
'''

from __future__ import annotations

from collections.abc import Callable
from typing import Final

from scarajectory.core.model.protocol.scara_response import ScaraResponse

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseClassificationRule:
    '''
        Predicate-based rule evaluating lines and producing typed responses.

        It defines:

            :attributes:
                | _response_type - Target response type string identifier.
                | _matcher - Predicate callable checking response line match.
                | _is_success - Flag indicating whether response is successful.
                | _preserve_clean_msg - True to keep delimiters in message.
            :methods:
                | __init__ - Initializes classification rule configuration.
                | matches - Checks whether line matches predicate.
                | classify - Builds typed ScaraResponse for matched line.
    '''

    _response_type: str
    _matcher: Callable[[str], bool]
    _is_success: bool
    _preserve_clean_msg: bool

    def __init__(
        self,
        response_type: str,
        matcher: Callable[[str], bool],
        *,
        is_success: bool = True,
        preserve_clean_msg: bool = False,
    ) -> None:
        '''
            Initializes classification rule.

            :param response_type: Response type identifier string.
            :param matcher: Predicate callable evaluating clean string.
            :param is_success: Whether this response signifies success.
            :param preserve_clean_msg: True to keep outer delimiters.
            :exceptions: None.
        '''
        self._response_type: Final[str] = response_type
        self._matcher: Final[Callable[[str], bool]] = matcher
        self._is_success: Final[bool] = is_success
        self._preserve_clean_msg: Final[bool] = preserve_clean_msg

    def matches(self, clean_line: str) -> bool:
        '''
            Checks whether response line matches predicate.

            :param clean_line: Stripped raw response string.
            :return: True if predicate matches, False otherwise.
            :exceptions: None.
        '''
        return self._matcher(clean_line)

    def classify(self, clean_line: str) -> ScaraResponse:
        '''
            Builds typed ScaraResponse for matched line.

            :param clean_line: Stripped raw response string.
            :return: Structured ScaraResponse instance.
            :exceptions: None.
        '''
        stripped: str = (
            clean_line[1:-1]
            if clean_line.startswith('<') and clean_line.endswith('>')
            else clean_line
        )
        msg: str = clean_line if self._preserve_clean_msg else stripped

        return ScaraResponse(
            response_type=self._response_type,
            message=msg,
            raw_line=clean_line,
            is_success=self._is_success,
        )
