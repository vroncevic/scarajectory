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

from scaracom.transport.factory import TransportFactory
from scaracom.transport.itransport import ITransport

from scaralang.infrastructure.protocol.builder.factory import BuilderFactory

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.connection.listener.factory import StreamTransportListenerFactory
from scarajectory.infrastructure.connection.listener.listener import StreamTransportListener
from scarajectory.infrastructure.connection.receiver.bootstrap import BootstrapBytesReceiver
from scarajectory.infrastructure.pacing.provides import PacingProvides
from scarajectory.infrastructure.state.dependencies import StateDependencies
from scarajectory.infrastructure.state.factory import StateFactory
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.streaming.assembly.stream_pacing_assembler import StreamPacingAssembler
from scarajectory.infrastructure.streaming.assembly.stream_transport_assembler import StreamTransportAssembler
from scarajectory.infrastructure.streaming.assembly.stream_worker_assembler import StreamWorkerAssembler
from scarajectory.infrastructure.streaming.assembly.worker_bundle import WorkerBundle
from scarajectory.infrastructure.streaming.binary.dependencies import BinaryDependencies
from scarajectory.infrastructure.streaming.binary.factory import BinaryFactory
from scarajectory.infrastructure.streaming.control.dependencies import ControlDependencies
from scarajectory.infrastructure.streaming.control.factory import ControlFactory
from scarajectory.infrastructure.streaming.observer.factory import ObserverFactory
from scarajectory.infrastructure.streaming.playback.dependencies import PlaybackDependencies
from scarajectory.infrastructure.streaming.playback.factory import PlaybackFactory
from scarajectory.infrastructure.streaming.provides import StreamingProvides
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
        transport: ITransport,
        *,
        queue_capacity: int = 16,
    ) -> StreamingProvides:
        '''
            Assembles streaming pipeline services and returns StreamingProvides.

            :param transport: Required ITransport parameter instance.
            :param queue_capacity: Flow control buffer capacity integer.
            :return: Fully wired StreamingProvides instance.
        '''
        state_machine: IStreamStateMachine = StateFactory.create(
            StateDependencies()
        ).stream_state_machine
        observer_provides = ObserverFactory.create()
        initial_receiver: BootstrapBytesReceiver = BootstrapBytesReceiver()
        listener: StreamTransportListener = StreamTransportListenerFactory.create(
            dispatcher=observer_provides.stream_observer_dispatcher,
            bytes_receiver=initial_receiver,
        )
        transport_bundle = StreamTransportAssembler.assemble(
            transport,
            listener=listener,
        )
        pacing_provides: PacingProvides = StreamPacingAssembler.assemble(
            queue_capacity=queue_capacity
        )
        worker: IExecutionWorker = StreamWorkerAssembler.assemble(
            transport_bundle[2],
            WorkerBundle(
                pacing_provides=pacing_provides,
                raw_transceiver=transport_bundle[1],
                state_machine=state_machine,
                dispatcher=observer_provides.stream_observer_dispatcher,
            ),
        )
        builders = BuilderFactory.create()
        ctrl_transmitter = ControlFactory.create(
            ControlDependencies(
                raw_transceiver=transport_bundle[1],
                system_builder=builders.system,
                frame_packer=builders.packer,
            )
        ).control_transmitter
        playback_ctrl = PlaybackFactory.create(
            PlaybackDependencies(
                connection_manager=transport_bundle[0],
                flow_barrier_coordinator=pacing_provides.flow_barrier_coordinator,
                stream_state_machine=state_machine,
                stream_observer_dispatcher=observer_provides.stream_observer_dispatcher,
                execution_worker=worker,
                control_transmitter=ctrl_transmitter,
            )
        ).playback_controller
        session: StreamSession = SessionFactory.create_default()

        return StreamingProvides(
            connection_manager=transport_bundle[0],
            raw_channel=transport_bundle[1],
            playback_controller=playback_ctrl,
            registry=observer_provides.stream_observer_registry,
            dispatcher=observer_provides.stream_observer_dispatcher,
            binary_streamer=BinaryFactory.create(
                BinaryDependencies(
                    connection_manager=transport_bundle[0],
                    stream_state_machine=state_machine,
                    stream_observer_dispatcher=observer_provides.stream_observer_dispatcher,
                    execution_worker=worker,
                    session=session,
                )
            ).binary_streamer,
        )

    @classmethod
    def assemble_default(
        cls,
        *,
        queue_capacity: int = 16,
    ) -> StreamingProvides:
        '''
            Assembles streaming pipeline using default transport.

            :param queue_capacity: Flow control buffer capacity integer.
            :return: Fully wired StreamingProvides instance.
        '''
        return cls.assemble(
            transport=TransportFactory.create(),
            queue_capacity=queue_capacity,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
        '''
        return __version__
