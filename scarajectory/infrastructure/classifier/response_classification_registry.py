# -*- coding: UTF-8 -*-

'''
Module
    response_classification_registry.py
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
    Registry holding ordered response classification rules for protocol lines.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.iresponse_classification_rule import IResponseClassificationRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseClassificationRegistry:
    '''
        Ordered registry executing rules to classify protocol response lines.

        It defines:

            :attributes:
                | _rules - Ordered list of classification rules.
            :methods:
                | __init__ - Initializes registry with optional rules.
                | register_rule - Appends a classification rule to registry.
                | classify - Evaluates line against rules and returns response.
    '''

    _rules: list[IResponseClassificationRule]

    def __init__(
        self,
        rules: Sequence[IResponseClassificationRule] = (),
    ) -> None:
        '''
            Initializes registry with ordered rules.

            :param rules: Initial sequence of IResponseClassificationRule items.
            :exceptions: None.
        '''
        self._rules = list(rules)

    def register_rule(self, rule: IResponseClassificationRule) -> None:
        '''
            Appends a classification rule to the registry.

            :param rule: IResponseClassificationRule instance.
            :exceptions: None.
        '''
        self._rules.append(rule)

    def classify(self, clean_line: str) -> ScaraResponse:
        '''
            Evaluates line against rules in order and returns first match.

            :param clean_line: Clean stripped response line.
            :return: Matched ScaraResponse or default UNKNOWN response.
            :exceptions: None.
        '''
        for rule in self._rules:
            if rule.matches(clean_line):
                return rule.classify(clean_line)

        return ScaraResponse(
            response_type='UNKNOWN',
            message=clean_line,
            raw_line=clean_line,
            is_success=True,
        )
