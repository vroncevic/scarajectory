# -*- coding: UTF-8 -*-

'''
Module
    strategy_test.py
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
    Unit tests for BinaryPacketStrategy component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.discretizer.factory import StepDiscretizerFactory
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.duration.factory import SegmentDurationCalculatorFactory
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.packet.strategy import BinaryPacketStrategy

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPacketStrategyTestCase(TestCase):
    '''Unit tests validating BinaryPacketStrategy waypoint encoding.'''

    def setUp(self) -> None:
        '''Sets up kinematics, discretizer, and frame builder fixtures.'''
        bounds = DefaultScaraProfile.create_bounds()
        transmission = DefaultScaraProfile.create_transmission()
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        converter: IJointStepTransmissionConverter = (
            TransmissionFactory.create(
                transmission=transmission
            )
        )
        self.discretizer: IStepDiscretizer = StepDiscretizerFactory.create(
            dependencies=DiscretizerDependencies(
                spatial=kinematics_provides.spatial,
                numerical_spatial=kinematics_provides.numerical_spatial,
                transmission=converter,
                duration_calculator=SegmentDurationCalculatorFactory.create(),
            )
        )
        builders = BuilderFactory.create()
        self.strategy = BinaryPacketStrategy(
            step_discretizer=self.discretizer,
            motion_frame_builder=builders.motion,
            frame_packer=builders.packer,
        )

    def test_format_waypoint_reachable(self) -> None:
        '''Tests encoding valid reachable waypoint into binary move frame.'''
        waypoint = TrajectoryWaypoint(x=150.0, y=100.0, z=10.0, speed=50.0, phi=30.0, name='', command='')
        packet = self.strategy.format_waypoint_packet(waypoint=waypoint, seq_num=5)

        self.assertGreater(len(packet), 0)
        self.assertEqual(packet[0], 0xAA)
        self.assertEqual(packet[1], 0x55)
        self.assertEqual(packet[3], 5)
        self.assertEqual(packet[-1], 0x0D)

    def test_format_waypoint_unreachable(self) -> None:
        '''Tests encoding unreachable waypoint with fallback discretization.'''
        waypoint = TrajectoryWaypoint(x=9999.0, y=9999.0, z=0.0, speed=10.0, phi=0.0, name='', command='')
        packet = self.strategy.format_waypoint_packet(waypoint=waypoint, seq_num=10)

        self.assertGreater(len(packet), 0)
        self.assertEqual(packet[0], 0xAA)
        self.assertEqual(packet[1], 0x55)
        self.assertEqual(packet[3], 10)

    def test_reset(self) -> None:
        '''Tests reset method restores initial angle state.'''
        self.strategy.reset()
        self.assertEqual(self.strategy.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
