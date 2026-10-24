# -*- coding: UTF-8 -*-

'''
Module
    assembler.py
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
    Dedicated sub-assembler for transport, streaming, and storage services.
'''

from __future__ import annotations

from ats_utilities.context.bundle import ContextBundle

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.factory import TransportFactory
from scaracom.transport.itransport import ITransport

from scarajectory.core.model.streaming.config import StreamConfig
from scarajectory.infrastructure.preferences.dependencies import PreferencesDependencies
from scarajectory.infrastructure.preferences.factory import PreferencesFactory
from scarajectory.infrastructure.preferences.provides import PreferencesProvides
from scarajectory.infrastructure.settings.communication.dependencies import CommunicationSettingsDependencies
from scarajectory.infrastructure.settings.communication.factory import CommunicationSettingsFactory
from scarajectory.infrastructure.settings.communication.loader import CommunicationSettingsLoader
from scarajectory.infrastructure.settings.communication.provides import CommunicationSettingsProvides
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory
from scarajectory.infrastructure.storage.dependencies import StorageDependencies
from scarajectory.infrastructure.storage.factory import StorageFactory
from scarajectory.infrastructure.storage.provides import StorageProvides
from scarajectory.infrastructure.storage.workspace.config import WorkspaceConfig
from scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler import StreamPipelineAssembler
from scarajectory.infrastructure.streaming.provides import StreamingProvides
from scarajectory.setup.assembly.runtime.bundle import AppRuntimeBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppRuntimeAssembler:
    '''
    Assembles runtime storage, hardware transport, and streaming services.

    It defines:

        :methods:
            | assemble - Constructs runtime bundle with default transport.
            | assemble_with_transport - Constructs bundle with transport.
            | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble(cls, context_bundle: ContextBundle) -> AppRuntimeBundle:
        '''
        Constructs runtime services bundle with default hardware transport.

        :param context_bundle: Application ContextBundle instance.
        :return: AppRuntimeBundle holding configured runtime services.
        '''
        transport: ITransport = TransportFactory.create()

        return cls.assemble_with_transport(
            context_bundle=context_bundle,
            transport=transport,
        )

    @classmethod
    def assemble_with_transport(
        cls,
        context_bundle: ContextBundle,
        transport: ITransport,
    ) -> AppRuntimeBundle:
        '''
        Constructs runtime services bundle with explicit transport.

        :param context_bundle: Application ContextBundle instance.
        :param transport: Injected ITransport communication instance.
        :return: AppRuntimeBundle holding configured runtime services.
        '''
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=context_bundle)
        )
        preferences: PreferencesProvides = PreferencesFactory.create(
            PreferencesDependencies(
                config_loader=io_provides.config_loader,
                config_storer=io_provides.config_storer,
            )
        )
        connection_repo: ISerialPreferenceRepository = preferences.serial_repository
        comm_provides: CommunicationSettingsProvides = CommunicationSettingsFactory.create(
            CommunicationSettingsDependencies(
                config_loader=io_provides.config_loader,
                config_path=CommunicationSettingsLoader.DEFAULT_COMMUNICATION_CONFIG,
                scheme_path=CommunicationSettingsLoader.DEFAULT_SCHEME_CONFIG,
            )
        )
        stream_config: StreamConfig = comm_provides.settings_loader.load_stream_config()
        streaming: StreamingProvides = StreamPipelineAssembler.assemble(
            transport=transport,
            queue_capacity=stream_config.queue_capacity,
        )
        storage_provides: StorageProvides = StorageFactory.create(
            StorageDependencies(
                io_loader=io_provides.config_loader,
                io_storer=io_provides.config_storer,
                workspace_config=WorkspaceConfig(),
            )
        )

        return AppRuntimeBundle(
            connection_repo=connection_repo,
            transport=transport,
            streaming=streaming,
            loader=storage_provides.plan_loader,
            storer=storage_provides.plan_storer,
            workspace=storage_provides.workspace_manager,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns assembler version string.

        :return: Version string.
        '''
        return __version__
