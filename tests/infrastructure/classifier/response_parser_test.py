# -*- coding: UTF-8 -*-

'''
Module
    response_parser_test.py
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
    Unit tests for ResponseParser and ResponseParserFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.iresponse_parser import IResponseParser
from scarajectory.infrastructure.classifier.response_parser import ResponseParser
from scarajectory.infrastructure.classifier.response_parser_factory import ResponseParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestResponseParser(TestCase):
    '''
        Test cases verifying ResponseParser protocol and decoding methods.
    '''

    def setUp(self) -> None:
        self.parser: ResponseParser = ResponseParserFactory.create()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that ResponseParser satisfies IResponseParser.
        '''
        self.assertIsInstance(self.parser, IResponseParser)

    def test_parse_response_ack_and_queue(self) -> None:
        '''
            Tests parsing ACK packet with queue depth metadata.
        '''
        resp: ScaraResponse = self.parser.parse_response(
            '<RESP:ACK#QUEUE=3>'
        )
        self.assertEqual(resp.response_type, 'ACK')
        self.assertTrue(resp.is_success)
        self.assertTrue(self.parser.has_queue_depth('<RESP:ACK#QUEUE=3>'))
        self.assertEqual(
            self.parser.parse_queue_depth('<RESP:ACK#QUEUE=3>'), 3
        )

    def test_has_queue_depth_false(self) -> None:
        '''
            Tests has_queue_depth returns False for non-ACK or lines without
            depth.
        '''
        self.assertFalse(self.parser.has_queue_depth('<RESP:ERR#FAIL>'))
        self.assertEqual(
            self.parser.parse_queue_depth('<RESP:ERR#FAIL>'), 0
        )

    def test_parse_various_responses(self) -> None:
        '''
            Tests parsing config, elbow, nack, and status responses.
        '''
        cfg = self.parser.parse_response('<RESP:CONFIG#R_MAX=300>')
        self.assertEqual(cfg.response_type, 'CONFIG')

        elbow = self.parser.parse_response('<RESP:ELBOW#LEFT>')
        self.assertEqual(elbow.response_type, 'ELBOW')

        nack = self.parser.parse_response('<RESP:NACK#INVALID>')
        self.assertEqual(nack.response_type, 'NACK')
        self.assertFalse(nack.is_success)


if __name__ == '__main__':
    main()
