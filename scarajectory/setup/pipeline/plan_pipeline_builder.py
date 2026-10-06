# -*- coding: UTF-8 -*-

'''
Module
    plan_pipeline_builder.py
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

from scarajectory.core.service.trajectory.history.plan_history import PlanHistory
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.plan.history.plan_history_service import PlanHistoryService
from scarajectory.core.service.trajectory.plan.history.plan_history_service_factory import PlanHistoryServiceFactory
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service import PlanMutationService
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service_factory import PlanMutationServiceFactory
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher import PlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher_factory import PlanObserverDispatcherFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_coordinator import PlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.plan_selection_coordinator_factory import PlanSelectionCoordinatorFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager import PlanSelectionManager
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager_factory import PlanSelectionManagerFactory
from scarajectory.core.service.trajectory.plan.store.waypoint_store import WaypointStore
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle

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
    '''

    @classmethod
    def build(cls) -> PlanPipelineBundle:
        '''
            Assembles store, history, selection, dispatcher and returns bundle.

            :return: Fully assembled PlanPipelineBundle instance.
            :exceptions: None.
        '''
        store: WaypointStore = WaypointStoreFactory.create()
        history_storage: PlanHistory = PlanHistoryFactory.create()
        selection_mgr: PlanSelectionManager = PlanSelectionManagerFactory.create()
        dispatcher: PlanObserverDispatcher = PlanObserverDispatcherFactory.create()
        selection: PlanSelectionCoordinator = (
            PlanSelectionCoordinatorFactory.create(
                store=store,
                selection=selection_mgr,
                dispatcher=dispatcher,
            )
        )
        mutation: PlanMutationService = PlanMutationServiceFactory.create(
            store=store,
            history=history_storage,
            selection=selection_mgr,
            dispatcher=dispatcher,
        )
        history: PlanHistoryService = PlanHistoryServiceFactory.create(
            store=store,
            history=history_storage,
            selection=selection_mgr,
            dispatcher=dispatcher,
        )

        return PlanPipelineBundle(
            store=store,
            selection=selection,
            mutation=mutation,
            history=history,
            dispatcher=dispatcher,
        )
