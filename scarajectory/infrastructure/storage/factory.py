# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Dedicated factory module for assembling and instantiating storage subsystem components.
'''

from __future__ import annotations

from scarajectory.infrastructure.storage.config_io.provides import ConfigIOProvides
from scarajectory.infrastructure.storage.dependencies import StorageDependencies
from scarajectory.infrastructure.storage.plan.dependencies import PlanDependencies
from scarajectory.infrastructure.storage.plan.factory import PlanFactory
from scarajectory.infrastructure.storage.plan.provides import PlanProvides
from scarajectory.infrastructure.storage.provides import StorageProvides
from scarajectory.infrastructure.storage.workspace.dependencies import WorkspaceDependencies
from scarajectory.infrastructure.storage.workspace.factory import WorkspaceFactory
from scarajectory.infrastructure.storage.workspace.provides import WorkspaceProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StorageFactory:
    '''
        Factory providing creation of storage subsystem components.

        It defines:

            :methods:
                | create - Constructs storage subsystem components with injected dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: StorageDependencies) -> StorageProvides:
        '''
            Assembles and instantiates storage subsystem components.

            :param dependencies: Injected StorageDependencies parameter bundle.
            :return: StorageProvides holding assembled storage adapters.
            :exceptions: None.
        '''
        plan_provides: PlanProvides = PlanFactory.create(
            PlanDependencies(
                config_loader=dependencies.io_loader,
                config_storer=dependencies.io_storer
            )
        )
        workspace_provides: WorkspaceProvides = WorkspaceFactory.create(
            WorkspaceDependencies(workspace_config=dependencies.workspace_config)
        )
        config_io_provides = ConfigIOProvides(
            config_loader=dependencies.io_loader,
            config_storer=dependencies.io_storer
        )

        return StorageProvides(
            plan_loader=plan_provides.plan_loader,
            plan_storer=plan_provides.plan_storer,
            workspace_manager=workspace_provides.workspace_manager,
            config_io_provides=config_io_provides,
            plan_storage_provides=plan_provides
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
