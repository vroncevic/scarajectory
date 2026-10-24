# -*- coding: UTF-8 -*-

'''
Module
    history.py
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
    Defines TrajectoryPlanHistory coordinating undo and redo transactions on trajectory plan.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.history.navigator.inavigator import IPlanHistoryNavigator
from scarajectory.core.service.trajectory.plan.observer.idispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.state.istate import IPlanSelectionState
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPlanHistory:
    '''
        Domain service coordinating plan undo and redo transactions across store, selection, and observers.

        It defines:

            :attributes:
                | _waypoint_store - Injected IWaypointStore collaborator.
                | _plan_history - Injected IPlanHistoryNavigator collaborator.
                | _plan_selection_state - Injected IPlanSelectionState collaborator.
                | _plan_observer_dispatcher - Injected IPlanObserverDispatcher collaborator.
            :methods:
                | __init__ - Initializes the history coordinator with injected collaborators.
                | undo - Reverts last state change on the plan.
                | redo - Restores reverted state change on the plan.
    '''

    _waypoint_store: IWaypointStore
    _plan_history: IPlanHistoryNavigator
    _plan_selection_state: IPlanSelectionState
    _plan_observer_dispatcher: IPlanObserverDispatcher

    def __init__(
        self,
        waypoint_store: IWaypointStore,
        plan_history: IPlanHistoryNavigator,
        plan_selection_state: IPlanSelectionState,
        plan_observer_dispatcher: IPlanObserverDispatcher,
    ) -> None:
        '''
            Initializes the history coordinator with injected collaborators.

            :param waypoint_store: Injected IWaypointStore instance.
            :param plan_history: Injected IPlanHistoryNavigator instance.
            :param plan_selection_state: Injected IPlanSelectionState instance.
            :param plan_observer_dispatcher: Injected IPlanObserverDispatcher instance.
            :exceptions: None.
        '''
        self._waypoint_store: Final[IWaypointStore] = waypoint_store
        self._plan_history: Final[IPlanHistoryNavigator] = plan_history
        self._plan_selection_state: Final[IPlanSelectionState] = (
            plan_selection_state
        )
        self._plan_observer_dispatcher: Final[IPlanObserverDispatcher] = (
            plan_observer_dispatcher
        )

    def undo(self) -> bool:
        '''
            Reverts last modification.

            :return: True if undone, False otherwise.
            :exceptions: None.
        '''
        if not self._plan_history.can_undo():
            return False

        prev = self._plan_history.undo(list(self._waypoint_store.waypoints))
        self._waypoint_store.replace(prev)
        self._plan_selection_state.clamp_to_count(self._waypoint_store.count)
        self._plan_observer_dispatcher.notify_change()

        return True

    def redo(self) -> bool:
        '''
            Re-applies previously undone action.

            :return: True if reapplied, False otherwise.
            :exceptions: None.
        '''
        if not self._plan_history.can_redo():
            return False

        nxt = self._plan_history.redo(list(self._waypoint_store.waypoints))
        self._waypoint_store.replace(nxt)
        self._plan_selection_state.clamp_to_count(self._waypoint_store.count)
        self._plan_observer_dispatcher.notify_change()

        return True
