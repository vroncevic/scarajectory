# -*- coding: UTF-8 -*-

'''
Module
    ivalidator_test.py
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
    Unit tests for native ITrajectoryValidator structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ITrajectoryValidatorTest(TestCase):
    '''
        Test cases for ITrajectoryValidator structural protocol verification.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies that mock conforms to protocol.
                | test_protocol_rejection - Verifies that non-conforming object is rejected.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that a valid implementation conforms to ITrajectoryValidator.

            :exceptions: None.
        '''
        validator = MagicMock(spec=ITrajectoryValidator)
        self.assertIsInstance(validator, ITrajectoryValidator)

    def test_protocol_rejection(self) -> None:
        '''
            Verifies that an incomplete implementation is rejected.

            :exceptions: None.
        '''
        self.assertNotIsInstance(object(), ITrajectoryValidator)


if __name__ == '__main__':
    main()
