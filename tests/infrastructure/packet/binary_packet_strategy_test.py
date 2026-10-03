# -*- coding: UTF-8 -*-

'''
Module
    binary_packet_strategy_test.py
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
    Unit tests for BinaryPacketStrategy and BinaryPacketStrategyFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.transmission_parameters import (
    TransmissionParameters,
)
from scaralang.core.service.kinematics.ikinematics_service import (
    IKinematicsService,
)
from scaralang.core.service.kinematics.kinematics_service_factory import (
    KinematicsServiceFactory,
)
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import (
    BinaryFrameBuilderFactory,
)
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.packet.ipacket_strategy import IPacketStrategy
from scarajectory.infrastructure.packet.binary_packet_strategy import (
    BinaryPacketStrategy,
)
from scarajectory.infrastructure.packet.binary_packet_strategy_factory import (
    BinaryPacketStrategyFactory,
)
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import (
    ScaraBoundsLoaderFactory,
)
from scarajectory.infrastructure.settings.transmission.scara_transmission_loader_factory import (
    ScaraTransmissionLoaderFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPacketStrategyTestCase(TestCase):
    '''
        Tests for BinaryPacketStrategy binary wire frame encoding.

        It defines:

            :methods:
                | setUp - Initializes kinematics and transmission fixtures.
                | test_factory_and_protocol_conformance - Tests factory and protocol conformance.
                | test_create_with_frame_builder - Tests factory with explicit frame builder.
                | test_format_waypoint_reachable - Tests encoding valid reachable waypoint.
                | test_format_waypoint_unreachable - Tests encoding unreachable waypoint fallback.
    '''

    kinematics: IKinematicsService
    transmission: TransmissionParameters

    def setUp(self) -> None:
        '''
            Initializes kinematics and transmission fixtures.

            :exceptions: None.
        '''
        bounds = ScaraBoundsLoaderFactory.create().load_bounds()
        self.transmission = (
            ScaraTransmissionLoaderFactory.create().load_transmission()
        )
        self.kinematics = KinematicsServiceFactory.create(bounds=bounds)

    def test_factory_and_protocol_conformance(self) -> None:
        '''
            Tests factory and protocol conformance.

            :exceptions: None.
        '''
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        self.assertIsInstance(strategy, BinaryPacketStrategy)
        self.assertIsInstance(strategy, IPacketStrategy)
        self.assertEqual(BinaryPacketStrategyFactory.get_version(), '1.0.4')

    def test_create_with_frame_builder(self) -> None:
        '''
            Tests factory with explicit frame builder.

            :exceptions: None.
        '''
        builder = BinaryFrameBuilderFactory.create()
        strategy = BinaryPacketStrategyFactory.create_with_frame_builder(
            kinematics=self.kinematics,
            transmission=self.transmission,
            frame_builder=builder,
        )
        self.assertIsInstance(strategy, BinaryPacketStrategy)

    def test_format_waypoint_reachable(self) -> None:
        '''
            Tests encoding valid reachable waypoint.

            :exceptions: None.
        '''
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        waypoint = Waypoint(x=150.0, y=100.0, z=10.0, speed=50.0, phi=30.0)
        packet = strategy.format_waypoint_packet(waypoint=waypoint, seq_num=5)

        self.assertGreater(len(packet), 0)
        self.assertEqual(packet[0], 0xAA)
        self.assertEqual(packet[1], 0x55)
        self.assertEqual(packet[3], 5)
        self.assertEqual(packet[-1], 0x0D)

    def test_format_waypoint_unreachable(self) -> None:
        '''
            Tests encoding unreachable waypoint fallback.

            :exceptions: None.
        '''
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        waypoint = Waypoint(
            x=9999.0, y=9999.0, z=0.0, speed=10.0, phi=0.0
        )
        packet = strategy.format_waypoint_packet(waypoint=waypoint, seq_num=10)

        self.assertGreater(len(packet), 0)
        self.assertEqual(packet[0], 0xAA)
        self.assertEqual(packet[1], 0x55)
        self.assertEqual(packet[3], 10)


if __name__ == '__main__':
    main()
