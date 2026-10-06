# -*- coding: UTF-8 -*-

'''
Module
    worker_thread_coordinator_test.py
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
    Unit testing for WorkerThreadCoordinator component.
'''

from __future__ import annotations

from threading import Event
from time import sleep
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.worker.thread.iworker_thread_coordinator import IWorkerThreadCoordinator
from scarajectory.infrastructure.worker.thread.worker_thread_coordinator import WorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerThreadCoordinatorTestCase(TestCase):
    '''Unit tests validating WorkerThreadCoordinator execution and synchronization.'''

    def test_protocol_and_initial_state(self) -> None:
        '''Verifies protocol conformance and initial idle state.'''
        mock_barrier = MagicMock()
        coordinator = WorkerThreadCoordinator(
            barrier_coordinator=mock_barrier
        )
        self.assertIsInstance(coordinator, IWorkerThreadCoordinator)
        self.assertFalse(coordinator.is_running())

    def test_thread_execution_and_lifecycle(self) -> None:
        '''Verifies start_thread, pause, resume, and stop operations.'''
        mock_barrier = MagicMock()
        coordinator = WorkerThreadCoordinator(
            barrier_coordinator=mock_barrier
        )

        captured_kwargs: dict[str, object] = {}

        def sample_loop(
            *,
            test_val: int,
            stop_event: Event,
            pause_event: Event,
        ) -> None:
            captured_kwargs['test_val'] = test_val
            captured_kwargs['stop_event'] = stop_event
            captured_kwargs['pause_event'] = pause_event
            while not stop_event.is_set():
                sleep(0.01)

        coordinator.start_thread(
            target=sample_loop,
            kwargs={'test_val': 42},
        )

        sleep(0.05)
        self.assertTrue(coordinator.is_running())
        self.assertEqual(captured_kwargs.get('test_val'), 42)

        pause_evt = captured_kwargs['pause_event']
        self.assertIsInstance(pause_evt, Event)
        self.assertFalse(pause_evt.is_set())

        coordinator.set_paused(paused=True)
        self.assertTrue(pause_evt.is_set())

        coordinator.set_paused(paused=False)
        self.assertFalse(pause_evt.is_set())

        coordinator.stop()
        sleep(0.05)
        self.assertFalse(coordinator.is_running())
        mock_barrier.reset.assert_called_once()


if __name__ == '__main__':
    main()
