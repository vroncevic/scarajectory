# -*- coding: UTF-8 -*-

'''
Module
    flow_pacing_bundle_factory.py
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
    Factory service constructing FlowPacingBundle instances.
'''

from __future__ import annotations

from typing import ClassVar

from scarajectory.core.service.barrier.iflow_barrier import IFlowBarrier
from scarajectory.core.service.barrier.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.core.service.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_barrier_coordinator_factory import FlowBarrierCoordinatorFactory
from scarajectory.infrastructure.pacing.flow_pacing_controller_factory import FlowPacingControllerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowPacingBundleFactory:
    '''
        Factory providing creation of FlowPacingBundle instances.

        It defines:

            :attributes:
                | DEFAULT_QUEUE_CAPACITY - Default capacity of microcontroller ring buffer.

            :methods:
                | create - Constructs FlowPacingBundle with configured collaborators and capacity.
                | get_version - Returns factory version string.
    '''

    DEFAULT_QUEUE_CAPACITY: ClassVar[int] = 16

    @classmethod
    def create(
        cls,
        *,
        barrier: IFlowBarrier,
        capacity: int = DEFAULT_QUEUE_CAPACITY,
    ) -> FlowPacingBundle:
        '''
            Constructs FlowPacingBundle with injected barrier and capacity.

            :param barrier: IFlowBarrier instance managing synchronization barriers.
            :param capacity: Microcontroller ring buffer capacity (default 16).
            :return: FlowPacingBundle instance.
            :exceptions: None.
        '''
        barrier_coordinator: IFlowBarrierCoordinator = (
            FlowBarrierCoordinatorFactory.create(barrier)
        )
        pacing_controller: IFlowPacingController = (
            FlowPacingControllerFactory.create(
                barrier_coordinator=barrier_coordinator,
                capacity=capacity,
            )
        )

        return FlowPacingBundle(
            pacing_controller=pacing_controller,
            barrier_coordinator=barrier_coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
