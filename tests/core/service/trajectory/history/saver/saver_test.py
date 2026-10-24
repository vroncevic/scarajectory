# -*- coding: UTF-8 -*-

'''
Module
    saver_test.py
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
    Unit tests for PlanHistorySaver class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.saver.isaver import IPlanHistorySaver
from scarajectory.core.service.trajectory.history.saver.saver import PlanHistorySaver
from scarajectory.core.service.trajectory.history.stack.stack import PlanHistoryStack

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanHistorySaver(TestCase):
    '''
        Test cases for PlanHistorySaver state saving operations.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_save_state_and_clear - Tests saving snapshots and clearing history.
                | test_undo_stack_overflow - Tests stack limit of 50 states.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        stack = PlanHistoryStack()
        saver = PlanHistorySaver(stack)
        self.assertIsInstance(saver, IPlanHistorySaver)

    def test_save_state_and_clear(self) -> None:
        '''
            Tests saving snapshots and clearing history.

            :exceptions: None.
        '''
        stack = PlanHistoryStack()
        saver = PlanHistorySaver(stack)
        wp = TrajectoryWaypoint(
            x=10.0, y=20.0, z=0.0, phi=0.0, speed=50.0, name='', command=''
        )
        saver.save_state([wp])
        self.assertEqual(len(stack.undo_stack), 1)

        saver.clear()
        self.assertEqual(len(stack.undo_stack), 0)
        self.assertEqual(len(stack.redo_stack), 0)

    def test_undo_stack_overflow(self) -> None:
        '''
            Tests stack limit of 50 states.

            :exceptions: None.
        '''
        stack = PlanHistoryStack()
        saver = PlanHistorySaver(stack)
        for i in range(60):
            wp = TrajectoryWaypoint(
                x=float(i), y=0.0, z=0.0, phi=0.0, speed=50.0, name='', command=''
            )
            saver.save_state([wp])

        self.assertEqual(len(stack.undo_stack), 50)


if __name__ == '__main__':
    main()
