# -*- coding: UTF-8 -*-

'''
Module
    app_runtime_assembler.py
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
from scarajectory.infrastructure.preferences.connection_repository import ConnectionRepository
from scarajectory.infrastructure.preferences.connection_repository_factory import ConnectionRepositoryFactory
from scarajectory.infrastructure.storage.plan_storage_service import PlanStorageService
from scarajectory.infrastructure.storage.plan_storage_service_factory import PlanStorageServiceFactory
from scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler import StreamPipelineAssembler
from scarajectory.infrastructure.streaming.bundle import StreamingBundle
from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.transport_factory import TransportFactory
from scarajectory.setup.assembly.app_runtime_bundle import AppRuntimeBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
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
        transport: TransportBundle = TransportFactory.create_default_transport()

        return cls.assemble_with_transport(
            context_bundle=context_bundle,
            transport=transport,
        )

    @classmethod
    def assemble_with_transport(
        cls,
        context_bundle: ContextBundle,
        transport: TransportBundle,
    ) -> AppRuntimeBundle:
        '''
        Constructs runtime services bundle with explicit transport.

        :param context_bundle: Application ContextBundle instance.
        :param transport: Injected TransportBundle communication instance.
        :return: AppRuntimeBundle holding configured runtime services.
        '''
        connection_repo: ConnectionRepository = (
            ConnectionRepositoryFactory.create(context_bundle=context_bundle)
        )
        streaming: StreamingBundle = StreamPipelineAssembler.assemble(
            transport=transport
        )
        storage: PlanStorageService = (
            PlanStorageServiceFactory.create_with_context(
                context_bundle=context_bundle
            )
        )

        return AppRuntimeBundle(
            connection_repo=connection_repo,
            transport=transport,
            streaming=streaming,
            storage=storage,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns assembler version string.

        :return: Version string.
        '''
        return __version__
