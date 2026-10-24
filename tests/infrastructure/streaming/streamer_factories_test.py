# -*- coding: UTF-8 -*-

'''
Module
    streamer_factories_test.py
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
    Unit tests for streamer sub-factories.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaracom.bridge.transceiver.ichannel import IRawChannel
from scaracom.flow.barrier.ibarrier import IFlowBarrier

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.observer.iregistry import IStreamObserverRegistry
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.infrastructure.barrier.factory import BarrierFactory
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.state.dependencies import StateDependencies
from scarajectory.infrastructure.state.factory import StateFactory
from scarajectory.infrastructure.streaming.assembly.stream_pacing_assembler import StreamPacingAssembler
from scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler import StreamPipelineAssembler
from scarajectory.infrastructure.streaming.binary.istreamer import IBinaryStreamer
from scarajectory.infrastructure.streaming.observer.factory import ObserverFactory
from scarajectory.infrastructure.streaming.provides import StreamingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerFactoriesTestCase(TestCase):
    '''
        Test cases verifying factory instantiation of sub-components.

        It defines:

            :methods:
                | test_barrier_and_flow_controller_factories - Tests flow barrier and pacing.
                | test_state_factory - Tests StateFactory.
                | test_observer_dispatcher_factory - Tests StreamObserverDispatcherFactory.
                | test_stream_pipeline_assembler - Tests StreamPipelineAssembler assembly.
    '''

    def test_barrier_and_flow_controller_factories(self) -> None:
        '''
            Tests FlowBarrier and FlowController factories.

            :exceptions: None.
        '''
        flow_barrier = BarrierFactory.create().flow_barrier
        self.assertIsInstance(flow_barrier, IFlowBarrier)
        self.assertTrue(flow_barrier.is_barrier_clear())

        pacing_provides = StreamPacingAssembler.assemble(queue_capacity=10)
        self.assertEqual(
            getattr(pacing_provides.flow_pacing_controller, 'capacity'),
            10,
        )
        self.assertTrue(
            pacing_provides.flow_barrier_coordinator.is_barrier_clear()
        )

    def test_state_factory(self) -> None:
        '''
            Tests StateFactory.

            :exceptions: None.
        '''
        state_machine = StateFactory.create(StateDependencies()).stream_state_machine
        self.assertEqual(state_machine.state, StreamState.IDLE)
        state_machine.transition_to(StreamState.STREAMING)
        self.assertEqual(state_machine.state, StreamState.STREAMING)

    def test_observer_dispatcher_factory(self) -> None:
        '''
            Tests StreamObserverDispatcherFactory.

            :exceptions: None.
        '''
        observer_provides = ObserverFactory.create()
        self.assertIsInstance(
            observer_provides.stream_observer_dispatcher,
            IStreamObserverDispatcher,
        )
        self.assertEqual(
            len(observer_provides.stream_observer_registry.get_observers()),
            0,
        )

    def test_stream_pipeline_assembler(self) -> None:
        '''
            Tests StreamPipelineAssembler assembly and fine-grained interface contracts.

            :exceptions: None.
        '''
        bundle = StreamPipelineAssembler.assemble_default()
        self.assertIsInstance(bundle, StreamingProvides)
        self.assertIsInstance(bundle.connection_manager, IConnectionManager)
        self.assertIsInstance(bundle.raw_channel, IRawChannel)
        self.assertIsInstance(bundle.playback_controller, IPlaybackController)
        self.assertIsInstance(bundle.registry, IStreamObserverRegistry)
        self.assertIsInstance(bundle.dispatcher, IStreamObserverDispatcher)
        self.assertIsInstance(bundle.binary_streamer, IBinaryStreamer)


if __name__ == '__main__':
    main()
