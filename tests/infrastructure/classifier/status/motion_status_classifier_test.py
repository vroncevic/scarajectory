# -*- coding: UTF-8 -*-

'''
Module
    motion_status_classifier_test.py
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
    Unit tests for MotionStatusClassifier and MotionStatusClassifierFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.protocol.scara_response import ScaraResponse
from scarajectory.infrastructure.classifier.status.imotion_status_classifier import IMotionStatusClassifier
from scarajectory.infrastructure.classifier.status.motion_status_classifier import MotionStatusClassifier
from scarajectory.infrastructure.classifier.status.motion_status_classifier_factory import MotionStatusClassifierFactory

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


class MotionStatusClassifierTestCase(TestCase):
    '''
        Tests for MotionStatusClassifier movement and action completion.

        It defines:

            :methods:
                | test_factory_and_protocol_conformance - Tests factory and structural protocol.
                | test_is_move_done - Tests waypoint move completion recognition.
                | test_is_move_failed - Tests waypoint move failure recognition.
                | test_is_action_done - Tests tool, wait, and auxiliary completion.
                | test_is_complete - Tests combined move and action completion.
    '''

    def test_factory_and_protocol_conformance(self) -> None:
        '''
            Tests factory and structural protocol.

            :exceptions: None.
        '''
        classifier = MotionStatusClassifierFactory.create()
        self.assertIsInstance(classifier, MotionStatusClassifier)
        self.assertIsInstance(classifier, IMotionStatusClassifier)
        self.assertEqual(MotionStatusClassifierFactory.get_version(), '1.0.3')

    def test_is_move_done(self) -> None:
        '''
            Tests waypoint move completion recognition.

            :exceptions: None.
        '''
        parser = StubResponseParser()
        classifier = MotionStatusClassifier(response_parser=parser)  # type: ignore[arg-type]

        parser.set_response(
            ScaraResponse(
                response_type='DONE',
                message='Move complete',
                raw_line='ok: DONE',
                is_success=True,
            )
        )
        self.assertTrue(classifier.is_move_done('ok: DONE'))

        parser.set_response(
            ScaraResponse(
                response_type='BUSY',
                message='Moving',
                raw_line='busy',
                is_success=True,
            )
        )
        self.assertFalse(classifier.is_move_done('busy'))

    def test_is_move_failed(self) -> None:
        '''
            Tests waypoint move failure recognition.

            :exceptions: None.
        '''
        parser = StubResponseParser()
        classifier = MotionStatusClassifier(response_parser=parser)  # type: ignore[arg-type]

        parser.set_response(
            ScaraResponse(
                response_type='MOVE_FAILED',
                message='Collision detected',
                raw_line='err: MOVE_FAILED',
                is_success=False,
            )
        )
        self.assertTrue(classifier.is_move_failed('err: MOVE_FAILED'))

        parser.set_response(
            ScaraResponse(
                response_type='DONE',
                message='',
                raw_line='ok',
                is_success=True,
            )
        )
        self.assertFalse(classifier.is_move_failed('ok'))

    def test_is_action_done(self) -> None:
        '''
            Tests tool, wait, and auxiliary completion.

            :exceptions: None.
        '''
        parser = StubResponseParser()
        classifier = MotionStatusClassifier(response_parser=parser)  # type: ignore[arg-type]

        self.assertTrue(classifier.is_action_done('info: WAIT_DONE'))
        self.assertTrue(classifier.is_action_done('ok: HOMED_SUCCESS'))
        self.assertTrue(classifier.is_action_done('<RESP:ACK#PUMP_ON>'))
        self.assertTrue(classifier.is_action_done('<RESP:ACK#VALVE_OPEN>'))
        self.assertTrue(classifier.is_action_done('<RESP:ACK#OVERRIDE=1>'))
        self.assertTrue(classifier.is_action_done('<RESP:ACK#ELBOW_UP>'))
        self.assertTrue(classifier.is_action_done('<RESP:ACK#MOTORS_ON>'))
        self.assertFalse(classifier.is_action_done('<RESP:ACK#OTHER>'))
        self.assertFalse(classifier.is_action_done('moving...'))

    def test_is_complete(self) -> None:
        '''
            Tests combined move and action completion.

            :exceptions: None.
        '''
        parser = StubResponseParser()
        classifier = MotionStatusClassifier(response_parser=parser)  # type: ignore[arg-type]

        # Case 1: is_move_done returns True
        parser.set_response(
            ScaraResponse(
                response_type='DONE',
                message='',
                raw_line='ok: DONE',
                is_success=True,
            )
        )
        self.assertTrue(classifier.is_complete('ok: DONE'))

        # Case 2: is_action_done returns True
        parser.set_response(
            ScaraResponse(
                response_type='ACK',
                message='',
                raw_line='<RESP:ACK#PUMP_OFF>',
                is_success=True,
            )
        )
        self.assertTrue(classifier.is_complete('<RESP:ACK#PUMP_OFF>'))

        # Case 3: neither is True
        parser.set_response(
            ScaraResponse(
                response_type='BUSY',
                message='',
                raw_line='busy',
                is_success=True,
            )
        )
        self.assertFalse(classifier.is_complete('busy'))


if __name__ == '__main__':
    main()
