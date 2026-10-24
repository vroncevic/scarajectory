# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for MotionProvides output container dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.infrastructure.manipulator.motion.provides import MotionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionProvidesTestCase(TestCase):
    '''
        Tests verifying MotionProvides creation and immutability.
    '''

    def test_provides_attributes(self) -> None:
        '''
            Verifies controller attribute assignment.

            :exceptions: None.
        '''
        mock_controller = MagicMock(spec=IMotionController)
        provides = MotionProvides(motion_controller=mock_controller)
        self.assertIs(provides.motion_controller, mock_controller)

    def test_provides_immutability(self) -> None:
        '''
            Verifies frozen dataclass behavior.

            :exceptions: None.
        '''
        provides = MotionProvides(motion_controller=MagicMock(spec=IMotionController))
        with self.assertRaises(FrozenInstanceError):
            provides.motion_controller = MagicMock(spec=IMotionController)  # type: ignore[misc]


if __name__ == '__main__':
    main()
