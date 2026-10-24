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
    Builder assembling trajectory plan management pipeline services.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.history.dependencies import HistoryStackDependencies
from scarajectory.core.service.trajectory.history.factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.history.provides import HistoryStackProvides
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory
from scarajectory.core.service.trajectory.history.stack.istack import IPlanHistoryStack
from scarajectory.core.service.trajectory.plan.history.dependencies import HistoryDependencies
from scarajectory.core.service.trajectory.plan.history.factory import HistoryFactory
from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.history.provides import HistoryProvides
from scarajectory.core.service.trajectory.plan.mutation.dependencies import MutationDependencies
from scarajectory.core.service.trajectory.plan.mutation.factory import MutationFactory
from scarajectory.core.service.trajectory.plan.mutation.provides import MutationProvides
from scarajectory.core.service.trajectory.plan.observer.factory import ObserverFactory
from scarajectory.core.service.trajectory.plan.observer.idispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.observer.provides import ObserverProvides
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.dependencies import SelectionDependencies
from scarajectory.core.service.trajectory.plan.selection.factory import SelectionFactory
from scarajectory.core.service.trajectory.plan.selection.provides import SelectionProvides
from scarajectory.core.service.trajectory.plan.store.dependencies import StoreDependencies
from scarajectory.core.service.trajectory.plan.store.factory import StoreFactory
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.plan.store.provides import StoreProvides
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanPipelineBuilder:
    '''
        Builder assembling trajectory plan management pipeline services.

        It defines:

            :methods:
                | build - Assembles and returns PlanPipelineBundle.
                | get_version - Returns builder version string.
    '''

    @classmethod
    def build(cls) -> PlanPipelineBundle:
        '''
            Assembles store, history, selection, dispatcher and returns bundle.

            :return: Fully assembled PlanPipelineBundle instance.
            :exceptions: None.
        '''
        store_provides: StoreProvides = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        )
        store: IWaypointStore = store_provides.waypoint_store
        observer_provides: ObserverProvides = ObserverFactory.create()
        dispatcher: IPlanObserverDispatcher = (
            observer_provides.plan_observer_dispatcher
        )
        selection_provides: SelectionProvides = SelectionFactory.create(
            SelectionDependencies(
                waypoint_store=store,
                plan_observer_dispatcher=dispatcher,
                initial_index=-1,
            )
        )
        selection: IPlanSelectionCoordinator = (
            selection_provides.plan_selection_coordinator
        )
        stack_storage: IPlanHistoryStack = PlanHistoryStackFactory.create()
        history_storage: HistoryStackProvides = PlanHistoryFactory.create(
            HistoryStackDependencies(stack=stack_storage)
        )
        mutation_provides: MutationProvides = MutationFactory.create(
            MutationDependencies(
                waypoint_store=store,
                plan_history_saver=history_storage.saver,
                plan_selection_navigator=selection_provides.plan_selection_navigator,
                plan_observer_dispatcher=dispatcher,
            )
        )
        history_provides: HistoryProvides = HistoryFactory.create(
            HistoryDependencies(
                waypoint_store=store,
                plan_history=history_storage.history,
                plan_selection_state=selection_provides.plan_selection_state,
                plan_observer_dispatcher=dispatcher,
            )
        )
        history: ITrajectoryPlanHistory = (
            history_provides.trajectory_plan_history
        )

        return PlanPipelineBundle(
            store=store,
            selection=selection,
            point_mutator=mutation_provides.plan_point_mutator,
            bulk_mutator=mutation_provides.plan_bulk_mutator,
            history=history,
            dispatcher=dispatcher,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns builder version string representation.

            :return: Builder version string.
            :exceptions: None.
        '''
        return __version__
