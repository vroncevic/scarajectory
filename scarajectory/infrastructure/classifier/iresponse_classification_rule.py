# -*- coding: UTF-8 -*-

'''
Module
    iresponse_classification_rule.py
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
    Defines structural protocol IResponseClassificationRule for classification.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.protocol.scara_response import ScaraResponse

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IResponseClassificationRule(Protocol):
    '''
        Structural protocol defining single response line classification rule.

        It defines:

            :methods:
                | matches - Checks whether line matches this rule predicate.
                | classify - Builds typed ScaraResponse for matched line.
    '''

    def matches(self, clean_line: str) -> bool:
        '''
            Checks whether response line matches rule predicate.

            :param clean_line: Stripped raw response string.
            :return: True if matched, False otherwise.
        '''

    def classify(self, clean_line: str) -> ScaraResponse:
        '''
            Builds typed ScaraResponse for matched line.

            :param clean_line: Stripped raw response string.
            :return: Structured ScaraResponse instance.
        '''
