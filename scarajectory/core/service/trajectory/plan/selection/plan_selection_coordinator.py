# -*- coding: UTF-8 -*-

'''
Module
    plan_selection_coordinator.py
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
    Defines PlanSelectionCoordinator managing selected index with observer notifications.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_manager import IPlanSelectionManager
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanSelectionCoordinator:
    '''
        Domain coordinator managing waypoint selection index queries and state dispatches.

        It defines:

            :attributes:
                | _store - Injected IWaypointStore collaborator.
                | _selection - Injected IPlanSelectionManager collaborator.
                | _dispatcher - Injected IPlanObserverDispatcher collaborator.
            :methods:
                | __init__ - Initializes coordinator with injected collaborators.
                | selected_index - Returns index of selected point.
                | set_selected_index - Selects a point by index.
    '''

    _store: IWaypointStore
    _selection: IPlanSelectionManager
    _dispatcher: IPlanObserverDispatcher

    def __init__(
        self,
        store: IWaypointStore,
        selection: IPlanSelectionManager,
        dispatcher: IPlanObserverDispatcher,
    ) -> None:
        '''
            Initializes coordinator with injected collaborators.

            :param store: Injected IWaypointStore instance.
            :param selection: Injected IPlanSelectionManager instance.
            :param dispatcher: Injected IPlanObserverDispatcher instance.
            :exceptions: None.
        '''
        self._store: Final[IWaypointStore] = store
        self._selection: Final[IPlanSelectionManager] = selection
        self._dispatcher: Final[IPlanObserverDispatcher] = dispatcher

    @property
    def selected_index(self) -> int:
        '''
            Returns index of selected point.

            :return: Current index or -1 if nothing is selected.
            :exceptions: None.
        '''
        return self._selection.selected_index

    def set_selected_index(self, index: int) -> None:
        '''
            Sets selected point by index and dispatches notification on state transition.

            :param index: Selected index.
            :exceptions: None.
        '''
        if self._selection.set_selected_index(index, self._store.count):
            self._dispatcher.notify_change()
