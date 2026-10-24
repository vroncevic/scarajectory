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
    Container bundle holding menu bar collaborator dependencies.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.editor.table.itable import ITable
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


@dataclass(slots=True, frozen=True)
class MenuBundle:
    '''
        Immutable data container holding application menu bar collaborators.

        It defines:

            :attributes:
                | plan - Trajectory plan management pipeline bundle.
                | loader - Plan loader service interface.
                | storer - Plan storer service interface.
                | dsl - SCARA DSL pipeline role services bundle.
                | navigator - Viewport navigation interface.
                | table - Waypoint table interface.
            :properties:
                | store - Waypoint store interface.
                | mutation - Plan bulk mutation interface.
                | history - Trajectory history interface.
    '''

    plan: PlanPipelineBundle
    loader: IPlanLoader
    storer: IPlanStorer
    dsl: DslPipelineBundle
    navigator: ICanvasViewNavigator
    table: ITable

    @property
    def store(self) -> IWaypointStore:
        '''
            Returns waypoint store from plan pipeline.

            :return: IWaypointStore instance.
        '''
        return self.plan.store

    @property
    def mutation(self) -> IPlanBulkMutator:
        '''
            Returns plan bulk mutator from plan pipeline.

            :return: IPlanBulkMutator instance.
        '''
        return self.plan.mutation

    @property
    def history(self) -> ITrajectoryPlanHistory:
        '''
            Returns trajectory plan history from plan pipeline.

            :return: ITrajectoryPlanHistory instance.
        '''
        return self.plan.history
