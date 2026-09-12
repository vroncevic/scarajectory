# -*- coding: UTF-8 -*-

'''
Module
    kinematics_service_test.py
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
    Unit tests for KinematicsService analytical kinematics and workspace calculations.
'''

from __future__ import annotations

from math import isclose, pi, radians
from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scarajectory.core.service.kinematics.kinematics_service import KinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsServiceTestCase(TestCase):
    '''
        Validates KinematicsService forward/inverse kinematics and workspace boundary logic.

        It defines:

            :methods:
                | setUp - Prepares default bounds and service instance.
                | test_protocol_conformance - Verifies runtime Protocol check.
                | test_reach_radii_calculation - Checks r_min and r_max calculation from link lengths.
                | test_forward_kinematics - Verifies FK analytical coordinate output.
                | test_inverse_kinematics_roundtrip - Verifies FK(IK(x, y)) roundtrip equivalence.
                | test_inverse_kinematics_unreachable - Confirms None returned for points beyond outer reach.
                | test_is_in_workspace - Tests annular distance and vertical height checks.
                | test_is_joint_reachable - Tests angular joint limits and singularity deadband.
    '''

    def setUp(self) -> None:
        '''
            Sets up standard SCARA geometry bounds and initializes KinematicsService.
        '''
        self.bounds = ScaraBounds(
            l1=150.0,
            l2=120.0,
            z_min=0.0,
            z_max=50.0,
            j1_min_rad=radians(-150.0),
            j1_max_rad=radians(150.0),
            j2_min_rad=radians(-145.0),
            j2_max_rad=radians(145.0),
            singularity_theta2_min_rad=radians(5.0)
        )
        self.service = KinematicsService(bounds=self.bounds)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that KinematicsService conforms to IKinematicsService runtime Protocol.
        '''
        self.assertIsInstance(self.service, IKinematicsService)

    def test_reach_radii_calculation(self) -> None:
        '''
            Verifies that minimum and maximum reach radii match link length calculations.
        '''
        self.assertAlmostEqual(self.service.r_min, 30.0)
        self.assertAlmostEqual(self.service.r_max, 270.0)
        self.assertEqual(self.service.bounds.l1, 150.0)
        self.assertEqual(self.service.bounds.l2, 120.0)

    def test_forward_kinematics(self) -> None:
        '''
            Tests forward kinematics at zero and 90-degree arm configurations.
        '''
        x, y = self.service.solve_fk(0.0, 0.0)
        self.assertAlmostEqual(x, 270.0)
        self.assertAlmostEqual(y, 0.0)

        x90, y90 = self.service.solve_fk(pi / 2.0, 0.0)
        self.assertAlmostEqual(x90, 0.0)
        self.assertAlmostEqual(y90, 270.0)

    def test_inverse_kinematics_roundtrip(self) -> None:
        '''
            Tests analytical IK roundtrip consistency with FK for both elbow configurations.
        '''
        target_x: float = 120.0
        target_y: float = 100.0

        for elbow_left in (False, True):
            ik_res = self.service.solve_ik(target_x, target_y, elbow_left=elbow_left)
            self.assertIsNotNone(ik_res)
            theta1, theta2 = ik_res
            fk_x, fk_y = self.service.solve_fk(theta1, theta2)
            self.assertTrue(isclose(fk_x, target_x, abs_tol=1e-3))
            self.assertTrue(isclose(fk_y, target_y, abs_tol=1e-3))

    def test_inverse_kinematics_unreachable(self) -> None:
        '''
            Tests that points outside the kinematic reach envelope return None.
        '''
        ik_res = self.service.solve_ik(300.0, 300.0)
        self.assertIsNone(ik_res)

        ik_res_origin = self.service.solve_ik(5.0, 0.0)
        self.assertIsNone(ik_res_origin)

    def test_is_in_workspace(self) -> None:
        '''
            Tests workspace envelope evaluation for annular deadband, outer reach, and Z limits.
        '''
        valid, msg = self.service.is_in_workspace(150.0, 50.0, 25.0)
        self.assertTrue(valid)

        out_reach, msg_reach = self.service.is_in_workspace(200.0, 200.0, 10.0)
        self.assertFalse(out_reach)
        self.assertIn('exceeds maximum reach', msg_reach)

        deadzone, msg_dead = self.service.is_in_workspace(10.0, 10.0, 10.0)
        self.assertFalse(deadzone)
        self.assertIn('inside deadzone', msg_dead)

        z_err, msg_z = self.service.is_in_workspace(150.0, 50.0, 60.0)
        self.assertFalse(z_err)
        self.assertIn('Elevation Z', msg_z)

    def test_is_joint_reachable(self) -> None:
        '''
            Tests joint angular limits and singularity deadband reachability evaluation.
        '''
        reachable, reasons = self.service.is_joint_reachable(150.0, 50.0)
        self.assertTrue(reachable)
        self.assertEqual(len(reasons), 0)

        unreachable_far, reasons_far = self.service.is_joint_reachable(350.0, 0.0)
        self.assertFalse(unreachable_far)

        unreachable_rear, reasons_rear = self.service.is_joint_reachable(-250.0, 0.0)
        self.assertFalse(unreachable_rear)


if __name__ == '__main__':
    main()
