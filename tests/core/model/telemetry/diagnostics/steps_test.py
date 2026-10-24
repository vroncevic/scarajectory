# -*- coding: UTF-8 -*-

'''
Module
    steps_test.py
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
    Unit tests for JointStepsDiagnostics immutable telemetry model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.steps import JointStepsDiagnostics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointStepsDiagnosticsTestCase(TestCase):
    '''
        Tests for JointStepsDiagnostics telemetry model.

        It defines:

            :methods:
                | test_steps_creation - Verifies attribute assignment during initialization.
                | test_steps_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_steps_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        steps = JointStepsDiagnostics(
            j1=5000,
            j2=4000,
            z=1000,
            j4=500,
        )
        self.assertEqual(steps.j1, 5000)
        self.assertEqual(steps.j2, 4000)
        self.assertEqual(steps.z, 1000)
        self.assertEqual(steps.j4, 500)

    def test_steps_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen JointStepsDiagnostics raises FrozenInstanceError.

            :exceptions: None.
        '''
        steps = JointStepsDiagnostics(
            j1=0,
            j2=0,
            z=0,
            j4=0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(steps, 'j1', 10)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical JointStepsDiagnostics instances.

            :exceptions: None.
        '''
        s1 = JointStepsDiagnostics(
            j1=100,
            j2=200,
            z=300,
            j4=400,
        )
        s2 = JointStepsDiagnostics(
            j1=100,
            j2=200,
            z=300,
            j4=400,
        )
        self.assertEqual(s1, s2)


if __name__ == '__main__':
    main()
