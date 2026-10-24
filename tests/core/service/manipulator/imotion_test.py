# -*- coding: UTF-8 -*-

'''
Module
    imotion_test.py
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
    Unit tests for IMotionController structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.manipulator.imotion import IMotionController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIMotionController(TestCase):
    '''
        Test cases verifying IMotionController protocol conformance.

        It defines:

            :methods:
                | test_protocol_isinstance_check - Verifies structural subtyping.
                | test_protocol_failure_on_missing_methods - Verifies failure.
    '''

    def test_protocol_isinstance_check(self) -> None:
        '''
            Verifies structural subtyping via isinstance.

            :exceptions: None.
        '''
        controller = MagicMock(spec=IMotionController)
        self.assertIsInstance(controller, IMotionController)

    def test_protocol_failure_on_missing_methods(self) -> None:
        '''
            Verifies isinstance returns False when methods are missing.

            :exceptions: None.
        '''
        self.assertNotIsInstance(object(), IMotionController)


if __name__ == '__main__':
    main()
