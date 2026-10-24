# -*- coding: UTF-8 -*-

'''
Module
    point_mutation.py
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
    Concrete implementation of individual point additions, removals, and updates.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.saver.isaver import IPlanHistorySaver
from scarajectory.core.service.trajectory.plan.observer.idispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.navigator.inavigator import IPlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanPointMutator:
    '''
        Concrete implementation of point operations coordinating store, history, and selection.

        It defines:

            :constants:
                | MIN_INDEX - Minimum valid index for waypoint operations.
            :attributes:
                | _waypoint_store - Injected IWaypointStore collaborator.
                | _plan_history_saver - Injected IPlanHistorySaver collaborator.
                | _plan_selection_navigator - Injected IPlanSelectionNavigator collaborator.
                | _plan_observer_dispatcher - Injected IPlanObserverDispatcher collaborator.
            :methods:
                | __init__ - Initializes the point mutator with injected collaborators.
                | add_point - Appends a waypoint to the plan.
                | insert_point - Inserts a waypoint at a specified index.
                | update_point - Updates a waypoint at an index.
                | remove_point - Removes a waypoint at an index.
    '''

    MIN_INDEX: ClassVar[int] = 0

    _waypoint_store: IWaypointStore
    _plan_history_saver: IPlanHistorySaver
    _plan_selection_navigator: IPlanSelectionNavigator
    _plan_observer_dispatcher: IPlanObserverDispatcher

    def __init__(
        self,
        waypoint_store: IWaypointStore,
        plan_history_saver: IPlanHistorySaver,
        plan_selection_navigator: IPlanSelectionNavigator,
        plan_observer_dispatcher: IPlanObserverDispatcher,
    ) -> None:
        '''
            Initializes the point mutator with injected collaborators.

            :param waypoint_store: Injected IWaypointStore instance.
            :param plan_history_saver: Injected IPlanHistorySaver instance.
            :param plan_selection_navigator: Injected IPlanSelectionNavigator instance.
            :param plan_observer_dispatcher: Injected IPlanObserverDispatcher instance.
            :exceptions: None.
        '''
        self._waypoint_store: Final[IWaypointStore] = waypoint_store
        self._plan_history_saver: Final[IPlanHistorySaver] = plan_history_saver
        self._plan_selection_navigator: Final[IPlanSelectionNavigator] = (
            plan_selection_navigator
        )
        self._plan_observer_dispatcher: Final[IPlanObserverDispatcher] = (
            plan_observer_dispatcher
        )

    def add_point(self, point: TrajectoryWaypoint) -> None:
        '''
            Appends a waypoint to the plan.

            :param point: TrajectoryWaypoint instance to append.
            :exceptions: None.
        '''
        self._plan_history_saver.save_state(list(self._waypoint_store.waypoints))
        self._waypoint_store.add(point)
        self._plan_selection_navigator.select_last(self._waypoint_store.count)
        self._plan_observer_dispatcher.notify_change()

    def insert_point(self, index: int, point: TrajectoryWaypoint) -> None:
        '''
            Inserts a waypoint at a specified index.

            :param index: Target insertion index.
            :param point: TrajectoryWaypoint instance to insert.
            :exceptions: None.
        '''
        self._plan_history_saver.save_state(list(self._waypoint_store.waypoints))
        self._waypoint_store.insert(index, point)
        self._plan_selection_navigator.select_index(index)
        self._plan_observer_dispatcher.notify_change()

    def update_point(self, index: int, point: TrajectoryWaypoint) -> bool:
        '''
            Updates a waypoint at a given index.

            :param index: Target waypoint index.
            :param point: New TrajectoryWaypoint data.
            :return: True if updated, False if index out of bounds.
            :exceptions: None.
        '''
        if self.MIN_INDEX <= index < self._waypoint_store.count:
            self._plan_history_saver.save_state(list(self._waypoint_store.waypoints))
            self._waypoint_store.update(index, point)
            self._plan_selection_navigator.select_index(index)
            self._plan_observer_dispatcher.notify_change()

            return True

        return False

    def remove_point(self, index: int) -> bool:
        '''
            Removes a waypoint at a given index.

            :param index: Index of waypoint to remove.
            :return: True if removed, False if index out of bounds.
            :exceptions: None.
        '''
        if self.MIN_INDEX <= index < self._waypoint_store.count:
            self._plan_history_saver.save_state(list(self._waypoint_store.waypoints))
            self._waypoint_store.remove(index)
            self._plan_selection_navigator.clamp_to_count(self._waypoint_store.count)
            self._plan_observer_dispatcher.notify_change()

            return True

        return False
