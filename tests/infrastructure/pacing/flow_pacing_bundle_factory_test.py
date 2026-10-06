# -*- coding: UTF-8 -*-

'''
Module
    flow_pacing_bundle_factory_test.py
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
    Unit tests for FlowPacingBundleFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFlowPacingBundleFactory(TestCase):
    '''
        Test cases verifying FlowPacingBundleFactory behavior.
    '''

    def test_create_bundle(self) -> None:
        '''
            Tests bundle creation with barrier and capacity.
        '''
        barrier = FlowBarrierFactory.create()
        bundle: FlowPacingBundle = FlowPacingBundleFactory.create(
            barrier=barrier,
            capacity=12,
        )
        self.assertIsInstance(bundle, FlowPacingBundle)
        self.assertEqual(bundle.pacing_controller.capacity, 12)
        self.assertTrue(bundle.barrier_coordinator.is_barrier_clear())

    def test_get_version(self) -> None:
        '''
            Tests factory version retrieval.
        '''
        self.assertIsInstance(FlowPacingBundleFactory.get_version(), str)


if __name__ == '__main__':
    main()
