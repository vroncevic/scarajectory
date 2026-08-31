# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_plan.py
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
    Interface protocol for trajectory domain plan operations and observers.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable
from collections.abc import Sequence

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.service.itrajectory_observer import ITrajectoryObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryPlan(Protocol):
    '''
        Structural interface protocol for trajectory plan domain model.

        It defines:

            :methods:
                | waypoints - Returns sequence of waypoints in plan.
                | count - Returns count of waypoints in plan.
                | selected_index - Returns currently selected waypoint index.
                | set_selected_index - Selects waypoint at index.
                | add_observer - Registers plan mutation observer.
                | add_point - Appends waypoint to plan.
                | insert_point - Inserts waypoint at index.
                | remove_point - Removes waypoint at index.
                | clear - Clears all waypoints.
                | set_waypoints - Replaces all waypoints with a new sequence.
                | update_point - Modifies waypoint at index.
                | undo - Reverts last state change.
                | redo - Restores reverted state change.
    '''

    @property
    def waypoints(self) -> Sequence[Waypoint]:
        '''
            Returns immutable sequence of waypoints in plan.

            :return: Sequence of Waypoint entities.
            :exceptions: None.
        '''

    @property
    def count(self) -> int:
        '''
            Returns count of waypoints in plan.

            :return: Integer count.
            :exceptions: None.
        '''

    @property
    def selected_index(self) -> int:
        '''
            Returns index of currently selected waypoint.

            :return: Selected waypoint index or -1.
            :exceptions: None.
        '''

    def set_selected_index(self, index: int) -> None:
        '''
            Selects a waypoint by index.

            :param index: Target index (-1 for deselect).
            :exceptions: None.
        '''

    def add_observer(self, observer: ITrajectoryObserver) -> None:
        '''
            Registers an observer widget.

            :param observer: ITrajectoryObserver instance.
            :exceptions: None.
        '''

    def add_point(self, point: Waypoint) -> None:
        '''
            Appends waypoint to plan.

            :param point: Waypoint entity.
            :exceptions: None.
        '''

    def insert_point(self, index: int, point: Waypoint) -> None:
        '''
            Inserts waypoint at specified index.

            :param index: Insertion index.
            :param point: Waypoint entity.
            :exceptions: None.
        '''

    def remove_point(self, index: int) -> bool:
        '''
            Removes waypoint at index.

            :param index: Target waypoint index.
            :return: True if removed, False otherwise.
            :exceptions: None.
        '''

    def clear(self) -> None:
        '''
            Clears all waypoints.

            :exceptions: None.
        '''

    def set_waypoints(self, waypoints: Sequence[Waypoint]) -> None:
        '''
            Replaces all waypoints with a new sequence.

            :param waypoints: Sequence of Waypoint instances.
            :exceptions: None.
        '''

    def update_point(self, index: int, new_point: Waypoint) -> bool:
        '''
            Modifies waypoint at index.

            :param index: Target waypoint index.
            :param new_point: Replacement Waypoint entity.
            :return: True if updated, False otherwise.
            :exceptions: None.
        '''

    def undo(self) -> bool:
        '''
            Reverts last state change.

            :return: True if undone, False otherwise.
            :exceptions: None.
        '''

    def redo(self) -> bool:
        '''
            Restores reverted state change.

            :return: True if redone, False otherwise.
            :exceptions: None.
        '''
