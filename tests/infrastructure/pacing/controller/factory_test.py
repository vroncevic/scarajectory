# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for ControllerFactory service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaracom.flow.barrier.barrier import FlowBarrier

from scarajectory.infrastructure.pacing.controller.controller import FlowPacingController
from scarajectory.infrastructure.pacing.controller.dependencies import ControllerDependencies
from scarajectory.infrastructure.pacing.controller.factory import ControllerFactory
from scarajectory.infrastructure.pacing.controller.provides import ControllerProvides
from scarajectory.infrastructure.pacing.coordinator.coordinator import FlowBarrierCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControllerFactoryTestCase(TestCase):
    '''Unit tests validating ControllerFactory creation and versioning.'''

    def test_factory_creation(self) -> None:
        '''
            Verifies ControllerFactory instantiates ControllerProvides.

            :exceptions: None.
        '''
        barrier = FlowBarrier()
        coordinator = FlowBarrierCoordinator(flow_barrier=barrier)
        deps = ControllerDependencies(
            flow_barrier_coordinator=coordinator,
            capacity=16,
        )
        provides: ControllerProvides = ControllerFactory.create(deps)

        self.assertIsInstance(provides, ControllerProvides)
        self.assertIsInstance(
            provides.flow_pacing_controller, FlowPacingController
        )

    def test_factory_version(self) -> None:
        '''
            Verifies ControllerFactory returns version string.

            :exceptions: None.
        '''
        self.assertEqual(ControllerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
