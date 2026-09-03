# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan.py
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
    Defines TrajectoryPlan managing ordered waypoint sequence, history and observers.
'''

from __future__ import annotations

from typing import Final
from collections.abc import Sequence

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.plan_history import PlanHistory
from scarajectory.core.service.itrajectory_observer import ITrajectoryObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPlan:
    '''
        Core domain model managing waypoints, selection, undo/redo history, and observers.

        It defines:

            :attributes:
                | _waypoints - List of motion waypoints.
                | _observers - Registered observers for UI synchronisation.
                | _selected_index - Index of currently selected waypoint.
                | _history - PlanHistory instance.
            :methods:
                | __init__ - Initializes the trajectory plan.
                | waypoints - Returns read-only view of waypoints.
                | count - Returns total number of waypoints.
                | selected_index - Returns index of currently selected waypoint.
                | add_observer - Registers an observer widget.
                | set_selected_index - Selects a waypoint by index.
                | add_point - Appends a new waypoint to the plan.
                | insert_point - Inserts a waypoint at a specific index.
                | update_point - Replaces waypoint at index with updated parameters.
                | remove_point - Removes waypoint at index.
                | clear - Clears all waypoints in the plan.
                | set_waypoints - Replaces all waypoints with a new list.
                | undo - Reverts last modification.
                | redo - Re-applies previously undone action.
    '''

    _waypoints: list[Waypoint]
    _observers: list[ITrajectoryObserver]
    _selected_index: int
    _history: PlanHistory

    def __init__(self) -> None:
        '''
            Initializes the trajectory plan with empty stacks and observers.

            :exceptions: None.
        '''
        self._waypoints = []
        self._observers = []
        self._selected_index = -1
        self._history: Final[PlanHistory] = PlanHistory()

    @property
    def waypoints(self) -> Sequence[Waypoint]:
        '''
            Returns read-only view of waypoints.

            :return: Tuple of Waypoint instances.
            :exceptions: None.
        '''
        return tuple(self._waypoints)

    @property
    def count(self) -> int:
        '''
            Returns total number of points.

            :return: Number of waypoints.
            :exceptions: None.
        '''
        return len(self._waypoints)

    @property
    def selected_index(self) -> int:
        '''
            Returns index of currently selected waypoint.

            :return: Selected waypoint index or -1.
            :exceptions: None.
        '''
        return self._selected_index

    def add_observer(self, observer: ITrajectoryObserver) -> None:
        '''
            Registers an observer widget.

            :param observer: ITrajectoryObserver instance.
            :exceptions: None.
        '''
        if observer not in self._observers:
            self._observers.append(observer)

    def _notify(self, notify_selection: bool = True) -> None:
        '''
            Notifies all observers of data and selection updates.

            :param notify_selection: Whether to also trigger selection callbacks.
            :exceptions: None.
        '''
        for obs in self._observers:
            obs.on_trajectory_updated()
            if notify_selection:
                obs.on_point_selected(self._selected_index)

    def set_selected_index(self, index: int) -> None:
        '''
            Selects a waypoint by index.

            :param index: Target index (-1 for deselect).
            :exceptions: None.
        '''
        if -1 <= index < len(self._waypoints):
            self._selected_index = index
            for obs in self._observers:
                obs.on_point_selected(index)

    def add_point(self, point: Waypoint) -> None:
        '''
            Appends a new waypoint to the plan.

            :param point: Waypoint instance to add.
            :exceptions: None.
        '''
        self._history.save_state(self._waypoints)
        self._waypoints.append(point)
        self._selected_index = len(self._waypoints) - 1
        self._notify()

    def insert_point(self, index: int, point: Waypoint) -> None:
        '''
            Inserts a waypoint at a specific index.

            :param index: Target insertion position.
            :param point: Waypoint to insert.
            :exceptions: None.
        '''
        self._history.save_state(self._waypoints)
        idx: int = max(0, min(len(self._waypoints), index))
        self._waypoints.insert(idx, point)
        self._selected_index = idx
        self._notify()

    def update_point(self, index: int, new_point: Waypoint) -> bool:
        '''
            Replaces waypoint at index with updated parameters.

            :param index: Target index.
            :param new_point: New waypoint data.
            :return: True if updated, False otherwise.
            :exceptions: None.
        '''
        if 0 <= index < len(self._waypoints):
            self._history.save_state(self._waypoints)
            self._waypoints[index] = new_point
            self._notify(notify_selection=False)
            return True
        return False

    def remove_point(self, index: int) -> bool:
        '''
            Removes waypoint at index.

            :param index: Target index to remove.
            :return: True if removed, False otherwise.
            :exceptions: None.
        '''
        if 0 <= index < len(self._waypoints):
            self._history.save_state(self._waypoints)
            self._waypoints.pop(index)
            if self._selected_index >= len(self._waypoints):
                self._selected_index = len(self._waypoints) - 1
            self._notify()
            return True
        return False

    def clear(self) -> None:
        '''
            Clears all waypoints in the plan.

            :exceptions: None.
        '''
        if self._waypoints:
            self._history.save_state(self._waypoints)
            self._waypoints.clear()
            self._selected_index = -1
            self._notify()

    def set_waypoints(self, waypoints: list[Waypoint]) -> None:
        '''
            Replaces all waypoints with a new list.

            :param waypoints: New list of Waypoint instances.
            :exceptions: None.
        '''
        self._history.save_state(self._waypoints)
        self._waypoints = list(waypoints)
        self._selected_index = 0 if self._waypoints else -1
        self._notify()

    def undo(self) -> bool:
        '''
            Reverts last modification.

            :return: True if undone, False otherwise.
            :exceptions: None.
        '''
        prev = self._history.undo(self._waypoints)
        if prev is not None:
            self._waypoints = prev
            self._selected_index = min(self._selected_index, len(self._waypoints) - 1)
            self._notify()
            return True
        return False

    def redo(self) -> bool:
        '''
            Re-applies previously undone action.

            :return: True if reapplied, False otherwise.
            :exceptions: None.
        '''
        nxt = self._history.redo(self._waypoints)
        if nxt is not None:
            self._waypoints = nxt
            self._selected_index = min(self._selected_index, len(self._waypoints) - 1)
            self._notify()
            return True
        return False
