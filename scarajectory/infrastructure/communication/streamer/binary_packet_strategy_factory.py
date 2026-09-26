# -*- coding: UTF-8 -*-

'''
Module
    binary_packet_strategy_factory.py
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
    Factory service constructing BinaryPacketStrategy instances.
'''

from __future__ import annotations

from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder import BinaryFrameBuilder
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.communication.streamer.binary_packet_strategy import BinaryPacketStrategy

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPacketStrategyFactory:
    '''
        Factory constructing BinaryPacketStrategy instances with injected collaborators.

        It defines:

            :methods:
                | create - Constructs BinaryPacketStrategy with required external dependencies.
                | create_with_frame_builder - Constructs BinaryPacketStrategy with injected frame builder.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters
    ) -> BinaryPacketStrategy:
        '''
            Constructs BinaryPacketStrategy with required external dependencies.

            :param kinematics: Required IKinematicsService instance from external domain.
            :param transmission: Required TransmissionParameters instance from external domain.
            :return: Configured BinaryPacketStrategy instance.
        '''
        return BinaryPacketStrategy(
            kinematics=kinematics,
            transmission=transmission,
            frame_builder=BinaryFrameBuilderFactory.create()
        )

    @classmethod
    def create_with_frame_builder(
        cls,
        *,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters,
        frame_builder: BinaryFrameBuilder
    ) -> BinaryPacketStrategy:
        '''
            Constructs BinaryPacketStrategy with injected frame builder.

            :param kinematics: Required IKinematicsService instance.
            :param transmission: Required TransmissionParameters instance.
            :param frame_builder: BinaryFrameBuilder instance.
            :return: Configured BinaryPacketStrategy instance.
        '''
        return BinaryPacketStrategy(
            kinematics=kinematics, transmission=transmission, frame_builder=frame_builder
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__

