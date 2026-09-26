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

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.discretization.waypoint_factory import WaypointFactory
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scarajectory.core.service.trajectory.validation.trajectory_validator import TrajectoryValidator
from scarajectory.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryValidator(TestCase):
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
        self.bounds = ScaraConfigLoaderFactory.create().load_bounds_with_options(
            options={'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
        )
        self.kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        self.validator = TrajectoryValidatorFactory.create(kinematics=self.kinematics)

    def test_reachable_point(self) -> None:
        '''
            Tests valid point inside reachable workspace.

            :exceptions: None.
        '''
        pt = WaypointFactory.create(x=100.0, y=100.0, z=20.0, phi=0.0, speed=40.0)
        res = self.validator.validate_point(pt)
        self.assertTrue(res.is_valid)

    def test_out_of_reach(self) -> None:
        '''
            Tests point outside maximum kinematic radius.

            :exceptions: None.
        '''
        pt = WaypointFactory.create(x=250.0, y=250.0, z=20.0, phi=0.0, speed=40.0)
        res = self.validator.validate_point(pt)
        self.assertFalse(res.is_valid)

    def test_deadzone_point(self) -> None:
        '''
            Tests point within inner deadzone singularity.

            :exceptions: None.
        '''
        pt = WaypointFactory.create(x=10.0, y=10.0, z=20.0, phi=0.0, speed=40.0)
        res = self.validator.validate_point(pt)
        self.assertFalse(res.is_valid)

    def test_z_axis_limits(self) -> None:
        '''
            Tests vertical stroke limit checks.

            :exceptions: None.
        '''
        pt_low = WaypointFactory.create(x=100.0, y=100.0, z=-10.0, phi=0.0, speed=40.0)
        pt_high = WaypointFactory.create(x=100.0, y=100.0, z=150.0, phi=0.0, speed=40.0)
        self.assertFalse(self.validator.validate_point(pt_low).is_valid)
        self.assertFalse(self.validator.validate_point(pt_high).is_valid)

    def test_validate_plan(self) -> None:
        '''
            Tests full trajectory plan validation.

            :exceptions: None.
        '''
        plan = TrajectoryPlanFactory.create()
        plan.add_point(WaypointFactory.create(x=100.0, y=100.0, z=20.0, phi=0.0, speed=40.0))
        plan.add_point(WaypointFactory.create(x=120.0, y=120.0, z=20.0, phi=0.0, speed=40.0))

        is_valid, messages = self.validator.validate_plan(plan)
        self.assertTrue(is_valid)
        self.assertGreater(len(messages), 0)

    def test_validate_point_with_waypoint(self) -> None:
        '''
            Tests validate_point directly with Waypoint entity.

            :exceptions: None.
        '''
        wp_valid = WaypointFactory.create(x=100.0, y=100.0, z=20.0, phi=0.0, speed=40.0)
        self.assertTrue(self.validator.validate_point(wp_valid).is_valid)

        wp_invalid = WaypointFactory.create(x=250.0, y=250.0, z=20.0, phi=0.0, speed=40.0)
        self.assertFalse(self.validator.validate_point(wp_invalid).is_valid)

    def test_direct_constructor_injection(self) -> None:
        '''
            Tests direct constructor dependency injection with kinematics service.

            :exceptions: None.
        '''
        kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        validator = TrajectoryValidator(kinematics=kinematics)
        self.assertEqual(validator.bounds, self.bounds)
        self.assertEqual(validator.kinematics, kinematics)


if __name__ == '__main__':
    main()
