# -*- coding: UTF-8 -*-

'''
Module
    stream_pipeline_assembler.py
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
    Assembler constructing fully-wired streaming pipeline services.
'''

from __future__ import annotations

from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.service.state.session_factory import SessionFactory
from scarajectory.core.service.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.connection.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.connection.stream_raw_transceiver import StreamRawTransceiver
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.state.stream_state_machine import StreamStateMachine
from scarajectory.infrastructure.state.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.streaming.assembly.stream_pacing_assembler import StreamPacingAssembler
from scarajectory.infrastructure.streaming.assembly.stream_transport_assembler import StreamTransportAssembler
from scarajectory.infrastructure.streaming.assembly.stream_worker_assembler import StreamWorkerAssembler
from scarajectory.infrastructure.streaming.assembly.worker_bundle import WorkerBundle
from scarajectory.infrastructure.streaming.binary_program_streamer_factory import BinaryProgramStreamerFactory
from scarajectory.infrastructure.streaming.bundle import StreamingBundle
from scarajectory.infrastructure.streaming.stream_control_transmitter import StreamControlTransmitter
from scarajectory.infrastructure.streaming.stream_control_transmitter_factory import StreamControlTransmitterFactory
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher import StreamObserverDispatcher
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.streaming.stream_playback_controller import StreamPlaybackController
from scarajectory.infrastructure.streaming.stream_playback_controller_factory import StreamPlaybackControllerFactory
from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.transport_factory import TransportFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPipelineAssembler:
    '''
    Assembler constructing fully-wired streaming pipeline services.

    It defines:

        :methods:
            | assemble - Assembles streaming pipeline with explicit transport.
            | assemble_default - Assembles streaming with default transport.
            | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble(
        cls,
        transport: TransportBundle,
        *,
        queue_capacity: int = 16,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> StreamingBundle:
        '''
        Assembles streaming pipeline services and returns StreamingBundle.

        :param transport: Required TransportBundle parameter instance.
        :param queue_capacity: Flow control buffer capacity integer.
        :param protocol_mode: Active ProtocolMode enum value.
        :return: Fully wired StreamingBundle instance.
        '''
        conn_mgr: StreamConnectionManager
        raw_xceiver: StreamRawTransceiver
        conn_mgr, raw_xceiver = StreamTransportAssembler.assemble(
            transport, protocol_mode=protocol_mode
        )
        state_machine: StreamStateMachine = StreamStateMachineFactory.create()
        dispatcher: StreamObserverDispatcher = (
            StreamObserverDispatcherFactory.create()
        )
        pacing_bundle: FlowPacingBundle = StreamPacingAssembler.assemble(
            queue_capacity=queue_capacity
        )
        worker: IExecutionWorker = StreamWorkerAssembler.assemble(
            transport.connection,
            WorkerBundle(
                pacing_bundle=pacing_bundle,
                raw_transceiver=raw_xceiver,
                state_machine=state_machine,
                dispatcher=dispatcher,
            ),
            protocol_mode,
        )
        session: StreamSession = SessionFactory.create()
        ctrl_transmitter: StreamControlTransmitter = (
            StreamControlTransmitterFactory.create(
                raw_transceiver=raw_xceiver,
                frame_builder=BinaryFrameBuilderFactory.create(),
            )
        )
        playback_ctrl: StreamPlaybackController = (
            StreamPlaybackControllerFactory.create(
                connection=conn_mgr,
                barrier_coordinator=pacing_bundle.barrier_coordinator,
                state_machine=state_machine,
                dispatcher=dispatcher,
                worker=worker,
                control_transmitter=ctrl_transmitter,
                session=session,
                protocol_mode=protocol_mode,
            )
        )
        binary_streamer = BinaryProgramStreamerFactory().create(
            connection=conn_mgr,
            state_machine=state_machine,
            dispatcher=dispatcher,
            worker=worker,
            session=session,
        )

        return StreamingBundle(
            connection=conn_mgr,
            raw_channel=raw_xceiver,
            playback_controller=playback_ctrl,
            dispatcher=dispatcher,
            binary_streamer=binary_streamer,
        )

    @classmethod
    def assemble_default(
        cls,
        *,
        queue_capacity: int = 16,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> StreamingBundle:
        '''
        Assembles streaming pipeline using default transport.

        :param queue_capacity: Flow control buffer capacity integer.
        :param protocol_mode: Active ProtocolMode enum value.
        :return: Fully wired StreamingBundle instance.
        '''
        return cls.assemble(
            transport=TransportFactory.create_default_transport(),
            queue_capacity=queue_capacity,
            protocol_mode=protocol_mode,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns assembler version string.

        :return: Version string.
        '''
        return __version__
