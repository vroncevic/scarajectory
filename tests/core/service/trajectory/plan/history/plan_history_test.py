# -*- coding: UTF-8 -*-

'''
Module
    plan_history_test.py
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
    Unit tests for PlanHistory undo/redo transaction manager.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.history.plan_history import PlanHistory
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.history.iplan_history import IPlanHistory
from scarajectory.core.service.trajectory.history.iplan_history_saver import IPlanHistorySaver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanHistory(TestCase):
    '''
        Test cases for PlanHistory undo/redo mechanism.

        It defines:

            :methods:
                | test_initial_state - Tests that initial history stacks return False and empty.
                | test_save_state_and_undo - Tests snapshot creation and undo restore.
                | test_redo - Tests redo forward stack restoration.
                | test_clear - Tests history reset.
                | test_factory_and_protocol_conformance - Tests factory instantiation and protocol conformance.
    '''

    def test_initial_state(self) -> None:
        '''
            Tests initial state of undo/redo availability.

            :exceptions: None.
        '''
        history = PlanHistory()
        pt = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.assertFalse(history.can_undo())
        self.assertFalse(history.can_redo())
        self.assertEqual(history.undo([pt]), [pt])
        self.assertEqual(history.redo([pt]), [pt])

    def test_save_state_and_undo(self) -> None:
        '''
            Tests saving state and performing undo operation.

            :exceptions: None.
        '''
        history = PlanHistory()
        pt1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        pt2 = Waypoint(x=30.0, y=40.0, z=0.0, phi=0.0, speed=10.0)

        history.save_state([pt1])
        self.assertTrue(history.can_undo())
        self.assertFalse(history.can_redo())

        restored = history.undo([pt1, pt2])
        self.assertEqual(len(restored), 1)
        self.assertEqual(restored[0].x, 10.0)
        self.assertFalse(history.can_undo())
        self.assertTrue(history.can_redo())

    def test_redo(self) -> None:
        '''
            Tests redoing a previously undone state.

            :exceptions: None.
        '''
        history = PlanHistory()
        pt1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        pt2 = Waypoint(x=30.0, y=40.0, z=0.0, phi=0.0, speed=10.0)

        history.save_state([pt1])
        history.undo([pt1, pt2])
        self.assertTrue(history.can_redo())

        redone = history.redo([pt1])
        self.assertEqual(len(redone), 2)
        self.assertFalse(history.can_redo())
        self.assertTrue(history.can_undo())

    def test_clear(self) -> None:
        '''
            Tests clearing history stacks.

            :exceptions: None.
        '''
        history = PlanHistory()
        pt1 = Waypoint(x=10.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        history.save_state([pt1])
        history.clear()
        self.assertFalse(history.can_undo())
        self.assertFalse(history.can_redo())
        self.assertEqual(history.undo([pt1]), [pt1])
        self.assertEqual(history.redo([pt1]), [pt1])

    def test_factory_and_protocol_conformance(self) -> None:
        '''
            Tests factory creation and IPlanHistory protocol conformance.

            :exceptions: None.
        '''
        history = PlanHistoryFactory.create()
        self.assertIsInstance(history, PlanHistory)
        self.assertIsInstance(history, IPlanHistory)
        self.assertIsInstance(history, IPlanHistorySaver)


if __name__ == '__main__':
    main()
