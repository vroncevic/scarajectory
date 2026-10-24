# -*- coding: UTF-8 -*-

'''
Module
    navigator_test.py
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
    Unit tests for PlanHistoryNavigator undo/redo stack manager.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.navigator.inavigator import IPlanHistoryNavigator
from scarajectory.core.service.trajectory.history.navigator.navigator import PlanHistoryNavigator
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


class TestPlanHistoryNavigator(TestCase):
    '''
        Test cases for PlanHistoryNavigator stack operations.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_undo_redo_lifecycle - Tests undo and redo operations.
                | test_empty_stack_operations - Tests undo/redo on empty stacks.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        stack = PlanHistoryStack()
        navigator = PlanHistoryNavigator(stack)
        self.assertIsInstance(navigator, IPlanHistoryNavigator)

    def test_undo_redo_lifecycle(self) -> None:
        '''
            Tests undo, redo, and clear lifecycle.

            :exceptions: None.
        '''
        stack = PlanHistoryStack()
        navigator = PlanHistoryNavigator(stack)
        saver = PlanHistorySaver(stack)

        self.assertFalse(navigator.can_undo())
        self.assertFalse(navigator.can_redo())

        wp1 = TrajectoryWaypoint(
            x=10.0, y=20.0, z=0.0, speed=100.0, phi=0.0, name='', command=''
        )
        wp2 = TrajectoryWaypoint(
            x=30.0, y=40.0, z=0.0, speed=100.0, phi=0.0, name='', command=''
        )

        saver.save_state([wp1])
        self.assertTrue(navigator.can_undo())
        self.assertFalse(navigator.can_redo())

        undone = navigator.undo([wp1, wp2])
        self.assertEqual(len(undone), 1)
        self.assertTrue(navigator.can_redo())

        redone = navigator.redo(undone)
        self.assertEqual(len(redone), 2)

        saver.clear()
        self.assertFalse(navigator.can_undo())
        self.assertFalse(navigator.can_redo())

    def test_empty_stack_operations(self) -> None:
        '''
            Tests undo and redo on empty stacks return current state without error.

            :exceptions: None.
        '''
        stack = PlanHistoryStack()
        navigator = PlanHistoryNavigator(stack)
        current = [
            TrajectoryWaypoint(
                x=0.0, y=0.0, z=0.0, speed=10.0, phi=0.0, name='', command=''
            )
        ]

        undone = navigator.undo(current)
        self.assertEqual(undone, current)

        redone = navigator.redo(current)
        self.assertEqual(redone, current)


if __name__ == '__main__':
    main()
