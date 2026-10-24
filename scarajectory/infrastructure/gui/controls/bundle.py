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

from scaracom.transport.preference.irepository import ISerialPreferenceRepository

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.storage_dependencies import StorageDependencies
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.provides import ScaralangProvides
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager
from scarajectory.infrastructure.streaming.provides import StreamingProvides
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class ControlsBundle:
    '''
    Container bundle holding controls panel collaborator dependencies.

    It defines:

        :attributes:
            | plan - Trajectory plan management pipeline bundle.
            | validator - Injected trajectory validator port.
            | streaming - Injected streaming services provides container.
            | dsl - Injected SCARA DSL pipeline bundle.
            | connection_repository - Injected connection repository port.
            | storage - Injected storage dependencies bundle.
            | scaralang - Injected scaralang subsystem provides container.
        :properties:
            | store - Injected waypoint query port.
            | mutation - Injected plan mutation service.
            | loader - Injected plan loader port.
            | storer - Injected plan storer port.
            | workspace - Injected workspace manager for examples.
            | avoidance_adapter - Dead zone avoidance and bypass adapter.
    '''

    plan: PlanPipelineBundle
    validator: ITrajectoryValidator
    streaming: StreamingProvides
    dsl: DslPipelineBundle
    connection_repository: ISerialPreferenceRepository
    storage: StorageDependencies
    scaralang: ScaralangProvides

    @property
    def store(self) -> IWaypointStore:
        '''
        Returns waypoint query and storage port.

        :return: IWaypointStore instance.
        '''
        return self.plan.store

    @property
    def mutation(self) -> IPlanBulkMutator:
        '''
        Returns plan mutation service port.

        :return: IPlanBulkMutator instance.
        '''
        return self.plan.mutation

    @property
    def loader(self) -> IPlanLoader:
        '''
        Returns trajectory plan loader port.

        :return: IPlanLoader instance.
        '''
        return self.storage.loader

    @property
    def storer(self) -> IPlanStorer:
        '''
        Returns trajectory plan storer port.

        :return: IPlanStorer instance.
        '''
        return self.storage.storer

    @property
    def workspace(self) -> IWorkspaceManager:
        '''
        Returns user workspace manager.

        :return: IWorkspaceManager instance.
        '''
        return self.storage.workspace

    @property
    def avoidance_adapter(self) -> IDeadZoneAvoidanceAdapter:
        '''
        Returns dead zone avoidance adapter.

        :return: IDeadZoneAvoidanceAdapter instance.
        '''
        return self.scaralang.dead_zone_avoidance
