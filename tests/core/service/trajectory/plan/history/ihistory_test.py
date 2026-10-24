# -*- coding: UTF-8 -*-

'''
Module
    ihistory_test.py
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
    Unit tests for ITrajectoryPlanHistory structural protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyPlanHistory:
    '''Dummy class conforming structurally to ITrajectoryPlanHistory.'''

    def undo(self) -> bool:
        '''Reverts last state change.'''
        return True

    def redo(self) -> bool:
        '''Restores reverted state change.'''
        return True


class DummyIncompletePlanHistory:
    '''Dummy class failing structural conformance to ITrajectoryPlanHistory.'''

    def undo(self) -> bool:
        '''Reverts last state change.'''
        return True

    def extra_method(self) -> bool:
        '''Additional method preventing R0903 while omitting redo.'''
        return False


class TestITrajectoryPlanHistory(TestCase):
    '''Test cases verifying ITrajectoryPlanHistory protocol conformance.'''

    def test_structural_conformance(self) -> None:
        '''Tests that class conforming structurally is recognized as instance.'''
        instance = DummyPlanHistory()
        self.assertIsInstance(instance, ITrajectoryPlanHistory)

    def test_non_conformance(self) -> None:
        '''Tests that incomplete class is not recognized as instance.'''
        incomplete = DummyIncompletePlanHistory()
        self.assertNotIsInstance(incomplete, ITrajectoryPlanHistory)


if __name__ == '__main__':
    main()
