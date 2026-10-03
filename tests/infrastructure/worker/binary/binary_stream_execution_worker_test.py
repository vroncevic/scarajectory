# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_execution_worker_test.py
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
    Unit testing for BinaryStreamExecutionWorker and BinaryStreamExecutionWorkerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.binary.binary_stream_execution_worker import (
    BinaryStreamExecutionWorker,
)
from scarajectory.infrastructure.worker.binary.binary_stream_execution_worker_factory import (
    BinaryStreamExecutionWorkerFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamExecutionWorkerTestCase(TestCase):
    '''Unit tests validating BinaryStreamExecutionWorker lifecycle and factory creation.'''

    def test_worker_waypoints_lifecycle(self) -> None:
        '''Verifies start, pause, resume, and stop lifecycle for waypoint streaming.'''
        mock_loop_runner = MagicMock()
        mock_barrier = MagicMock()
        worker = BinaryStreamExecutionWorker(
            loop_runner=mock_loop_runner,
            barrier_coordinator=mock_barrier,
        )

        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )

        with patch('scarajectory.infrastructure.worker.binary.binary_stream_execution_worker.Thread') as mock_thread_cls:
            mock_thread = MagicMock()
            mock_thread_cls.return_value = mock_thread

            worker.start(session=session)
            mock_thread.start.assert_called_once()

            worker.pause()
            worker.resume()
            worker.stop()
            mock_barrier.reset.assert_called_once()

    def test_worker_program_lifecycle(self) -> None:
        '''Verifies start_program launches loop runner for pre-compiled binary steps.'''
        mock_loop_runner = MagicMock()
        mock_barrier = MagicMock()
        worker = BinaryStreamExecutionWorker(
            loop_runner=mock_loop_runner,
            barrier_coordinator=mock_barrier,
        )

        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        mock_program = MagicMock(spec=BinaryProgram)

        with patch(
            'scarajectory.infrastructure.worker.binary.binary_stream_execution_worker.Thread'
        ) as mock_thread_cls:
            mock_thread = MagicMock()
            mock_thread.is_alive.return_value = True
            mock_thread_cls.return_value = mock_thread

            worker.start_program(program=mock_program, session=session)
            mock_thread.start.assert_called_once()
            self.assertTrue(worker.is_running())

    def test_handle_incoming_bytes(self) -> None:
        '''Verifies handle_incoming_bytes delegates and triggers stop on fault.'''
        mock_loop_runner = MagicMock()
        mock_barrier = MagicMock()
        worker = BinaryStreamExecutionWorker(
            loop_runner=mock_loop_runner,
            barrier_coordinator=mock_barrier,
        )

        mock_loop_runner.handle_incoming_bytes.return_value = False
        worker.handle_incoming_bytes(b'\xAA\x01')
        mock_barrier.reset.assert_not_called()

        mock_loop_runner.handle_incoming_bytes.return_value = True
        worker.handle_incoming_bytes(b'\xEE\xFF')
        mock_barrier.reset.assert_called_once()

    def test_factory_methods_and_version(self) -> None:
        '''Verifies factory creation with default or injected parser and version string.'''
        mock_bundle = MagicMock()
        mock_strategy = MagicMock()
        mock_sender = MagicMock()
        mock_state = MagicMock()
        mock_dispatcher = MagicMock()
        mock_pacing = MagicMock()

        with patch(
            'scarajectory.infrastructure.worker.binary.binary_stream_execution_worker_factory.BinaryStreamLoopRunnerFactory.create'
        ) as mock_lr_create, patch(
            'scarajectory.infrastructure.worker.binary.binary_stream_execution_worker_factory.BinaryStreamLoopRunnerFactory.create_with_parser'
        ) as mock_lr_create_parser:
            mock_lr_create.return_value = MagicMock()
            mock_lr_create_parser.return_value = MagicMock()

            worker1 = BinaryStreamExecutionWorkerFactory.create(
                pacing_bundle=mock_bundle,
                packet_strategy=mock_strategy,
                byte_sender=mock_sender,
                state_controller=mock_state,
                observer_dispatcher=mock_dispatcher,
                pacing_config=mock_pacing,
            )
            self.assertIsInstance(worker1, BinaryStreamExecutionWorker)

            mock_parser = MagicMock()
            worker2 = BinaryStreamExecutionWorkerFactory.create_with_parser(
                pacing_bundle=mock_bundle,
                packet_strategy=mock_strategy,
                frame_parser=mock_parser,
                byte_sender=mock_sender,
                state_controller=mock_state,
                observer_dispatcher=mock_dispatcher,
                pacing_config=mock_pacing,
            )
            self.assertIsInstance(worker2, BinaryStreamExecutionWorker)

        self.assertEqual(BinaryStreamExecutionWorkerFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
