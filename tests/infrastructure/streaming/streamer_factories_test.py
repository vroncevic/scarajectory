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
from unittest.mock import MagicMock

from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.service.barrier.iflow_barrier import IFlowBarrier
from scarajectory.core.service.classifier.iflow_status_classifier import IFlowStatusClassifier
from scarajectory.core.service.classifier.ihoming_status_classifier import IHomingStatusClassifier
from scarajectory.core.service.classifier.imotion_status_classifier import IMotionStatusClassifier
from scarajectory.core.service.classifier.iresponse_parser import IResponseParser
from scarajectory.core.service.connection.iconnection import IConnection
from scarajectory.core.service.connection.iraw_channel import IRawChannel
from scarajectory.core.service.streaming.ibinary_program_streamer import IBinaryProgramStreamer
from scarajectory.core.service.streaming.istream_dispatcher import IStreamDispatcher
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.core.service.streaming.stream_pacing_config_factory import StreamPacingConfigFactory
from scarajectory.core.service.worker.icommand_formatter import ICommandFormatter
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.classifier.status.flow_status_classifier_factory import FlowStatusClassifierFactory
from scarajectory.infrastructure.classifier.status.homing_status_classifier_factory import HomingStatusClassifierFactory
from scarajectory.infrastructure.classifier.status.motion_status_classifier_factory import MotionStatusClassifierFactory
from scarajectory.infrastructure.classifier.response_parser_factory import ResponseParserFactory
from scarajectory.infrastructure.formatter.command_formatter_factory import CommandFormatterFactory
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.state.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler import StreamPipelineAssembler
from scarajectory.infrastructure.streaming.bundle import StreamingBundle
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.worker.stream_execution_worker_factory import StreamExecutionWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerFactoriesTestCase(TestCase):
    '''
        Test cases verifying factory instantiation of sub-components.
    '''

    def test_classifier_and_formatter_factories(self) -> None:
        '''
            Tests classifier and command formatter factories.
        '''
        flow_classifier = FlowStatusClassifierFactory.create()
        self.assertIsInstance(flow_classifier, IFlowStatusClassifier)

        homing_classifier = HomingStatusClassifierFactory.create()
        self.assertIsInstance(homing_classifier, IHomingStatusClassifier)

        motion_classifier = MotionStatusClassifierFactory.create()
        self.assertIsInstance(motion_classifier, IMotionStatusClassifier)

        response_parser = ResponseParserFactory.create()
        self.assertIsInstance(response_parser, IResponseParser)

        cmd_formatter = CommandFormatterFactory.create()
        self.assertIsInstance(cmd_formatter, ICommandFormatter)

    def test_barrier_and_flow_controller_factories(self) -> None:
        '''
            Tests FlowBarrier and FlowController factories.
        '''
        barrier = FlowBarrierFactory.create()
        self.assertIsInstance(barrier, IFlowBarrier)
        self.assertTrue(barrier.is_barrier_clear())

        pacing_bundle = FlowPacingBundleFactory.create(barrier=barrier, capacity=10)
        self.assertEqual(pacing_bundle.pacing_controller.capacity, 10)
        self.assertTrue(pacing_bundle.barrier_coordinator.is_barrier_clear())

    def test_state_machine_factory(self) -> None:
        '''
            Tests StreamStateMachineFactory.
        '''
        state_machine = StreamStateMachineFactory.create()
        self.assertEqual(state_machine.state, StreamState.IDLE)
        state_machine.transition_to(StreamState.STREAMING)
        self.assertEqual(state_machine.state, StreamState.STREAMING)

    def test_observer_dispatcher_factory(self) -> None:
        '''
            Tests StreamObserverDispatcherFactory.
        '''
        dispatcher = StreamObserverDispatcherFactory.create()
        self.assertFalse(dispatcher.has_observers())

    def test_execution_worker_factory(self) -> None:
        '''
            Tests StreamExecutionWorkerFactory.
        '''
        mock_sender = MagicMock()
        barrier = FlowBarrierFactory.create()
        pacing_bundle = FlowPacingBundleFactory.create(barrier=barrier, capacity=8)
        state_controller = StreamStateMachineFactory.create()
        observer_dispatcher = StreamObserverDispatcherFactory.create()
        pacing_config = StreamPacingConfigFactory.create_ascii()

        worker = StreamExecutionWorkerFactory.create(
            pacing_bundle=pacing_bundle,
            command_sender=mock_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )
        self.assertFalse(worker.is_running())

    def test_stream_pipeline_assembler(self) -> None:
        '''
            Tests StreamPipelineAssembler assembly and fine-grained interface contracts.
        '''
        bundle = StreamPipelineAssembler.assemble_default()
        self.assertIsInstance(bundle, StreamingBundle)
        self.assertIsInstance(bundle.connection, IConnection)
        self.assertIsInstance(bundle.raw_channel, IRawChannel)
        self.assertIsInstance(bundle.playback_controller, IStreamPlaybackController)
        self.assertIsInstance(bundle.dispatcher, IStreamDispatcher)
        self.assertIsInstance(bundle.binary_streamer, IBinaryProgramStreamer)


if __name__ == '__main__':
    main()
