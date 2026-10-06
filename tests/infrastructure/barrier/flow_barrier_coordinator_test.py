# -*- coding: UTF-8 -*-

'''
Module
    flow_barrier_coordinator_test.py
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
    Unit tests for FlowBarrierCoordinator and FlowBarrierCoordinatorFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.pacing.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.flow_barrier_coordinator import FlowBarrierCoordinator
from scarajectory.infrastructure.pacing.flow_barrier_coordinator_factory import FlowBarrierCoordinatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFlowBarrierCoordinator(TestCase):
    '''
        Test cases for FlowBarrierCoordinator and FlowBarrierCoordinatorFactory.

        It defines:

            :methods:
                | test_flow_barrier_coordinator_protocol - Verifies protocol conformance.
                | test_flow_barrier_coordinator_lifecycle - Verifies set, clear, is_clear and reset.
                | test_flow_barrier_coordinator_factory - Verifies factory creation and version.
    '''

    def test_flow_barrier_coordinator_protocol(self) -> None:
        '''
            Verifies that FlowBarrierCoordinator satisfies IFlowBarrierCoordinator.
        '''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        self.assertIsInstance(coordinator, IFlowBarrierCoordinator)

    def test_flow_barrier_coordinator_lifecycle(self) -> None:
        '''
            Verifies set, clear, is_barrier_clear and reset operations.
        '''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)

        self.assertTrue(coordinator.is_barrier_clear())

        coordinator.set_barrier()
        self.assertFalse(coordinator.is_barrier_clear())

        coordinator.clear_barrier()
        self.assertTrue(coordinator.is_barrier_clear())

        coordinator.set_barrier()
        self.assertFalse(coordinator.is_barrier_clear())

        coordinator.reset()
        self.assertTrue(coordinator.is_barrier_clear())

    def test_flow_barrier_coordinator_factory(self) -> None:
        '''
            Verifies factory construction and version retrieval.
        '''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        self.assertIsInstance(coordinator, FlowBarrierCoordinator)
        self.assertIsInstance(FlowBarrierCoordinatorFactory.get_version(), str)


if __name__ == '__main__':
    main()
