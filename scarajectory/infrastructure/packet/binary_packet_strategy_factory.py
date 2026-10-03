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

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.packet.binary_packet_strategy import BinaryPacketStrategy
from scarajectory.infrastructure.transmission.transmission_step_calculator import TransmissionStepCalculator
from scarajectory.infrastructure.transmission.transmission_step_calculator_factory import TransmissionStepCalculatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
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
        transmission: TransmissionParameters,
    ) -> BinaryPacketStrategy:
        '''
            Constructs BinaryPacketStrategy with internal BinaryFrameBuilder instance.

            :param kinematics: IKinematicsService implementation.
            :param transmission: TransmissionParameters configuration.
            :return: Configured BinaryPacketStrategy instance.
        '''
        step_calc: TransmissionStepCalculator = TransmissionStepCalculatorFactory.create(
            transmission=transmission
        )
        return BinaryPacketStrategy(
            kinematics=kinematics,
            transmission=transmission,
            frame_builder=BinaryFrameBuilderFactory.create(),
            step_calculator=step_calc,
        )

    @classmethod
    def create_with_frame_builder(
        cls,
        *,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters,
        frame_builder: IBinaryFrameBuilder,
    ) -> BinaryPacketStrategy:
        '''
            Constructs BinaryPacketStrategy with injected frame builder.

            :param kinematics: IKinematicsService implementation.
            :param transmission: TransmissionParameters configuration.
            :param frame_builder: IBinaryFrameBuilder implementation.
            :return: Configured BinaryPacketStrategy instance.
        '''
        step_calc: TransmissionStepCalculator = TransmissionStepCalculatorFactory.create(
            transmission=transmission
        )
        return BinaryPacketStrategy(
            kinematics=kinematics,
            transmission=transmission,
            frame_builder=frame_builder,
            step_calculator=step_calc,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
        '''
        return __version__
