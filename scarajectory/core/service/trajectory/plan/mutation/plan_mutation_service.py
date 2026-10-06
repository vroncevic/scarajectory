# -*- coding: UTF-8 -*-

'''
Module
    plan_mutation_service.py
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
    Domain service coordinating waypoint additions, removals, updates, and resets.
'''

from __future__ import annotations

from typing import Final
from collections.abc import Sequence

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.history.iplan_history_saver import IPlanHistorySaver
from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_manager import IPlanSelectionManager
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanMutationService:
    '''
        Domain service coordinating waypoint additions, removals, updates, and resets.

        It defines:

            :attributes:
                | _store - Injected IWaypointStore collaborator.
                | _history - Injected IPlanHistorySaver collaborator.
                | _selection - Injected IPlanSelectionManager collaborator.
                | _dispatcher - Injected IPlanObserverDispatcher collaborator.
            :methods:
                | __init__ - Initializes the mutation service with injected collaborators.
                | add_point - Appends a waypoint to the plan.
                | insert_point - Inserts a waypoint at a specified index.
                | update_point - Updates a waypoint at an index.
                | remove_point - Removes a waypoint at an index.
                | clear - Clears all waypoints from the plan.
                | set_waypoints - Replaces all waypoints with a new sequence.
    '''

    _store: IWaypointStore
    _history: IPlanHistorySaver
    _selection: IPlanSelectionManager
    _dispatcher: IPlanObserverDispatcher

    def __init__(
        self,
        store: IWaypointStore,
        history: IPlanHistorySaver,
        selection: IPlanSelectionManager,
        dispatcher: IPlanObserverDispatcher,
    ) -> None:
        '''
            Initializes the mutation service with injected collaborators.

            :param store: Injected IWaypointStore instance.
            :param history: Injected IPlanHistorySaver instance.
            :param selection: Injected IPlanSelectionManager instance.
            :param dispatcher: Injected IPlanObserverDispatcher instance.
            :exceptions: None.
        '''
        self._store: Final[IWaypointStore] = store
        self._history: Final[IPlanHistorySaver] = history
        self._selection: Final[IPlanSelectionManager] = selection
        self._dispatcher: Final[IPlanObserverDispatcher] = dispatcher

    def add_point(self, point: Waypoint) -> None:
        '''
            Appends a waypoint to the plan.

            :param point: Waypoint instance to append.
            :exceptions: None.
        '''
        self._history.save_state(list(self._store.waypoints))
        self._store.add(point)
        self._selection.select_last(self._store.count)
        self._dispatcher.notify_change()

    def insert_point(self, index: int, point: Waypoint) -> None:
        '''
            Inserts a waypoint at a specified index.

            :param index: Target insertion index.
            :param point: Waypoint instance to insert.
            :exceptions: None.
        '''
        self._history.save_state(list(self._store.waypoints))
        self._store.insert(index, point)
        self._selection.select_index(index)
        self._dispatcher.notify_change()

    def update_point(self, index: int, point: Waypoint) -> bool:
        '''
            Updates a waypoint at a given index.

            :param index: Target waypoint index.
            :param point: New Waypoint data.
            :return: True if updated, False if index out of bounds.
            :exceptions: None.
        '''
        if 0 <= index < self._store.count:
            self._history.save_state(list(self._store.waypoints))
            self._store.update(index, point)
            self._selection.select_index(index)
            self._dispatcher.notify_change()

            return True

        return False

    def remove_point(self, index: int) -> bool:
        '''
            Removes a waypoint at a given index.

            :param index: Index of waypoint to remove.
            :return: True if removed, False if index out of bounds.
            :exceptions: None.
        '''
        if 0 <= index < self._store.count:
            self._history.save_state(list(self._store.waypoints))
            self._store.remove(index)
            self._selection.clamp_to_count(self._store.count)
            self._dispatcher.notify_change()

            return True

        return False

    def clear(self) -> None:
        '''
            Clears all waypoints from the plan.

            :exceptions: None.
        '''
        if self._store.count > 0:
            self._history.save_state(list(self._store.waypoints))
            self._store.clear()
            self._selection.reset()
            self._dispatcher.notify_change()

    def set_waypoints(self, points: Sequence[Waypoint]) -> None:
        '''
            Replaces all waypoints with a new sequence.

            :param points: Sequence of Waypoint instances.
            :exceptions: None.
        '''
        self._history.save_state(list(self._store.waypoints))
        self._store.replace(list(points))
        self._selection.select_first_or_none(self._store.count)
        self._dispatcher.notify_change()
