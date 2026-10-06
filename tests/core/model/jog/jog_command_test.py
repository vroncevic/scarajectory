# -*- coding: UTF-8 -*-

'''
Module
    jog_command_test.py
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
    Unit tests for JogCommand immutable data model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.jog.jog_axis import JogAxis
from scarajectory.core.model.jog.jog_direction import JogDirection
from scarajectory.core.model.jog.jog_command import JogCommand

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogCommandTestCase(TestCase):
    '''
        Tests for JogCommand data container creation and immutability.

        It defines:

            :methods:
                | test_command_creation - Verifies attribute assignment on creation.
                | test_command_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality between instances.
    '''

    def test_command_creation(self) -> None:
        '''
            Verifies attribute values assigned during initialization.

            :exceptions: None.
        '''
        command = JogCommand(
            axis=JogAxis.X,
            direction=JogDirection.POSITIVE,
            step_mm=10.0,
            feedrate=100.0,
        )
        self.assertEqual(command.axis, JogAxis.X)
        self.assertEqual(command.direction, JogDirection.POSITIVE)
        self.assertEqual(command.step_mm, 10.0)
        self.assertEqual(command.feedrate, 100.0)

    def test_command_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen JogCommand raises FrozenInstanceError.

            :exceptions: None.
        '''
        command = JogCommand(
            axis=JogAxis.Z,
            direction=JogDirection.NEGATIVE,
            step_mm=5.0,
            feedrate=50.0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(command, 'step_mm', 20.0)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical JogCommand instances.

            :exceptions: None.
        '''
        cmd1 = JogCommand(
            axis=JogAxis.Y,
            direction=JogDirection.POSITIVE,
            step_mm=15.0,
            feedrate=80.0,
        )
        cmd2 = JogCommand(
            axis=JogAxis.Y,
            direction=JogDirection.POSITIVE,
            step_mm=15.0,
            feedrate=80.0,
        )
        self.assertEqual(cmd1, cmd2)


if __name__ == '__main__':
    main()
