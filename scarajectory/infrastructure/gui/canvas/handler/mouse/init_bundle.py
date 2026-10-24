# -*- coding: UTF-8 -*-

'''
Module
    init_bundle.py
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
    Parameter bundle for initial construction of CanvasMouseHandler.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.mutation.provides import MutationProvides
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.adapter_bundle import CanvasAdapterBundle
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MouseHandlerInitBundle:
    '''
        Immutable container holding dependencies required to build CanvasMouseHandler.

        It defines:

            :attributes:
                | store - Active waypoint query and storage service.
                | selection - Plan waypoint selection coordinator.
                | mutations - Plan mutation provides container.
                | vp - Viewport transformation matrix.
                | state - Interactive mouse pan, drag and selection state.
                | adapters - Injected external adapters bundle.
                | validator - Manipulator kinematic reachability validator.
            :methods:
                | mutation - Exposes plan point mutator service.
                | bulk_mutator - Exposes plan bulk mutator service.
                | avoidance_adapter - Exposes dead zone avoidance adapter.
                | planner_adapter - Exposes shape planner adapter.
    '''

    store: IWaypointStore
    selection: IPlanSelectionCoordinator
    mutations: MutationProvides
    vp: ViewportTransform
    state: CanvasInteractionState
    adapters: CanvasAdapterBundle
    validator: ITrajectoryValidator

    @property
    def mutation(self) -> IPlanPointMutator:
        '''
            Exposes plan point mutator service.

            :return: IPlanPointMutator instance.
            :exceptions: None.
        '''
        return self.mutations.plan_point_mutator

    @property
    def bulk_mutator(self) -> IPlanBulkMutator:
        '''
            Exposes plan bulk mutator service.

            :return: IPlanBulkMutator instance.
            :exceptions: None.
        '''
        return self.mutations.plan_bulk_mutator

    @property
    def avoidance_adapter(self) -> IDeadZoneAvoidanceAdapter:
        '''
            Exposes dead zone avoidance adapter.

            :return: IDeadZoneAvoidanceAdapter instance.
            :exceptions: None.
        '''
        return self.adapters.avoidance

    @property
    def planner_adapter(self) -> IShapePlannerAdapter:
        '''
            Exposes shape planner adapter.

            :return: IShapePlannerAdapter instance.
            :exceptions: None.
        '''
        return self.adapters.planner
