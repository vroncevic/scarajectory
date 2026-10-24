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

from ats_utilities.context.factory import ContextBundleFactory

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.duration.factory import SegmentDurationCalculatorFactory
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.parser.factory import ParserFactory

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.infrastructure.connection.listener.factory import StreamTransportListenerFactory
from scarajectory.infrastructure.packet.dependencies import PacketDependencies
from scarajectory.infrastructure.packet.factory import PacketFactory
from scarajectory.infrastructure.packet.istrategy import IPacketStrategy
from scarajectory.infrastructure.scaralang.discretizer.dependencies import DiscretizerDependencies
from scarajectory.infrastructure.scaralang.discretizer.factory import DualElbowStepDiscretizerFactory
from scarajectory.infrastructure.settings.communication.dependencies import CommunicationSettingsDependencies
from scarajectory.infrastructure.settings.communication.factory import CommunicationSettingsFactory
from scarajectory.infrastructure.settings.communication.loader import CommunicationSettingsLoader
from scarajectory.infrastructure.settings.dependencies import SettingsDependencies
from scarajectory.infrastructure.settings.factory import SettingsFactory
from scarajectory.infrastructure.settings.provides import SettingsProvides
from scarajectory.infrastructure.settings.reader.reader import SettingsReader
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory
from scarajectory.infrastructure.streaming.assembly.worker_bundle import WorkerBundle
from scarajectory.infrastructure.worker.dependencies import WorkerDependencies
from scarajectory.infrastructure.worker.factory import WorkerFactory
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.worker.parser.bundle import ParserBundle
from scarajectory.infrastructure.worker.provides import WorkerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
                | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble_binary(
        cls,
        connection: IConnectionCoordinator,
        bundle: WorkerBundle,
    ) -> IExecutionWorker:
        '''
            Constructs and binds binary execution worker and transport listener.

            :param connection: Injected IStreamTransportConnection instance.
            :param bundle: Injected WorkerBundle parameter object.
            :return: Fully configured binary IExecutionWorker instance.
            :exceptions: None.
        '''
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(
                context_bundle=ContextBundleFactory.create_bundle()
            )
        )
        settings_provides: SettingsProvides = SettingsFactory.create(
            SettingsDependencies(
                config_loader=io_provides.config_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        bounds: ScaraBounds = (
            settings_provides.bounds_provides.bounds_loader.load_bounds()
        )
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        converter: IJointStepTransmissionConverter = (
            TransmissionFactory.create(
                transmission=settings_provides.transmission_provides.transmission_loader.load_transmission()
            )
        )
        discretizer: IStepDiscretizer = DualElbowStepDiscretizerFactory.create(
            dependencies=DiscretizerDependencies(
                spatial=kinematics_provides.spatial,
                numerical_spatial=kinematics_provides.numerical_spatial,
                transmission=converter,
                duration_calculator=SegmentDurationCalculatorFactory.create(),
                bounds=bounds,
            ),
        )
        builder_provides = BuilderFactory.create()
        packet_strategy: IPacketStrategy = PacketFactory.create(
            dependencies=PacketDependencies(
                step_discretizer=discretizer,
                motion_frame_builder=builder_provides.motion,
                frame_packer=builder_provides.packer,
            )
        ).packet_strategy
        pacing_config: StreamPacingConfig = (
            CommunicationSettingsFactory.create(
                CommunicationSettingsDependencies(
                    config_loader=io_provides.config_loader,
                    config_path=CommunicationSettingsLoader.DEFAULT_COMMUNICATION_CONFIG,
                    scheme_path=CommunicationSettingsLoader.DEFAULT_SCHEME_CONFIG,
                )
            ).settings_loader.load_pacing_config()
        )
        parser_provides = ParserFactory.create()
        parser_bundle: ParserBundle = ParserBundle(
            frame_parser=parser_provides.parser,
            response_unpacker=parser_provides.response_unpacker,
        )
        worker_provides: WorkerProvides = WorkerFactory.create(
            WorkerDependencies(
                pacing_bundle=bundle.pacing_bundle,
                packet_strategy=packet_strategy,
                byte_sender=bundle.raw_transceiver,
                state_controller=bundle.state_machine,
                observer_dispatcher=bundle.dispatcher,
                pacing_config=pacing_config,
                parser_bundle=parser_bundle,
            )
        )
        connection.set_listener(
            StreamTransportListenerFactory.create(
                bytes_receiver=worker_provides.bytes_receiver,
                dispatcher=bundle.dispatcher,
            )
        )

        return worker_provides.execution_worker

    @classmethod
    def assemble(
        cls,
        connection: IConnectionCoordinator,
        bundle: WorkerBundle,
    ) -> IExecutionWorker:
        '''
            Constructs and binds worker.

            :param connection: Injected IStreamTransportConnection instance.
            :param bundle: Injected WorkerBundle parameter object.
            :return: Fully configured IExecutionWorker instance.
            :exceptions: None.
        '''
        return cls.assemble_binary(connection, bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
