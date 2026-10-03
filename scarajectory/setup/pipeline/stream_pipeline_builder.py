# -*- coding: UTF-8 -*-

'''
Module
    stream_pipeline_builder.py
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
    Builder assembling streaming pipeline services and collaborator adapters.
'''

from __future__ import annotations

from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.service.state.session_factory import SessionFactory
from scarajectory.core.service.streaming.stream_pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.barrier.flow_barrier import FlowBarrier
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.connection.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.connection.stream_connection_manager_factory import StreamConnectionManagerFactory
from scarajectory.infrastructure.connection.stream_raw_transceiver import StreamRawTransceiver
from scarajectory.infrastructure.connection.stream_raw_transceiver_factory import StreamRawTransceiverFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.state.stream_state_machine import StreamStateMachine
from scarajectory.infrastructure.state.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.streaming.binary_program_streamer import BinaryProgramStreamer
from scarajectory.infrastructure.streaming.binary_program_streamer_factory import BinaryProgramStreamerFactory
from scarajectory.infrastructure.streaming.stream_control_transmitter import StreamControlTransmitter
from scarajectory.infrastructure.streaming.stream_control_transmitter_factory import StreamControlTransmitterFactory
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher import StreamObserverDispatcher
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.streaming.stream_playback_controller import StreamPlaybackController
from scarajectory.infrastructure.streaming.stream_playback_controller_factory import StreamPlaybackControllerFactory
from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.transport_factory import TransportFactory
from scarajectory.infrastructure.worker.stream_execution_worker import StreamExecutionWorker
from scarajectory.infrastructure.worker.stream_execution_worker_factory import StreamExecutionWorkerFactory
from scarajectory.setup.pipeline.stream_pipeline_bundle import StreamPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPipelineBuilder:
    '''
    Builder assembling streaming pipeline services and collaborator adapters.

    It defines:

        :methods:
            | build - Assembles StreamPipelineBundle with explicit transport.
            | build_default - Assembles StreamPipelineBundle with default transport.
            | get_version - Returns builder version string.
    '''

    @classmethod
    def build(
        cls,
        transport: TransportBundle,
    ) -> StreamPipelineBundle:
        '''
        Assembles streaming pipeline collaborators into StreamPipelineBundle.

        :param transport: Required TransportBundle parameter instance.
        :return: Fully assembled StreamPipelineBundle instance.
        '''
        connection: StreamConnectionManager = (
            StreamConnectionManagerFactory.create(
                connection=transport.connection,
                protocol_mode=ProtocolMode.BINARY,
            )
        )
        raw_transceiver: StreamRawTransceiver = (
            StreamRawTransceiverFactory.create(
                connection=transport.connection,
                transceiver=transport.transceiver,
            )
        )
        state_machine: StreamStateMachine = StreamStateMachineFactory.create()
        barrier: FlowBarrier = FlowBarrierFactory.create()
        pacing_bundle: FlowPacingBundle = FlowPacingBundleFactory.create(
            barrier=barrier
        )
        dispatcher: StreamObserverDispatcher = (
            StreamObserverDispatcherFactory.create()
        )
        session: StreamSession = SessionFactory.create()
        control_transmitter: StreamControlTransmitter = (
            StreamControlTransmitterFactory.create(
                raw_transceiver=raw_transceiver,
                frame_builder=BinaryFrameBuilderFactory.create(),
            )
        )
        worker: StreamExecutionWorker = StreamExecutionWorkerFactory.create(
            pacing_bundle=pacing_bundle,
            command_sender=raw_transceiver,
            state_controller=state_machine,
            observer_dispatcher=dispatcher,
            pacing_config=StreamPacingConfigFactory.create_binary(),
        )
        playback_controller: StreamPlaybackController = (
            StreamPlaybackControllerFactory.create(
                connection=connection,
                barrier_coordinator=pacing_bundle.barrier_coordinator,
                state_machine=state_machine,
                dispatcher=dispatcher,
                worker=worker,
                control_transmitter=control_transmitter,
                session=session,
                protocol_mode=ProtocolMode.BINARY,
            )
        )
        binary_streamer: BinaryProgramStreamer = (
            BinaryProgramStreamerFactory().create(
                connection=connection,
                state_machine=state_machine,
                dispatcher=dispatcher,
                worker=worker,
                session=session,
            )
        )

        return StreamPipelineBundle(
            connection=connection,
            raw_channel=raw_transceiver,
            playback_controller=playback_controller,
            binary_streamer=binary_streamer,
            dispatcher=dispatcher,
        )

    @classmethod
    def build_default(cls) -> StreamPipelineBundle:
        '''
        Assembles StreamPipelineBundle using default TransportBundle.

        :return: Fully assembled StreamPipelineBundle instance.
        '''
        return cls.build(TransportFactory.create_default_transport())

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns builder version string.

        :return: Version string.
        '''
        return __version__
