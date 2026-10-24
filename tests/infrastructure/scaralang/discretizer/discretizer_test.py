# -*- coding: UTF-8 -*-

'''
Module
    discretizer_test.py
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
    Unit tests for DualElbowStepDiscretizer.
'''

from __future__ import annotations

from io import StringIO
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.pose.angles import JointAngles
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.duration.factory import SegmentDurationCalculatorFactory
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.solver.analytical.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

from scarajectory.infrastructure.scaralang.discretizer.dependencies import DiscretizerDependencies
from scarajectory.infrastructure.scaralang.discretizer.discretizer import DualElbowStepDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DualElbowStepDiscretizerTestCase(TestCase):
    '''
        Unit tests for DualElbowStepDiscretizer.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and discretizer instance.
                | test_righty_waypoint - Verifies standard Righty waypoint discretization.
                | test_lefty_fallback_waypoint - Verifies Lefty elbow selection for bottom quadrant.
                | test_unreachable_waypoint - Verifies error on unreachable coordinates.
                | test_angles_to_steps - Verifies step conversion delegation.
                | test_dls_fallback_recovers_waypoint - Verifies DLS recovery when analytical fails.
                | test_z_limit_error - Verifies exception when waypoint exceeds Z bounds.
    '''

    _discretizer: DualElbowStepDiscretizer
    _converter: IJointStepTransmissionConverter
    _duration: ISegmentDurationCalculator
    _bounds: ScaraBounds

    def setUp(self) -> None:
        '''
            Sets up test fixtures and instantiates DualElbowStepDiscretizer.

            :exceptions: None.
        '''
        self._bounds = DefaultScaraProfile.create_bounds()
        transmission = DefaultScaraProfile.create_transmission()
        kinematics: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=self._bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        self._converter = TransmissionFactory.create(
            transmission=transmission
        )
        self._duration = SegmentDurationCalculatorFactory.create()
        self._discretizer = DualElbowStepDiscretizer(
            DiscretizerDependencies(
                spatial=kinematics.spatial,
                numerical_spatial=kinematics.numerical_spatial,
                transmission=self._converter,
                duration_calculator=self._duration,
                bounds=self._bounds,
            )
        )

    def test_righty_waypoint(self) -> None:
        '''
            Verifies standard Righty waypoint discretization.

            :exceptions: None.
        '''
        self.assertIsInstance(self._discretizer, IStepDiscretizer)
        wp = Waypoint(x=100.0, y=100.0, z=10.0, speed=50.0, phi=0.0, name='', command='')
        prev = JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0)
        steps, new_ang = self._discretizer.discretize_waypoint(waypoint=wp, prev_angles=prev)
        self.assertIsInstance(steps, JointSteps)
        self.assertIsInstance(new_ang, JointAngles)

    def test_lefty_fallback_waypoint(self) -> None:
        '''
            Verifies Lefty elbow selection for bottom quadrant waypoint.

            :exceptions: None.
        '''
        wp = Waypoint(x=-23.0, y=-88.0, z=10.0, speed=50.0, phi=0.0, name='', command='')
        prev = JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0)
        steps, new_ang = self._discretizer.discretize_waypoint(waypoint=wp, prev_angles=prev)
        self.assertIsInstance(steps, JointSteps)
        self.assertGreater(new_ang.theta1, -2.617)

    def test_unreachable_waypoint(self) -> None:
        '''
            Verifies error on unreachable coordinates.

            :exceptions: None.
        '''
        wp = Waypoint(x=500.0, y=500.0, z=10.0, speed=50.0, phi=0.0, name='', command='')
        prev = JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0)
        with self.assertRaises(ScaraKinematicsError) as ctx:
            self._discretizer.discretize_waypoint(waypoint=wp, prev_angles=prev)
        self.assertIn('analytical dual-elbow failed', str(ctx.exception))
        self.assertIn('numerical DLS fallback failed', str(ctx.exception))

    def test_angles_to_steps(self) -> None:
        '''
            Verifies step conversion delegation.

            :exceptions: None.
        '''
        steps = self._discretizer.angles_to_steps(0.1, 0.2, 5.0, 0.0)
        self.assertIsNotNone(steps)
        self.assertEqual(self._discretizer.get_version(), '1.0.3')

    def test_dls_fallback_recovers_waypoint(self) -> None:
        '''
            Verifies DLS recovery when analytical dual-elbow IK fails.

            :exceptions: None.
        '''
        mock_spatial = MagicMock(spec=ISpatialKinematicsSolver)
        mock_spatial.solve_ik_4d.return_value = ScaraJoints(
            theta1=0.0,
            theta2=0.0,
            z=10.0,
            theta4=0.0,
            reachable=False,
            status=IkStatus.SINGULARITY,
        )
        mock_numerical = MagicMock(spec=INumericalSpatialKinematicsSolver)
        mock_numerical.solve_dls_4d.return_value = ScaraJoints(
            theta1=0.5,
            theta2=0.5,
            z=10.0,
            theta4=0.0,
            reachable=True,
            status=IkStatus.SUCCESS,
        )
        discretizer = DualElbowStepDiscretizer(
            DiscretizerDependencies(
                spatial=mock_spatial,
                numerical_spatial=mock_numerical,
                transmission=self._converter,
                duration_calculator=self._duration,
                bounds=self._bounds,
            )
        )
        wp = Waypoint(x=120.0, y=120.0, z=10.0, speed=50.0, phi=0.0, name='', command='')
        prev = JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0)
        with patch(
            'scarajectory.infrastructure.scaralang.discretizer.discretizer.stderr',
            new_callable=StringIO,
        ) as fake_stderr:
            steps, new_ang = discretizer.discretize_waypoint(waypoint=wp, prev_angles=prev)
            self.assertIn('scarajectory: warning: Waypoint', fake_stderr.getvalue())
            self.assertIn('recovered using numerical DLS fallback', fake_stderr.getvalue())
            self.assertIsInstance(steps, JointSteps)
            self.assertEqual(new_ang.theta1, 0.5)

    def test_z_limit_error(self) -> None:
        '''
            Verifies exception when waypoint exceeds Z bounds.

            :exceptions: None.
        '''
        wp = Waypoint(x=100.0, y=100.0, z=150.0, speed=50.0, phi=0.0, name='', command='')
        prev = JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0)
        with self.assertRaises(ScaraKinematicsError) as ctx:
            self._discretizer.discretize_waypoint(waypoint=wp, prev_angles=prev)
        self.assertIn('is outside vertical limits', str(ctx.exception))


if __name__ == '__main__':
    main()
