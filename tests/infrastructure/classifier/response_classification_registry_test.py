# -*- coding: UTF-8 -*-

'''
Module
    response_classification_registry_test.py
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
    Unit tests for ResponseClassificationRegistry and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.response_classification_registry import ResponseClassificationRegistry
from scarajectory.infrastructure.classifier.response_classification_registry_factory import ResponseClassificationRegistryFactory
from scarajectory.infrastructure.classifier.response_classification_rule import ResponseClassificationRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestResponseClassificationRegistry(TestCase):
    '''
        Test cases verifying ResponseClassificationRegistry behavior.
    '''

    def test_custom_registry_registration_and_classify(self) -> None:
        '''
            Tests registering rule and classifying response.
        '''
        registry = ResponseClassificationRegistry()
        registry.register_rule(
            ResponseClassificationRule('CUSTOM', lambda s: 'CUSTOM' in s)
        )
        resp: ScaraResponse = registry.classify('<CUSTOM_MESSAGE>')
        self.assertEqual(resp.response_type, 'CUSTOM')
        self.assertEqual(resp.message, 'CUSTOM_MESSAGE')

    def test_initial_rules_sequence(self) -> None:
        '''
            Tests initializing registry with a tuple of rules directly.
        '''
        rule = ResponseClassificationRule('INIT_TEST', lambda s: 'INIT' in s)
        registry = ResponseClassificationRegistry((rule,))
        resp: ScaraResponse = registry.classify('INIT_MSG')
        self.assertEqual(resp.response_type, 'INIT_TEST')

    def test_unknown_fallback(self) -> None:
        '''
            Tests fallback to UNKNOWN for unhandled strings.
        '''
        registry = ResponseClassificationRegistry()
        resp: ScaraResponse = registry.classify('SOME_RANDOM_TEXT')
        self.assertEqual(resp.response_type, 'UNKNOWN')
        self.assertEqual(resp.message, 'SOME_RANDOM_TEXT')
        self.assertTrue(resp.is_success)

    def test_factory_standard_rules(self) -> None:
        '''
            Tests factory produces registry with all standard protocol rules.
        '''
        registry: ResponseClassificationRegistry = (
            ResponseClassificationRegistryFactory.create()
        )

        ack = registry.classify('<RESP:ACK#QUEUE=2>')
        self.assertEqual(ack.response_type, 'ACK')
        self.assertTrue(ack.is_success)

        nack = registry.classify('<RESP:NACK#ERR>')
        self.assertEqual(nack.response_type, 'NACK')
        self.assertFalse(nack.is_success)

        done = registry.classify('<DONE>')
        self.assertEqual(done.response_type, 'DONE')
        self.assertEqual(done.message, '<DONE>')

        err = registry.classify('<ERR#TIMEOUT>')
        self.assertEqual(err.response_type, 'ERR')
        self.assertFalse(err.is_success)

        homed = registry.classify('HOMED_SUCCESS')
        self.assertEqual(homed.response_type, 'HOMED')

        homed_fail = registry.classify('HOMING_FAILED')
        self.assertEqual(homed_fail.response_type, 'HOMED_FAIL')
        self.assertFalse(homed_fail.is_success)


if __name__ == '__main__':
    main()
