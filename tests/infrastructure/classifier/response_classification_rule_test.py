# -*- coding: UTF-8 -*-

'''
Module
    response_classification_rule_test.py
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
    Unit tests for ResponseClassificationRule and its protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.iresponse_classification_rule \
    import (
        IResponseClassificationRule
    )
from scarajectory.infrastructure.classifier.response_classification_rule \
    import (
        ResponseClassificationRule
    )

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestResponseClassificationRule(TestCase):
    '''
        Test cases verifying ResponseClassificationRule behavior.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies rule implements IResponseClassificationRule.
        '''
        rule = ResponseClassificationRule(
            'TEST', lambda s: s.startswith('TEST')
        )
        self.assertIsInstance(rule, IResponseClassificationRule)

    def test_matches_positive_and_negative(self) -> None:
        '''
            Tests matches returns True for matching string and False otherwise.
        '''
        rule = ResponseClassificationRule(
            'ACK', lambda s: s.startswith('<ACK')
        )
        self.assertTrue(rule.matches('<ACK>'))
        self.assertFalse(rule.matches('<NACK>'))

    def test_classify_stripped_message(self) -> None:
        '''
            Tests classify strips wrapping angle brackets by default.
        '''
        rule = ResponseClassificationRule(
            'ACK', lambda s: s.startswith('<ACK'), is_success=True
        )
        resp: ScaraResponse = rule.classify('<ACK#1>')
        self.assertEqual(resp.response_type, 'ACK')
        self.assertEqual(resp.message, 'ACK#1')
        self.assertEqual(resp.raw_line, '<ACK#1>')
        self.assertTrue(resp.is_success)

    def test_classify_preserved_message(self) -> None:
        '''
            Tests classify preserves delimiters when preserve_clean_msg=True.
        '''
        rule = ResponseClassificationRule(
            'DONE',
            lambda s: s == '<DONE>',
            is_success=True,
            preserve_clean_msg=True,
        )
        resp: ScaraResponse = rule.classify('<DONE>')
        self.assertEqual(resp.response_type, 'DONE')
        self.assertEqual(resp.message, '<DONE>')
        self.assertTrue(resp.is_success)

    def test_classify_failure_flag(self) -> None:
        '''
            Tests classify propagates is_success=False.
        '''
        rule = ResponseClassificationRule(
            'ERR',
            lambda s: 'ERR' in s,
            is_success=False,
            preserve_clean_msg=True,
        )
        resp: ScaraResponse = rule.classify('<ERR#TIMEOUT>')
        self.assertEqual(resp.response_type, 'ERR')
        self.assertFalse(resp.is_success)


if __name__ == '__main__':
    main()
