# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_test.py
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
    Unit tests for TrajectoryPlan domain model.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.trajectory_plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryPlan(unittest.TestCase):
    '''
        Test cases for TrajectoryPlan entity and observer notifications.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_add_and_count - Tests adding waypoints and count property.
                | test_update_and_remove - Tests point modification and removal.
                | test_selection - Tests waypoint selection tracking.
                | test_undo_redo - Tests plan history integration.
                | test_clear - Tests clearing all waypoints.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        self.plan = TrajectoryPlan()

    def test_add_and_count(self) -> None:
        '''
            Tests adding waypoints and count property.

            :exceptions: None.
        '''
        self.assertEqual(self.plan.count, 0)
        p1 = Waypoint(x=0.0, y=0.0, z=20.0, phi=0.0, speed=40.0)
        p2 = Waypoint(x=40.0, y=0.0, z=20.0, phi=0.0, speed=40.0)
        p3 = Waypoint(x=40.0, y=30.0, z=20.0, phi=0.0, speed=40.0)

        self.plan.add_point(p1)
        self.plan.add_point(p2)
        self.plan.add_point(p3)

        self.assertEqual(self.plan.count, 3)
        self.assertEqual(len(self.plan.waypoints), 3)

    def test_update_and_remove(self) -> None:
        '''
            Tests updating and removing waypoint elements.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=10.0)
        p2 = Waypoint(x=20.0, y=20.0, z=0.0, phi=0.0, speed=10.0)
        self.plan.set_waypoints([p1, p2])

        p1_mod = Waypoint(x=15.0, y=15.0, z=0.0, phi=0.0, speed=10.0)
        updated = self.plan.update_point(0, p1_mod)
        self.assertTrue(updated)
        self.assertEqual(self.plan.waypoints[0].x, 15.0)

        removed = self.plan.remove_point(0)
        self.assertTrue(removed)
        self.assertEqual(self.plan.count, 1)
        self.assertEqual(self.plan.waypoints[0].x, 20.0)

    def test_selection(self) -> None:
        '''
            Tests selection of waypoint indices.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=10.0)
        self.plan.add_point(p1)

        self.plan.set_selected_index(0)
        self.assertEqual(self.plan.selected_index, 0)

        self.plan.set_selected_index(-1)
        self.assertEqual(self.plan.selected_index, -1)

    def test_undo_redo(self) -> None:
        '''
            Tests undo and redo transaction integration on TrajectoryPlan.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=10.0)
        p2 = Waypoint(x=20.0, y=20.0, z=0.0, phi=0.0, speed=10.0)

        self.plan.add_point(p1)
        self.plan.add_point(p2)
        self.assertEqual(self.plan.count, 2)

        undone = self.plan.undo()
        self.assertTrue(undone)
        self.assertEqual(self.plan.count, 1)

        redone = self.plan.redo()
        self.assertTrue(redone)
        self.assertEqual(self.plan.count, 2)

    def test_clear(self) -> None:
        '''
            Tests clearing all waypoints.

            :exceptions: None.
        '''
        p1 = Waypoint(x=10.0, y=10.0, z=0.0, phi=0.0, speed=10.0)
        self.plan.add_point(p1)
        self.plan.clear()
        self.assertEqual(self.plan.count, 0)


if __name__ == '__main__':
    unittest.main()
