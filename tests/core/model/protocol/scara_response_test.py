# -*- coding: UTF-8 -*-

'''
Module
    scara_response_test.py
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
    Unit tests for ScaraResponse parsed microcontroller response data model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.protocol.scara_response import ScaraResponse

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraResponseTestCase(TestCase):
    '''
        Tests for ScaraResponse immutable data container.

        It defines:

            :methods:
                | test_response_creation - Verifies field values upon initialization.
                | test_response_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across identical responses.
    '''

    def test_response_creation(self) -> None:
        '''
            Verifies field values upon initialization.

            :exceptions: None.
        '''
        response = ScaraResponse(
            response_type='ACK',
            message='Command acknowledged',
            raw_line='ok: ACK',
            is_success=True,
        )
        self.assertEqual(response.response_type, 'ACK')
        self.assertEqual(response.message, 'Command acknowledged')
        self.assertEqual(response.raw_line, 'ok: ACK')
        self.assertTrue(response.is_success)

    def test_response_immutability(self) -> None:
        '''
            Verifies frozen instance constraints.

            :exceptions: None.
        '''
        response = ScaraResponse(
            response_type='ERR',
            message='Invalid axis',
            raw_line='err: axis out of bounds',
            is_success=False,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(response, 'is_success', True)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical responses.

            :exceptions: None.
        '''
        resp1 = ScaraResponse(
            response_type='POS',
            message='X:100 Y:50',
            raw_line='pos: 100 50',
            is_success=True,
        )
        resp2 = ScaraResponse(
            response_type='POS',
            message='X:100 Y:50',
            raw_line='pos: 100 50',
            is_success=True,
        )
        self.assertEqual(resp1, resp2)


if __name__ == '__main__':
    main()
