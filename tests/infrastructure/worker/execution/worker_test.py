# -*- coding: UTF-8 -*-

'''
Module
    worker_test.py
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
    Unit tests for StreamExecutionWorker concurrency implementation.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.program import BinaryProgram

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.infrastructure.worker.execution.worker import StreamExecutionWorker
from scarajectory.infrastructure.worker.holder import StreamSessionHolder
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner
from scarajectory.infrastructure.worker.thread.icoordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamExecutionWorkerTestCase(TestCase):
    '''
        Unit tests for StreamExecutionWorker.

        It defines:

            :methods:
                | setUp - Prepares worker and mock collaborators.
                | test_structural_conformance - Verifies conformance to IExecutionWorker.
                | test_start_waypoints - Verifies waypoints loop thread spawn.
                | test_start_program - Verifies program loop thread spawn.
                | test_lifecycle_delegation - Verifies set_paused, stop, and is_running.
    '''

    def setUp(self) -> None:
        '''
            Prepares worker and mock collaborators.

            :exceptions: None.
        '''
        self.mock_runner = MagicMock(spec=IStreamLoopRunner)
        self.mock_coord = MagicMock(spec=IWorkerThreadCoordinator)
        self.mock_session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        self.holder = StreamSessionHolder(session=self.mock_session)
        self.worker = StreamExecutionWorker(
            loop_runner=self.mock_runner,
            coordinator=self.mock_coord,
            session_holder=self.holder,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies worker satisfies IExecutionWorker structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.worker, IExecutionWorker)

    def test_start_waypoints(self) -> None:
        '''
            Verifies start_waypoints spawns background thread for waypoints loop.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=10.0,
        )
        self.worker.start_waypoints(session=session)
        self.assertIs(self.holder.session, session)
        self.mock_coord.start_thread.assert_called_once_with(
            target=self.mock_runner.run_waypoints_loop,
            kwargs={'session': session},
        )

    def test_start_program(self) -> None:
        '''
            Verifies start_program spawns background thread for binary program loop.

            :exceptions: None.
        '''
        mock_program = MagicMock(spec=BinaryProgram)
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=20.0,
        )
        self.worker.start_program(session=session, program=mock_program)
        self.assertIs(self.holder.session, session)
        self.mock_coord.start_thread.assert_called_once_with(
            target=self.mock_runner.run_program_loop,
            kwargs={'program': mock_program, 'session': session},
        )

    def test_lifecycle_delegation(self) -> None:
        '''
            Verifies set_paused, stop, and is_running delegation to coordinator.

            :exceptions: None.
        '''
        self.worker.set_paused(True)
        self.mock_coord.set_paused.assert_called_with(paused=True)

        self.worker.set_paused(False)
        self.mock_coord.set_paused.assert_called_with(paused=False)

        self.worker.stop()
        self.mock_coord.stop.assert_called_once()

        self.mock_coord.is_running.return_value = True
        self.assertTrue(self.worker.is_running())


if __name__ == '__main__':
    main()
