# -*- coding: UTF-8 -*-

'''
Module
    service_factory.py
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
    Factory module for assembling and instantiating Service instances.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.engine import Service
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServiceFactory:
    '''
        Factory responsible for assembling and instantiating Service instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a Service instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        validator: ITrajectoryValidator,
        storage: IPlanStorageService,
        store: IWaypointStore,
        mutation: IPlanBulkMutator,
    ) -> Service:
        '''
            Assembles and instantiates a Service instance.

            :param validator: ITrajectoryValidator instance.
            :param storage: IPlanStorageService instance.
            :param store: IWaypointStore instance.
            :param mutation: IPlanBulkMutator instance.
            :return: Fully assembled Service instance.
            :exceptions: None.
        '''
        return Service(
            validator=validator,
            storage=storage,
            store=store,
            mutation=mutation,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
