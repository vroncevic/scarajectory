# -*- coding: UTF-8 -*-

'''
Module
    flow_barrier_test.py
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
    Unit tests for FlowBarrier and FlowBarrierFactory components.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.barrier.iflow_barrier import IFlowBarrier
from scarajectory.infrastructure.barrier.flow_barrier import FlowBarrier
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFlowBarrier(TestCase):
    '''
        Test cases for FlowBarrier and FlowBarrierFactory.

        It defines:

            :methods:
                | test_flow_barrier_protocol_conformance - Verifies FlowBarrier conforms to IFlowBarrier.
                | test_flow_barrier_lifecycle - Verifies set, clear, is_barrier_clear and reset behaviors.
                | test_flow_barrier_factory - Verifies factory creation and version retrieval.
    '''

    def test_flow_barrier_protocol_conformance(self) -> None:
        '''
            Verifies that FlowBarrier instance satisfies IFlowBarrier protocol.
        '''
        barrier = FlowBarrierFactory.create()
        self.assertIsInstance(barrier, IFlowBarrier)

    def test_flow_barrier_lifecycle(self) -> None:
        '''
            Verifies set, clear, is_barrier_clear and reset lifecycle operations.
        '''
        barrier = FlowBarrierFactory.create()
        self.assertTrue(barrier.is_barrier_clear())

        barrier.set_barrier()
        self.assertFalse(barrier.is_barrier_clear())

        barrier.clear_barrier()
        self.assertTrue(barrier.is_barrier_clear())

        barrier.set_barrier()
        self.assertFalse(barrier.is_barrier_clear())

        barrier.reset()
        self.assertTrue(barrier.is_barrier_clear())

    def test_flow_barrier_factory(self) -> None:
        '''
            Verifies factory construction and version retrieval.
        '''
        barrier = FlowBarrierFactory.create()
        self.assertIsInstance(barrier, FlowBarrier)
        self.assertIsInstance(FlowBarrierFactory.get_version(), str)


if __name__ == '__main__':
    main()
