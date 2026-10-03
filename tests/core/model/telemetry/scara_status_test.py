# -*- coding: UTF-8 -*-

'''
Module
    scara_status_test.py
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
    Unit tests for ScaraStatus immutable telemetry value object.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.scara_status import ScaraStatus

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraStatusTestCase(TestCase):
    '''
        Tests for ScaraStatus telemetry data model.

        It defines:

            :methods:
                | test_status_creation - Verifies telemetry attribute values.
                | test_status_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_status_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        status = ScaraStatus(
            system_state=1,
            is_busy=True,
            queue_count=4,
            j1_steps=1200,
            j2_steps=2400,
            z_steps=-500,
            j4_steps=180,
        )
        self.assertEqual(status.system_state, 1)
        self.assertTrue(status.is_busy)
        self.assertEqual(status.queue_count, 4)
        self.assertEqual(status.j1_steps, 1200)
        self.assertEqual(status.j2_steps, 2400)
        self.assertEqual(status.z_steps, -500)
        self.assertEqual(status.j4_steps, 180)

    def test_status_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen ScaraStatus raises FrozenInstanceError.

            :exceptions: None.
        '''
        status = ScaraStatus(
            system_state=0,
            is_busy=False,
            queue_count=0,
            j1_steps=0,
            j2_steps=0,
            z_steps=0,
            j4_steps=0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(status, 'is_busy', True)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical ScaraStatus instances.

            :exceptions: None.
        '''
        s1 = ScaraStatus(
            system_state=0,
            is_busy=False,
            queue_count=0,
            j1_steps=100,
            j2_steps=200,
            z_steps=300,
            j4_steps=400,
        )
        s2 = ScaraStatus(
            system_state=0,
            is_busy=False,
            queue_count=0,
            j1_steps=100,
            j2_steps=200,
            z_steps=300,
            j4_steps=400,
        )
        self.assertEqual(s1, s2)


if __name__ == '__main__':
    main()
