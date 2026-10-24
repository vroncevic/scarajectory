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
    Unit tests for JogProvides output container dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.infrastructure.manipulator.jog.provides import JogProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogProvidesTestCase(TestCase):
    '''
        Tests verifying JogProvides creation and immutability.
    '''

    def test_provides_attributes(self) -> None:
        '''
            Verifies controller attribute assignment.

            :exceptions: None.
        '''
        mock_controller = MagicMock(spec=IJogController)
        provides = JogProvides(jog_controller=mock_controller)
        self.assertIs(provides.jog_controller, mock_controller)

    def test_provides_immutability(self) -> None:
        '''
            Verifies frozen dataclass behavior.

            :exceptions: None.
        '''
        provides = JogProvides(jog_controller=MagicMock(spec=IJogController))
        with self.assertRaises(FrozenInstanceError):
            provides.jog_controller = MagicMock(spec=IJogController)  # type: ignore[misc]


if __name__ == '__main__':
    main()
