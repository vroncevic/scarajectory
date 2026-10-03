# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Container bundle holding controls panel collaborator dependencies.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.mutation.iplan_mutation_service import IPlanMutationService
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.streaming.bundle import StreamingBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class ControlsBundle:
    '''
    Container bundle holding controls panel collaborator dependencies.

    It defines:

        :attributes:
            | store - Injected waypoint query port.
            | mutation - Injected plan mutation service.
            | validator - Injected trajectory validator port.
            | streaming - Injected streaming services bundle.
            | storage - Injected plan storage service.
            | dsl_service - Injected SCARA DSL service.
            | connection_repository - Injected connection repository port.
        :methods:
            | streamer - Returns streaming bundle for backward compatibility.
    '''

    store: IWaypointStore
    mutation: IPlanMutationService
    validator: ITrajectoryValidator
    streaming: StreamingBundle
    storage: IPlanStorageService
    dsl_service: IScaraDslService
    connection_repository: IConnectionRepository

    @property
    def streamer(self) -> StreamingBundle:
        '''
        Returns streaming subsystem services bundle.

        :return: StreamingBundle instance.
        '''
        return self.streaming
