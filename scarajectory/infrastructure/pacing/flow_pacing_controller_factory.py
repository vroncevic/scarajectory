# -*- coding: UTF-8 -*-

'''
Module
    flow_pacing_controller_factory.py
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
    Factory service constructing FlowPacingController instances with injected protocol classifiers.
'''

from __future__ import annotations

from scarajectory.core.service.barrier.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.core.service.classifier.iflow_status_classifier import IFlowStatusClassifier
from scarajectory.core.service.classifier.ihoming_status_classifier import IHomingStatusClassifier
from scarajectory.core.service.classifier.imotion_status_classifier import IMotionStatusClassifier
from scarajectory.core.service.classifier.iresponse_parser import IResponseParser
from scarajectory.infrastructure.classifier.status.flow_status_classifier_factory import FlowStatusClassifierFactory
from scarajectory.infrastructure.classifier.status.homing_status_classifier_factory import HomingStatusClassifierFactory
from scarajectory.infrastructure.classifier.status.motion_status_classifier_factory import MotionStatusClassifierFactory
from scarajectory.infrastructure.classifier.response_parser_factory import ResponseParserFactory
from scarajectory.infrastructure.pacing.flow_pacing_controller import FlowPacingController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowPacingControllerFactory:
    '''
        Factory providing creation of FlowPacingController instances.

        It defines:

            :methods:
                | create - Constructs FlowPacingController with default configured classifiers and capacity.
                | create_with_classifiers - Constructs FlowPacingController with injected protocol classifiers.
                | get_version - Returns factory version string.
    '''

    DEFAULT_QUEUE_CAPACITY: int = 16

    @classmethod
    def create(
        cls,
        *,
        barrier_coordinator: IFlowBarrierCoordinator,
        capacity: int = DEFAULT_QUEUE_CAPACITY,
    ) -> FlowPacingController:
        '''
            Constructs and returns configured FlowPacingController with injected barrier coordinator.

            :param barrier_coordinator: IFlowBarrierCoordinator managing synchronization barriers.
            :param capacity: Microcontroller ring buffer capacity (default 16).
            :return: FlowPacingController instance.
            :exceptions: None.
        '''
        return FlowPacingController(
            capacity=capacity,
            response_parser=ResponseParserFactory.create(),
            flow_classifier=FlowStatusClassifierFactory.create(),
            motion_classifier=MotionStatusClassifierFactory.create(),
            homing_classifier=HomingStatusClassifierFactory.create(),
            barrier_coordinator=barrier_coordinator,
        )

    @classmethod
    def create_with_classifiers(
        cls,
        *,
        response_parser: IResponseParser,
        flow_classifier: IFlowStatusClassifier,
        motion_classifier: IMotionStatusClassifier,
        homing_classifier: IHomingStatusClassifier,
        barrier_coordinator: IFlowBarrierCoordinator,
        capacity: int = DEFAULT_QUEUE_CAPACITY,
    ) -> FlowPacingController:
        '''
            Constructs FlowPacingController with injected protocol classifiers and barrier coordinator.

            :param response_parser: IResponseParser instance.
            :param flow_classifier: IFlowStatusClassifier instance.
            :param motion_classifier: IMotionStatusClassifier instance.
            :param homing_classifier: IHomingStatusClassifier instance.
            :param barrier_coordinator: IFlowBarrierCoordinator managing synchronization barriers.
            :param capacity: Microcontroller ring buffer capacity (default 16).
            :return: FlowPacingController instance.
            :exceptions: None.
        '''
        return FlowPacingController(
            capacity=capacity,
            response_parser=response_parser,
            flow_classifier=flow_classifier,
            motion_classifier=motion_classifier,
            homing_classifier=homing_classifier,
            barrier_coordinator=barrier_coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
