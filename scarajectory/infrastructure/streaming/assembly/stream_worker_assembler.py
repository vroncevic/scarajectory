# -*- coding: UTF-8 -*-

'''
Module
    stream_worker_assembler.py
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
    Assembles execution worker and transport listener for streaming.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.streaming.stream_pacing_config_factory import StreamPacingConfigFactory
from scarajectory.core.service.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.packet.binary_packet_strategy import BinaryPacketStrategy
from scarajectory.infrastructure.packet.binary_packet_strategy_factory import BinaryPacketStrategyFactory
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.infrastructure.settings.transmission.scara_transmission_loader_factory import ScaraTransmissionLoaderFactory
from scarajectory.infrastructure.streaming.assembly.worker_bundle import WorkerBundle
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.listener.stream_ascii_transport_listener import StreamAsciiTransportListener
from scarajectory.infrastructure.transport.listener.stream_ascii_transport_listener_factory import StreamAsciiTransportListenerFactory
from scarajectory.infrastructure.transport.listener.stream_binary_transport_listener import StreamBinaryTransportListener
from scarajectory.infrastructure.transport.listener.stream_binary_transport_listener_factory import StreamBinaryTransportListenerFactory
from scarajectory.infrastructure.worker.binary.binary_stream_execution_worker_factory import BinaryStreamExecutionWorkerFactory
from scarajectory.infrastructure.worker.stream_execution_worker_factory import StreamExecutionWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamWorkerAssembler:
    '''
        Sub-assembler for stream execution workers and transport listeners.

        It defines:

            :methods:
                | assemble - Constructs worker based on protocol mode.
                | assemble_binary - Constructs BinaryStreamExecutionWorker.
                | assemble_ascii - Constructs StreamExecutionWorker.
                | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble_binary(
        cls,
        connection: IStreamTransportConnection,
        bundle: WorkerBundle,
    ) -> IExecutionWorker:
        '''
            Constructs and binds binary execution worker and transport listener.

            :param connection: Injected IStreamTransportConnection instance.
            :param bundle: Injected WorkerBundle parameter object.
            :return: Fully configured binary IExecutionWorker instance.
            :exceptions: None.
        '''
        bounds_loader = ScaraBoundsLoaderFactory.create()
        trans_loader = ScaraTransmissionLoaderFactory.create()
        bounds: ScaraBounds = bounds_loader.load_bounds()
        transmission: TransmissionParameters = trans_loader.load_transmission()
        kinematics: IKinematicsService = KinematicsServiceFactory.create(
            bounds=bounds
        )
        packet_strategy: BinaryPacketStrategy = (
            BinaryPacketStrategyFactory.create(
                kinematics=kinematics,
                transmission=transmission,
            )
        )
        pacing_config = StreamPacingConfigFactory.create_binary()
        worker: IExecutionWorker = BinaryStreamExecutionWorkerFactory.create(
            pacing_bundle=bundle.pacing_bundle,
            packet_strategy=packet_strategy,
            byte_sender=bundle.raw_transceiver,
            state_controller=bundle.state_machine,
            observer_dispatcher=bundle.dispatcher,
            pacing_config=pacing_config,
        )
        binary_listener: StreamBinaryTransportListener = (
            StreamBinaryTransportListenerFactory.create(
                bytes_receiver=worker,
                dispatcher=bundle.dispatcher,
            )
        )
        connection.set_listener(binary_listener)

        return worker

    @classmethod
    def assemble_ascii(
        cls,
        connection: IStreamTransportConnection,
        bundle: WorkerBundle,
    ) -> IExecutionWorker:
        '''
            Constructs and binds ascii execution worker and transport listener.

            :param connection: Injected IStreamTransportConnection instance.
            :param bundle: Injected WorkerBundle parameter object.
            :return: Fully configured ascii IExecutionWorker instance.
            :exceptions: None.
        '''
        ascii_pacing_config = StreamPacingConfigFactory.create_ascii()
        ascii_worker: IExecutionWorker = StreamExecutionWorkerFactory.create(
            pacing_bundle=bundle.pacing_bundle,
            command_sender=bundle.raw_transceiver,
            state_controller=bundle.state_machine,
            observer_dispatcher=bundle.dispatcher,
            pacing_config=ascii_pacing_config,
        )
        ascii_listener: StreamAsciiTransportListener = (
            StreamAsciiTransportListenerFactory.create(
                line_receiver=ascii_worker,
                dispatcher=bundle.dispatcher,
            )
        )
        connection.set_listener(ascii_listener)

        return ascii_worker

    @classmethod
    def assemble(
        cls,
        connection: IStreamTransportConnection,
        bundle: WorkerBundle,
        protocol_mode: ProtocolMode,
    ) -> IExecutionWorker:
        '''
            Constructs and binds worker based on active protocol mode.

            :param connection: Injected IStreamTransportConnection instance.
            :param bundle: Injected WorkerBundle parameter object.
            :param protocol_mode: Active protocol mode enum.
            :return: Fully configured IExecutionWorker instance.
            :exceptions: None.
        '''
        if protocol_mode == ProtocolMode.BINARY:
            return cls.assemble_binary(connection, bundle)

        return cls.assemble_ascii(connection, bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
