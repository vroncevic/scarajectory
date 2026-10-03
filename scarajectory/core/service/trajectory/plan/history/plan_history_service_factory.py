# -*- coding: UTF-8 -*-

'''
Module
    plan_history_service_factory.py
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
    Factory module for instantiating PlanHistoryService instances.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.history.iplan_history import IPlanHistory
from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_manager import IPlanSelectionManager
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.core.service.trajectory.plan.history.plan_history_service import PlanHistoryService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanHistoryServiceFactory:
    '''
        Factory responsible for creating PlanHistoryService instances.

        It defines:

            :methods:
                | create - Instantiates a PlanHistoryService with injected collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        store: IWaypointStore,
        history: IPlanHistory,
        selection: IPlanSelectionManager,
        dispatcher: IPlanObserverDispatcher,
    ) -> PlanHistoryService:
        '''
            Instantiates a PlanHistoryService with injected collaborators.

            :param store: Injected IWaypointStore instance.
            :param history: Injected IPlanHistory instance.
            :param selection: Injected IPlanSelectionManager instance.
            :param dispatcher: Injected IPlanObserverDispatcher instance.
            :return: Fully initialized PlanHistoryService instance.
            :exceptions: None.
        '''
        return PlanHistoryService(
            store=store,
            history=history,
            selection=selection,
            dispatcher=dispatcher,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: String version.
            :exceptions: None.
        '''
        return __version__
