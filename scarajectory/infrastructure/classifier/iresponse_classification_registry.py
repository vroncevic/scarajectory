# -*- coding: UTF-8 -*-

'''
Module
    iresponse_classification_registry.py
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
    Defines structural protocol IResponseClassificationRegistry for rule dispatching.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.iresponse_classification_rule import IResponseClassificationRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IResponseClassificationRegistry(Protocol):
    '''
        Structural protocol defining classification rule registry operations.

        It defines:

            :methods:
                | register_rule - Appends a classification rule to registry.
                | classify - Evaluates line against rules and returns response.
    '''

    def register_rule(self, rule: IResponseClassificationRule) -> None:
        '''
            Appends a classification rule to the ordered registry.

            :param rule: Rule implementing IResponseClassificationRule.
            :exceptions: None.
        '''

    def classify(self, clean_line: str) -> ScaraResponse:
        '''
            Evaluates line against rules and returns structured response.

            :param clean_line: Clean stripped response line.
            :return: Structured ScaraResponse instance.
            :exceptions: None.
        '''
