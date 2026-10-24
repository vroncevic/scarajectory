# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for WorkerThreadCoordinator lifecycle implementation.
'''

from __future__ import annotations

from threading import Event
from time import sleep
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.pacing.coordinator.icoordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.worker.thread.coordinator import WorkerThreadCoordinator
from scarajectory.infrastructure.worker.thread.icoordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerThreadCoordinatorTestCase(TestCase):
    '''
        Unit tests for WorkerThreadCoordinator.

        It defines:

            :methods:
                | setUp - Prepares mock collaborators.
                | test_structural_conformance - Verifies coordinator conforms to protocol.
                | test_thread_lifecycle - Verifies start, pause, resume, and stop flow.
    '''

    def setUp(self) -> None:
        '''
            Prepares test coordinator and mock dependencies.

            :exceptions: None.
        '''
        self.mock_barrier = MagicMock(spec=IFlowBarrierCoordinator)
        self.coordinator = WorkerThreadCoordinator(
            barrier_coordinator=self.mock_barrier
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies coordinator satisfies IWorkerThreadCoordinator structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, IWorkerThreadCoordinator)

    def test_thread_lifecycle(self) -> None:
        '''
            Verifies start_thread, pause, resume, and stop behavior.

            :exceptions: None.
        '''
        executed = Event()

        def sample_target(
            *,
            stop_event: Event,
            pause_event: Event,
        ) -> None:
            while not stop_event.is_set():
                if pause_event.is_set():
                    sleep(0.01)
                    continue
                executed.set()
                sleep(0.01)

        self.coordinator.start_thread(
            target=sample_target,
            kwargs={},
        )
        self.assertTrue(self.coordinator.is_running())
        self.assertTrue(executed.wait(timeout=0.5))

        self.coordinator.set_paused(paused=True)
        self.coordinator.set_paused(paused=False)

        self.coordinator.stop()
        self.mock_barrier.reset.assert_called_once()
        self.assertFalse(self.coordinator.is_running())


if __name__ == '__main__':
    main()
