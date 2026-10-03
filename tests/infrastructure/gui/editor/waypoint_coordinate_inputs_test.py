# -*- coding: UTF-8 -*-

'''
Module
    waypoint_coordinate_inputs_test.py
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
    Unit testing for WaypointCoordinateInputs value object.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.infrastructure.gui.editor.waypoint_coordinate_inputs import (
    WaypointCoordinateInputs,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointCoordinateInputsTestCase(TestCase):
    '''
        Unit tests for WaypointCoordinateInputs value object.

        It defines:

            :methods:
                | test_fields_access - Verifies raw string attributes accessibility.
                | test_immutability - Verifies container cannot be mutated after creation.
    '''

    def test_fields_access(self) -> None:
        '''Verifies raw string coordinate values are accessible via properties.'''
        inputs = WaypointCoordinateInputs(
            x='10.5',
            y='20.5',
            z='5.0',
            phi='45.0',
            speed='80.0',
        )
        self.assertEqual(inputs.x, '10.5')
        self.assertEqual(inputs.y, '20.5')
        self.assertEqual(inputs.z, '5.0')
        self.assertEqual(inputs.phi, '45.0')
        self.assertEqual(inputs.speed, '80.0')

    def test_immutability(self) -> None:
        '''Verifies instance attributes cannot be reassigned due to frozen state.'''
        inputs = WaypointCoordinateInputs(
            x='10.5',
            y='20.5',
            z='5.0',
            phi='45.0',
            speed='80.0',
        )
        with self.assertRaises(FrozenInstanceError):
            inputs.x = '99.0'


if __name__ == '__main__':
    main()
