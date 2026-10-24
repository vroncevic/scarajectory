# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for PacingDependencies dataclass bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaracom.flow.barrier.barrier import FlowBarrier

from scarajectory.infrastructure.pacing.dependencies import PacingDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PacingDependenciesTestCase(TestCase):
    '''
        Unit tests validating PacingDependencies bundle.

        It defines:

            :methods:
                | test_dependencies_defaults - Verifies default parameters and attribute storage.
                | test_dependencies_custom_capacity_and_immutability - Verifies custom capacity and frozen immutability.
    '''

    def test_dependencies_defaults(self) -> None:
        '''
            Verifies default parameters and attribute storage.

            :exceptions: None.
        '''
        barrier = FlowBarrier()
        deps = PacingDependencies(flow_barrier=barrier)

        self.assertIs(deps.flow_barrier, barrier)
        self.assertEqual(deps.capacity, 16)

    def test_dependencies_custom_capacity_and_immutability(self) -> None:
        '''
            Verifies custom capacity and frozen immutability.

            :exceptions: None.
        '''
        barrier = FlowBarrier()
        deps = PacingDependencies(
            flow_barrier=barrier,
            capacity=24,
        )

        self.assertEqual(deps.capacity, 24)
        with self.assertRaises(FrozenInstanceError):
            deps.capacity = 48  # type: ignore[misc]


if __name__ == '__main__':
    main()
