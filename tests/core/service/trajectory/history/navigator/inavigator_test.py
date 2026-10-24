# -*- coding: UTF-8 -*-

'''
Module
    inavigator_test.py
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
    Unit tests for IPlanHistoryNavigator structural protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.navigator.inavigator import IPlanHistoryNavigator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyPlanHistoryNavigator:
    '''Dummy class conforming structurally to IPlanHistoryNavigator.'''

    def undo(self, current: Sequence[TrajectoryWaypoint]) -> list[TrajectoryWaypoint]:
        '''Reverts last state change.'''
        return list(current)

    def redo(self, current: Sequence[TrajectoryWaypoint]) -> list[TrajectoryWaypoint]:
        '''Restores reverted state change.'''
        return list(current)

    def can_undo(self) -> bool:
        '''Checks if undo is possible.'''
        return True

    def can_redo(self) -> bool:
        '''Checks if redo is possible.'''
        return False


class IncompletePlanHistoryNavigator:
    '''Dummy class failing structural conformance to IPlanHistoryNavigator.'''

    def can_undo(self) -> bool:
        '''Checks if undo is possible.'''
        return True

    def extra_method(self) -> bool:
        '''Additional method preventing R0903 while omitting other methods.'''
        return False


class TestIPlanHistoryNavigator(TestCase):
    '''
        Test cases verifying IPlanHistoryNavigator protocol conformance.

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
        navigator = DummyPlanHistoryNavigator()
        self.assertIsInstance(navigator, IPlanHistoryNavigator)

    def test_protocol_failure_on_missing_methods(self) -> None:
        '''
            Verifies isinstance returns False when methods are missing.

            :exceptions: None.
        '''
        incomplete = IncompletePlanHistoryNavigator()
        self.assertNotIsInstance(incomplete, IPlanHistoryNavigator)


if __name__ == '__main__':
    main()
