# -*- coding: UTF-8 -*-

'''
Module
    plan_history_service.py
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
    Defines PlanHistoryService coordinating undo and redo transactions on trajectory plan.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.history.iplan_history import IPlanHistory
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


class PlanHistoryService:
    '''
        Domain service coordinating plan undo and redo transactions across store, selection, and observers.

        It defines:

            :attributes:
                | _store - Injected IWaypointStore collaborator.
                | _history - Injected IPlanHistory collaborator.
                | _selection - Injected IPlanSelectionManager collaborator.
                | _dispatcher - Injected IPlanObserverDispatcher collaborator.
            :methods:
                | __init__ - Initializes the history service with injected collaborators.
                | undo - Reverts last state change on the plan.
                | redo - Restores reverted state change on the plan.
    '''

    _store: IWaypointStore
    _history: IPlanHistory
    _selection: IPlanSelectionManager
    _dispatcher: IPlanObserverDispatcher

    def __init__(
        self,
        store: IWaypointStore,
        history: IPlanHistory,
        selection: IPlanSelectionManager,
        dispatcher: IPlanObserverDispatcher,
    ) -> None:
        '''
            Initializes the history service with injected collaborators.

            :param store: Injected IWaypointStore instance.
            :param history: Injected IPlanHistory instance.
            :param selection: Injected IPlanSelectionManager instance.
            :param dispatcher: Injected IPlanObserverDispatcher instance.
            :exceptions: None.
        '''
        self._store: Final[IWaypointStore] = store
        self._history: Final[IPlanHistory] = history
        self._selection: Final[IPlanSelectionManager] = selection
        self._dispatcher: Final[IPlanObserverDispatcher] = dispatcher

    def undo(self) -> bool:
        '''
            Reverts last modification.

            :return: True if undone, False otherwise.
            :exceptions: None.
        '''
        if not self._history.can_undo():
            return False

        prev = self._history.undo(list(self._store.waypoints))
        self._store.replace(prev)
        self._selection.clamp_to_count(self._store.count)
        self._dispatcher.notify_change()
        return True

    def redo(self) -> bool:
        '''
            Re-applies previously undone action.

            :return: True if reapplied, False otherwise.
            :exceptions: None.
        '''
        if not self._history.can_redo():
            return False

        nxt = self._history.redo(list(self._store.waypoints))
        self._store.replace(nxt)
        self._selection.clamp_to_count(self._store.count)
        self._dispatcher.notify_change()

        return True
