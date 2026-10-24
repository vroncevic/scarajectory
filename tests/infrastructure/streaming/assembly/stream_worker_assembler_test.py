# -*- coding: UTF-8 -*-

'''
Module
    stream_worker_assembler_test.py
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
    Unit tests for StreamWorkerAssembler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.pacing.provides import PacingProvides
from scarajectory.infrastructure.state.dependencies import StateDependencies
from scarajectory.infrastructure.state.factory import StateFactory
from scarajectory.infrastructure.streaming.assembly.stream_pacing_assembler import StreamPacingAssembler
from scarajectory.infrastructure.streaming.assembly.stream_worker_assembler import StreamWorkerAssembler
from scarajectory.infrastructure.streaming.assembly.worker_bundle import WorkerBundle
from scarajectory.infrastructure.streaming.observer.factory import ObserverFactory
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamWorkerAssembler(TestCase):
    '''
    Test cases verifying StreamWorkerAssembler behavior.

    It defines:

        :methods:
            | setUp - Prepares mock collaborators and WorkerBundle.
            | test_assemble - Tests assembly of execution worker and listener binding.
            | test_assemble_binary_worker - Tests direct assembly of binary execution worker.
            | test_get_version - Tests get_version returns string.
    '''

    def setUp(self) -> None:
        '''
        Prepares mock collaborators and WorkerBundle.

        :exceptions: None.
        '''
        self.pacing_provides: PacingProvides = StreamPacingAssembler.assemble(
            queue_capacity=16
        )
        self.mock_transceiver = MagicMock()
        self.state_machine = StateFactory.create(
            StateDependencies()
        ).stream_state_machine
        self.dispatcher = ObserverFactory.create().stream_observer_dispatcher
        self.mock_connection = MagicMock()
        self.bundle: WorkerBundle = WorkerBundle(
            pacing_provides=self.pacing_provides,
            raw_transceiver=self.mock_transceiver,
            state_machine=self.state_machine,
            dispatcher=self.dispatcher,
        )

    def test_assemble(self) -> None:
        '''
        Tests assembly of execution worker and listener binding.

        :exceptions: None.
        '''
        worker: IExecutionWorker = StreamWorkerAssembler.assemble(
            self.mock_connection,
            self.bundle,
        )
        self.assertIsInstance(worker, IExecutionWorker)
        self.mock_connection.set_listener.assert_called_once()

    def test_assemble_binary_worker(self) -> None:
        '''
        Tests direct assembly of binary execution worker and listener binding.

        :exceptions: None.
        '''
        worker: IExecutionWorker = StreamWorkerAssembler.assemble_binary(
            self.mock_connection,
            self.bundle,
        )
        self.assertIsInstance(worker, IExecutionWorker)
        self.mock_connection.set_listener.assert_called_once()

    def test_get_version(self) -> None:
        '''
        Tests get_version returns string.

        :exceptions: None.
        '''
        self.assertIsInstance(StreamWorkerAssembler.get_version(), str)


if __name__ == '__main__':
    main()
