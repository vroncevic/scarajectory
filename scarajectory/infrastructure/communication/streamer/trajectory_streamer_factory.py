# -*- coding: UTF-8 -*-

'''
Module
    trajectory_streamer_factory.py
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
    Factory assembling TrajectoryStreamer instances with full collaborator dependency injection.
'''

from __future__ import annotations

from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.service.communication.stream.iexecution_worker import IExecutionWorker
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scarajectory.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scarajectory.infrastructure.communication.controller.robot_controller import RobotController
from scarajectory.infrastructure.communication.controller.robot_controller_factory import RobotControllerFactory
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder import BinaryFrameBuilder
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.communication.streamer.binary_packet_strategy import BinaryPacketStrategy
from scarajectory.infrastructure.communication.streamer.binary_packet_strategy_factory import BinaryPacketStrategyFactory
from scarajectory.infrastructure.communication.streamer.binary_stream_execution_worker_factory import BinaryStreamExecutionWorkerFactory
from scarajectory.infrastructure.communication.streamer.flow_controller import FlowController
from scarajectory.infrastructure.communication.streamer.flow_controller_factory import FlowControllerFactory
from scarajectory.infrastructure.communication.streamer.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.communication.streamer.stream_connection_manager_factory import StreamConnectionManagerFactory
from scarajectory.infrastructure.communication.streamer.stream_execution_worker_factory import StreamExecutionWorkerFactory
from scarajectory.infrastructure.communication.streamer.stream_observer_dispatcher import StreamObserverDispatcher
from scarajectory.infrastructure.communication.streamer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.communication.streamer.stream_state_machine import StreamStateMachine
from scarajectory.infrastructure.communication.streamer.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.communication.streamer.trajectory_streamer import TrajectoryStreamer
from scarajectory.infrastructure.communication.transport.itransport import ITransport
from scarajectory.infrastructure.communication.transport.transport_factory import TransportFactory
from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryStreamerFactory:
    '''
    Factory assembling TrajectoryStreamer instances with full collaborator dependency injection.

    It defines:

        :methods:
            | create - Constructs and fully wires TrajectoryStreamer with external transport.
            | create_default - Constructs TrajectoryStreamer using default transport.
            | create_with_collaborators - Constructs TrajectoryStreamer with custom collaborators.
            | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        transport: ITransport,
        queue_capacity: int = 16,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> TrajectoryStreamer:
        '''
        Constructs and returns a fully wired TrajectoryStreamer instance with injected transport.

        :param transport: Required ITransport implementation instance.
        :param queue_capacity: Flow control buffer capacity integer (default 16).
        :param protocol_mode: Active ProtocolMode enum value (default BINARY).
        :return: Fully wired TrajectoryStreamer instance.
        '''
        conn_manager: StreamConnectionManager = StreamConnectionManagerFactory.create(
            transport,
            protocol_mode=protocol_mode,
        )
        state_machine: StreamStateMachine = StreamStateMachineFactory.create()
        dispatcher: StreamObserverDispatcher = StreamObserverDispatcherFactory.create()
        flow_controller: FlowController = FlowControllerFactory.create(
            capacity=queue_capacity
        )
        frame_builder: BinaryFrameBuilder = BinaryFrameBuilderFactory.create()

        streamer = TrajectoryStreamer(
            connection_manager=conn_manager,
            flow_controller=flow_controller,
            state_machine=state_machine,
            dispatcher=dispatcher,
            frame_builder=frame_builder,
            protocol_mode=protocol_mode,
        )

        worker: IExecutionWorker
        if protocol_mode == ProtocolMode.BINARY:
            loader = ScaraConfigLoaderFactory.create()
            bounds: ScaraBounds = loader.load_bounds()
            transmission: TransmissionParameters = loader.load_transmission()
            kinematics: IKinematicsService = KinematicsServiceFactory.create(
                bounds=bounds
            )
            packet_strategy: BinaryPacketStrategy = (
                BinaryPacketStrategyFactory.create(
                    kinematics=kinematics,
                    transmission=transmission,
                )
            )
            worker = BinaryStreamExecutionWorkerFactory.create(
                flow_controller=flow_controller,
                packet_strategy=packet_strategy,
                send_bytes=streamer.send_raw_bytes,
                notify_progress=streamer.notify_progress,
                notify_log=streamer.on_connection_log,
                on_state_change=streamer.on_worker_state_change,
            )
        else:
            worker = StreamExecutionWorkerFactory.create(
                flow_controller=flow_controller,
                send_command=streamer.send_raw_command,
                notify_progress=streamer.notify_progress,
                notify_log=streamer.on_connection_log,
                on_state_change=streamer.on_worker_state_change,
            )
        streamer.set_worker(worker)

        robot_controller: RobotController = RobotControllerFactory.create(
            streamer,
            protocol_mode=protocol_mode,
        )
        streamer.set_robot_controller(robot_controller)

        return streamer

    @classmethod
    def create_default(
        cls,
        *,
        queue_capacity: int = 16,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> TrajectoryStreamer:
        '''
        Constructs TrajectoryStreamer using the default transport mechanism.

        :param queue_capacity: Flow control buffer capacity integer (default 16).
        :param protocol_mode: Active ProtocolMode enum value (default BINARY).
        :return: Fully wired TrajectoryStreamer instance.
        '''
        return cls.create(
            transport=TransportFactory.create_default_transport(),
            queue_capacity=queue_capacity,
            protocol_mode=protocol_mode,
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        connection_manager: StreamConnectionManager,
        flow_controller: FlowController,
        state_machine: StreamStateMachine,
        dispatcher: StreamObserverDispatcher,
        worker: IExecutionWorker,
        robot_controller: RobotController,
        frame_builder: BinaryFrameBuilder,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> TrajectoryStreamer:
        '''
        Constructs TrajectoryStreamer with explicitly provided custom collaborators.

        :param connection_manager: StreamConnectionManager instance.
        :param flow_controller: FlowController instance.
        :param state_machine: StreamStateMachine instance.
        :param dispatcher: StreamObserverDispatcher instance.
        :param worker: IExecutionWorker instance.
        :param robot_controller: RobotController instance.
        :param frame_builder: BinaryFrameBuilder instance.
        :param protocol_mode: Active ProtocolMode enum value.
        :return: TrajectoryStreamer instance.
        '''
        return TrajectoryStreamer(
            connection_manager=connection_manager,
            flow_controller=flow_controller,
            state_machine=state_machine,
            dispatcher=dispatcher,
            worker=worker,
            robot_controller=robot_controller,
            frame_builder=frame_builder,
            protocol_mode=protocol_mode,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns factory version string.

        :return: Factory version string.
        '''
        return __version__

