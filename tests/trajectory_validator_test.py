# -*- coding: UTF-8 -*-

'''
Module
    trajectory_validator_test.py
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
    Unit tests for TrajectoryValidator.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.point import Point
from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory_validator import TrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryValidator(unittest.TestCase):
    '''
        Test cases for TrajectoryValidator kinematic validation.

        It defines:

            :methods:
                | setUp - Initializes validator fixture with standard SCARA dimensions.
                | test_reachable_point - Tests valid point inside annular workspace.
                | test_out_of_reach - Tests point exceeding maximum reach.
                | test_deadzone_point - Tests point located inside inner deadzone radius.
                | test_z_axis_limits - Tests vertical stroke boundaries.
                | test_validate_plan - Tests full trajectory plan validation report.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        self.bounds = ScaraBounds(l1=150.0, l2=120.0, z_min=0.0, z_max=100.0)
        self.validator = TrajectoryValidator(self.bounds)

    def test_reachable_point(self) -> None:
        '''
            Tests valid point inside reachable workspace.

            :exceptions: None.
        '''
        pt = Point(x=100.0, y=100.0, z=20.0, phi=0.0, speed=40.0)
        res = self.validator.validate_point_dto(pt)
        self.assertTrue(res.is_valid)

    def test_out_of_reach(self) -> None:
        '''
            Tests point outside maximum kinematic radius.

            :exceptions: None.
        '''
        pt = Point(x=250.0, y=250.0, z=20.0, phi=0.0, speed=40.0)
        res = self.validator.validate_point_dto(pt)
        self.assertFalse(res.is_valid)

    def test_deadzone_point(self) -> None:
        '''
            Tests point within inner deadzone singularity.

            :exceptions: None.
        '''
        pt = Point(x=10.0, y=10.0, z=20.0, phi=0.0, speed=40.0)
        res = self.validator.validate_point_dto(pt)
        self.assertFalse(res.is_valid)

    def test_z_axis_limits(self) -> None:
        '''
            Tests vertical stroke limit checks.

            :exceptions: None.
        '''
        pt_low = Point(x=100.0, y=100.0, z=-10.0, phi=0.0, speed=40.0)
        pt_high = Point(x=100.0, y=100.0, z=150.0, phi=0.0, speed=40.0)
        self.assertFalse(self.validator.validate_point_dto(pt_low).is_valid)
        self.assertFalse(self.validator.validate_point_dto(pt_high).is_valid)

    def test_validate_plan(self) -> None:
        '''
            Tests full trajectory plan validation.

            :exceptions: None.
        '''
        plan = TrajectoryPlan()
        plan.add_point(Waypoint(x=100.0, y=100.0, z=20.0, phi=0.0, speed=40.0))
        plan.add_point(Waypoint(x=120.0, y=120.0, z=20.0, phi=0.0, speed=40.0))

        is_valid, messages = self.validator.validate_plan(plan)
        self.assertTrue(is_valid)
        self.assertGreater(len(messages), 0)


if __name__ == '__main__':
    unittest.main()
