# -*- coding: UTF-8 -*-

'''
Module
    iresponse_classification_registry_test.py
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
    Unit testing for IResponseClassificationRegistry protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.iresponse_classification_registry import IResponseClassificationRegistry
from scarajectory.infrastructure.classifier.iresponse_classification_rule import IResponseClassificationRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseClassificationRegistryStub:
    '''Structural test stub satisfying IResponseClassificationRegistry protocol.'''

    def register_rule(self, rule: IResponseClassificationRule) -> None:
        '''Appends a classification rule.'''
        _ = rule

    def classify(self, clean_line: str) -> ScaraResponse:
        '''Evaluates line against rules and returns response.'''
        _ = clean_line
        return ScaraResponse(
            response_type='ACK',
            message='',
            raw_line='',
            is_success=True,
        )


class IncompleteResponseClassificationRegistryStub:
    '''Incomplete test stub missing required classify method.'''

    def register_rule(self, rule: IResponseClassificationRule) -> None:
        '''Appends a classification rule.'''
        _ = rule

    def get_rules_count(self) -> int:
        '''Returns number of registered rules.'''
        return 0


class ResponseClassificationRegistryTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IResponseClassificationRegistry.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IResponseClassificationRegistry protocol.'''
        stub = ResponseClassificationRegistryStub()
        self.assertIsInstance(stub, IResponseClassificationRegistry)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IResponseClassificationRegistry protocol check.'''
        incomplete = IncompleteResponseClassificationRegistryStub()
        self.assertNotIsInstance(incomplete, IResponseClassificationRegistry)


if __name__ == '__main__':
    main()
