# -*- coding: UTF-8 -*-

'''
Module
    stream_execution_worker_factory_test.py
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
    Unit tests for StreamExecutionWorkerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.stream_pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.worker.ascii.stream_execution_worker import StreamExecutionWorker
from scarajectory.infrastructure.worker.ascii.stream_execution_worker_factory import StreamExecutionWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamExecutionWorkerFactory(TestCase):
    '''
        Test cases verifying StreamExecutionWorkerFactory behavior.

        It defines:

            :methods:
                | test_create_worker - Tests default worker creation.
                | test_create_with_formatter - Tests creation with explicit formatter.
                | test_get_version - Tests get_version return value.
    '''

    def test_create_worker(self) -> None:
        '''
            Tests create factory method.

            :exceptions: None.
        '''
        barrier = FlowBarrierFactory.create()
        pacing_bundle = FlowPacingBundleFactory.create(barrier=barrier, capacity=8)
        pacing_config = StreamPacingConfigFactory.create_ascii()
        worker = StreamExecutionWorkerFactory.create(
            pacing_bundle=pacing_bundle,
            command_sender=MagicMock(),
            state_controller=MagicMock(),
            observer_dispatcher=MagicMock(),
            pacing_config=pacing_config,
        )
        self.assertIsInstance(worker, StreamExecutionWorker)

    def test_create_with_formatter(self) -> None:
        '''
            Tests create_with_formatter factory method.

            :exceptions: None.
        '''
        barrier = FlowBarrierFactory.create()
        pacing_bundle = FlowPacingBundleFactory.create(barrier=barrier, capacity=8)
        pacing_config = StreamPacingConfigFactory.create_ascii()
        worker = StreamExecutionWorkerFactory.create_with_formatter(
            pacing_bundle=pacing_bundle,
            formatter=MagicMock(),
            command_sender=MagicMock(),
            state_controller=MagicMock(),
            observer_dispatcher=MagicMock(),
            pacing_config=pacing_config,
        )
        self.assertIsInstance(worker, StreamExecutionWorker)

    def test_get_version(self) -> None:
        '''
            Tests get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = StreamExecutionWorkerFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
