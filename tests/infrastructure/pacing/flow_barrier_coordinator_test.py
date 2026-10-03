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
    Unit testing for FlowBarrierCoordinator and FlowBarrierCoordinatorFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.pacing.flow_barrier_coordinator import (
    FlowBarrierCoordinator,
)
from scarajectory.infrastructure.pacing.flow_barrier_coordinator_factory import (
    FlowBarrierCoordinatorFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowBarrierCoordinatorTestCase(TestCase):
    '''Unit tests validating FlowBarrierCoordinator operations and factory creation.'''

    def test_barrier_actions(self) -> None:
        '''Verifies set_barrier, clear_barrier, is_barrier_clear, and reset delegation.'''
        barrier = MagicMock()
        barrier.is_barrier_clear.return_value = True

        coordinator = FlowBarrierCoordinator(barrier)

        coordinator.set_barrier()
        barrier.set_barrier.assert_called_once()

        coordinator.clear_barrier()
        barrier.clear_barrier.assert_called_once()

        self.assertTrue(coordinator.is_barrier_clear())
        barrier.is_barrier_clear.assert_called_once()

        coordinator.reset()
        barrier.reset.assert_called_once()

    def test_factory_creation_and_version(self) -> None:
        '''Verifies FlowBarrierCoordinatorFactory instantiates coordinator and returns version.'''
        barrier = MagicMock()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        self.assertIsInstance(coordinator, FlowBarrierCoordinator)
        self.assertEqual(FlowBarrierCoordinatorFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
