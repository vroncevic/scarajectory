# -*- coding: UTF-8 -*-

'''
Module
    flow_status_classifier_test.py
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
    Unit tests for FlowStatusClassifier and FlowStatusClassifierFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.status.iflow_status_classifier import IFlowStatusClassifier
from scarajectory.infrastructure.classifier.status.flow_status_classifier import FlowStatusClassifier
from scarajectory.infrastructure.classifier.status.flow_status_classifier_factory import FlowStatusClassifierFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubResponseParser:
    '''
        Structural stub for ASCII response parser.
    '''

    def __init__(self) -> None:
        self.response = ScaraResponse(
            response_type='OK',
            message='',
            raw_line='',
            is_success=True,
        )

    def parse_response(self, line: str) -> ScaraResponse:
        '''Returns configured ScaraResponse.'''
        _ = line
        return self.response

    def set_response(self, response: ScaraResponse) -> None:
        '''Configures response to return.'''
        self.response = response


class FlowStatusClassifierTestCase(TestCase):
    '''
        Tests for FlowStatusClassifier buffer and safety classification.

        It defines:

            :methods:
                | test_factory_and_protocol_conformance - Tests factory creation and protocol matching.
                | test_is_buffer_full - Tests buffer saturation classification.
                | test_is_error - Tests error and fault condition classification.
                | test_is_telemetry - Tests telemetry packet classification.
    '''

    def test_factory_and_protocol_conformance(self) -> None:
        '''
            Tests factory creation and protocol matching.

            :exceptions: None.
        '''
        classifier = FlowStatusClassifierFactory.create()
        self.assertIsInstance(classifier, FlowStatusClassifier)
        self.assertIsInstance(classifier, IFlowStatusClassifier)
        self.assertEqual(FlowStatusClassifierFactory.get_version(), '1.0.3')

    def test_is_buffer_full(self) -> None:
        '''
            Tests buffer saturation classification.

            :exceptions: None.
        '''
        parser = StubResponseParser()
        classifier = FlowStatusClassifier(response_parser=parser)  # type: ignore[arg-type]

        parser.set_response(
            ScaraResponse(
                response_type='FULL',
                message='Buffer queue full',
                raw_line='<RESP:FULL#BUFFER_FULL>',
                is_success=False,
            )
        )
        self.assertTrue(classifier.is_buffer_full('<RESP:FULL#BUFFER_FULL>'))

        parser.set_response(
            ScaraResponse(
                response_type='OK',
                message='Ready',
                raw_line='ok',
                is_success=True,
            )
        )
        self.assertFalse(classifier.is_buffer_full('ok'))

    def test_is_error(self) -> None:
        '''
            Tests error and fault condition classification.

            :exceptions: None.
        '''
        parser = StubResponseParser()
        classifier = FlowStatusClassifier(response_parser=parser)  # type: ignore[arg-type]

        parser.set_response(
            ScaraResponse(
                response_type='ERR',
                message='Motion error',
                raw_line='err: invalid target',
                is_success=False,
            )
        )
        self.assertTrue(classifier.is_error('err: invalid target'))

        parser.set_response(
            ScaraResponse(
                response_type='OK',
                message='',
                raw_line='ok',
                is_success=True,
            )
        )
        self.assertFalse(classifier.is_error('ok'))

    def test_is_telemetry(self) -> None:
        '''
            Tests telemetry packet classification.

            :exceptions: None.
        '''
        parser = StubResponseParser()
        classifier = FlowStatusClassifier(response_parser=parser)  # type: ignore[arg-type]

        parser.set_response(
            ScaraResponse(
                response_type='TELEM',
                message='x=10 y=20',
                raw_line='<TELEM:10,20>',
                is_success=True,
            )
        )
        self.assertTrue(classifier.is_telemetry('<TELEM:10,20>'))

        parser.set_response(
            ScaraResponse(
                response_type='OK',
                message='',
                raw_line='ok',
                is_success=True,
            )
        )
        self.assertFalse(classifier.is_telemetry('ok'))


if __name__ == '__main__':
    main()
