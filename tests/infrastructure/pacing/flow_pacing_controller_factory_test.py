# -*- coding: UTF-8 -*-

'''
Module
    flow_pacing_controller_factory_test.py
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
    Unit testing for FlowPacingControllerFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.flow_barrier_coordinator_factory import FlowBarrierCoordinatorFactory
from scarajectory.infrastructure.pacing.flow_pacing_controller import FlowPacingController
from scarajectory.infrastructure.pacing.flow_pacing_controller_factory import FlowPacingControllerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowPacingControllerFactoryTestCase(TestCase):
    '''
        Unit tests for FlowPacingControllerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory creation with default classifiers.
                | test_create_with_classifiers - Verifies factory creation with custom classifiers.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory instantiates FlowPacingController with barrier coordinator.'''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        controller = FlowPacingControllerFactory.create(
            barrier_coordinator=coordinator,
            capacity=8,
        )
        self.assertIsInstance(controller, FlowPacingController)

    def test_create_with_classifiers(self) -> None:
        '''Verifies factory instantiates FlowPacingController with custom injected classifiers.'''
        controller = FlowPacingControllerFactory.create_with_classifiers(
            response_parser=MagicMock(),
            flow_classifier=MagicMock(),
            motion_classifier=MagicMock(),
            homing_classifier=MagicMock(),
            barrier_coordinator=MagicMock(),
            capacity=12,
        )
        self.assertIsInstance(controller, FlowPacingController)

    def test_get_version(self) -> None:
        '''Verifies factory exposes semantic version string matching package.'''
        self.assertEqual(
            FlowPacingControllerFactory.get_version(), '1.0.3'
        )


if __name__ == '__main__':
    main()
