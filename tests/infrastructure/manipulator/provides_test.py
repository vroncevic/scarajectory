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
    Unit tests for ManipulatorProvides output dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.core.service.manipulator.iquery import IQueryController
from scarajectory.infrastructure.manipulator.provides import ManipulatorProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorProvidesTestCase(TestCase):
    '''
        Tests verifying ManipulatorProvides creation and immutability.
    '''

    def test_provides_attributes(self) -> None:
        '''
            Verifies attribute assignments.

            :exceptions: None.
        '''
        jog = MagicMock(spec=IJogController)
        motion = MagicMock(spec=IMotionController)
        query = MagicMock(spec=IQueryController)
        provides = ManipulatorProvides(
            jog_controller=jog,
            motion_controller=motion,
            query_controller=query,
        )
        self.assertIs(provides.jog_controller, jog)
        self.assertIs(provides.motion_controller, motion)
        self.assertIs(provides.query_controller, query)

    def test_provides_immutability(self) -> None:
        '''
            Verifies frozen dataclass behavior.

            :exceptions: None.
        '''
        provides = ManipulatorProvides(
            jog_controller=MagicMock(spec=IJogController),
            motion_controller=MagicMock(spec=IMotionController),
            query_controller=MagicMock(spec=IQueryController),
        )
        with self.assertRaises(FrozenInstanceError):
            provides.jog_controller = MagicMock(spec=IJogController)  # type: ignore[misc]


if __name__ == '__main__':
    main()
