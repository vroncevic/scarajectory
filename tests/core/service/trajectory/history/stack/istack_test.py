# -*- coding: UTF-8 -*-

'''
Module
    istack_test.py
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
    Unit tests for IPlanHistoryStack structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.stack.istack import IPlanHistoryStack

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyPlanHistoryStack:
    '''Dummy class conforming structurally to IPlanHistoryStack.'''

    @property
    def undo_stack(self) -> list[list[TrajectoryWaypoint]]:
        '''Returns undo stack.'''
        return []

    @property
    def redo_stack(self) -> list[list[TrajectoryWaypoint]]:
        '''Returns redo stack.'''
        return []

    def clear(self) -> None:
        '''Clears history stacks.'''


class IncompletePlanHistoryStack:
    '''Dummy class failing structural conformance to IPlanHistoryStack.'''

    def clear(self) -> None:
        '''Clears history stacks.'''

    def extra_method(self) -> bool:
        '''Additional method preventing R0903 while omitting stack properties.'''
        return False


class TestIPlanHistoryStack(TestCase):
    '''
        Test cases verifying IPlanHistoryStack protocol conformance.

        It defines:

            :methods:
                | test_protocol_isinstance_check - Verifies structural subtyping via isinstance.
                | test_protocol_failure_on_missing_methods - Verifies isinstance returns False when incomplete.
    '''

    def test_protocol_isinstance_check(self) -> None:
        '''
            Verifies structural subtyping via isinstance.

            :exceptions: None.
        '''
        stack = DummyPlanHistoryStack()
        self.assertIsInstance(stack, IPlanHistoryStack)

    def test_protocol_failure_on_missing_methods(self) -> None:
        '''
            Verifies isinstance returns False when methods are missing.

            :exceptions: None.
        '''
        incomplete = IncompletePlanHistoryStack()
        self.assertNotIsInstance(incomplete, IPlanHistoryStack)


if __name__ == '__main__':
    main()
