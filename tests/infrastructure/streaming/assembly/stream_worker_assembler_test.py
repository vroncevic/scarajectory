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

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.state.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.streaming.assembly.stream_worker_assembler import StreamWorkerAssembler
from scarajectory.infrastructure.streaming.assembly.worker_bundle import WorkerBundle
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamWorkerAssembler(TestCase):
    '''
        Test cases verifying StreamWorkerAssembler behavior.
    '''

    def setUp(self) -> None:
        barrier = FlowBarrierFactory.create()
        self.pacing_bundle: FlowPacingBundle = FlowPacingBundleFactory.create(
            barrier=barrier, capacity=16
        )
        self.mock_transceiver = MagicMock()
        self.state_machine = StreamStateMachineFactory.create()
        self.dispatcher = StreamObserverDispatcherFactory.create()
        self.mock_connection = MagicMock()
        self.bundle: WorkerBundle = WorkerBundle(
            pacing_bundle=self.pacing_bundle,
            raw_transceiver=self.mock_transceiver,
            state_machine=self.state_machine,
            dispatcher=self.dispatcher,
        )

    def test_assemble_ascii_worker(self) -> None:
        '''
            Tests assembly of ASCII execution worker and listener binding.
        '''
        worker: IExecutionWorker = StreamWorkerAssembler.assemble(
            self.mock_connection,
            self.bundle,
            ProtocolMode.ASCII,
        )
        self.assertIsInstance(worker, IExecutionWorker)
        self.mock_connection.set_listener.assert_called_once()

    def test_assemble_binary_worker(self) -> None:
        '''
            Tests assembly of binary execution worker and listener binding.
        '''
        worker: IExecutionWorker = StreamWorkerAssembler.assemble(
            self.mock_connection,
            self.bundle,
            ProtocolMode.BINARY,
        )
        self.assertIsInstance(worker, IExecutionWorker)
        self.mock_connection.set_listener.assert_called_once()

    def test_get_version(self) -> None:
        '''
            Tests get_version returns string.
        '''
        self.assertIsInstance(StreamWorkerAssembler.get_version(), str)


if __name__ == '__main__':
    main()
