# -*- coding: UTF-8 -*-

'''
Module
    ibulk_mutation_test.py
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
    Unit tests for IPlanBulkMutator structural protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyBulkMutator:
    '''Dummy class conforming structurally to IPlanBulkMutator.'''

    def clear(self) -> None:
        '''Clears all waypoints.'''

    def set_waypoints(self, waypoints: Sequence[TrajectoryWaypoint]) -> None:
        '''Sets waypoints sequence.'''
        _ = waypoints


class DummyIncompleteBulkMutator:
    '''Dummy class missing set_waypoints method.'''

    def other_operation(self) -> None:
        '''Performs other operation.'''

    def clear(self) -> None:
        '''Clears all waypoints.'''


class TestIPlanBulkMutator(TestCase):
    '''
        Test cases for IPlanBulkMutator protocol.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies protocol structural subtyping.
                | test_invalid_conformance - Verifies rejection of incomplete implementation.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies protocol structural subtyping.

            :exceptions: None.
        '''
        mutator = DummyBulkMutator()
        self.assertIsInstance(mutator, IPlanBulkMutator)

    def test_invalid_conformance(self) -> None:
        '''
            Verifies rejection of incomplete implementation.

            :exceptions: None.
        '''
        mutator = DummyIncompleteBulkMutator()
        self.assertNotIsInstance(mutator, IPlanBulkMutator)


if __name__ == '__main__':
    main()
