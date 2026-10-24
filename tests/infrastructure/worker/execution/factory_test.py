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
    Unit tests for StreamExecutionWorkerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.worker.execution.dependencies import ExecutionWorkerDependencies
from scarajectory.infrastructure.worker.execution.factory import StreamExecutionWorkerFactory
from scarajectory.infrastructure.worker.execution.worker import StreamExecutionWorker
from scarajectory.infrastructure.worker.holder import StreamSessionHolder
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner
from scarajectory.infrastructure.worker.thread.icoordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamExecutionWorkerFactoryTestCase(TestCase):
    '''
        Unit tests for StreamExecutionWorkerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory creates StreamExecutionWorker.
                | test_version - Verifies factory get_version returns string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates StreamExecutionWorker instance.

            :exceptions: None.
        '''
        mock_runner = MagicMock(spec=IStreamLoopRunner)
        mock_coord = MagicMock(spec=IWorkerThreadCoordinator)
        holder = StreamSessionHolder(session=SessionFactory.create_default())

        dependencies = ExecutionWorkerDependencies(
            loop_runner=mock_runner,
            coordinator=mock_coord,
            session_holder=holder,
        )
        worker = StreamExecutionWorkerFactory.create(dependencies)
        self.assertIsInstance(worker, StreamExecutionWorker)

    def test_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(StreamExecutionWorkerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
