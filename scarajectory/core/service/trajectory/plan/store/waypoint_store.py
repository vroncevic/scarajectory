# -*- coding: UTF-8 -*-

'''
Module
    waypoint_store.py
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
    Concrete implementation of waypoint storage and buffer operations.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.store.iwaypoint_bulk_mutator import IWaypointBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_mutator import IWaypointMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_query import IWaypointQuery

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointStore:
    '''
        Concrete implementation of waypoint storage composing query and mutator collaborators.

        It defines:

            :attributes:
                | _query - Injected collaborator handling read-only queries.
                | _mutator - Injected collaborator handling point CRUD operations.
                | _bulk_mutator - Injected collaborator handling bulk operations.
            :methods:
                | __init__ - Initializes waypoint storage with injected collaborators.
                | waypoints - Returns read-only view of waypoints.
                | count - Returns total number of waypoints.
                | add - Appends a waypoint to storage.
                | insert - Inserts a waypoint at specific index.
                | update - Updates a waypoint at specific index.
                | remove - Removes a waypoint at specific index.
                | clear - Clears all stored waypoints.
                | replace - Replaces all stored waypoints with a new sequence.
    '''

    _query: IWaypointQuery
    _mutator: IWaypointMutator
    _bulk_mutator: IWaypointBulkMutator

    def __init__(
        self,
        query: IWaypointQuery,
        mutator: IWaypointMutator,
        bulk_mutator: IWaypointBulkMutator,
    ) -> None:
        '''
            Initializes waypoint storage with injected collaborators.

            :param query: Injected IWaypointQuery collaborator.
            :param mutator: Injected IWaypointMutator collaborator.
            :param bulk_mutator: Injected IWaypointBulkMutator collaborator.
            :exceptions: None.
        '''
        self._query: Final[IWaypointQuery] = query
        self._mutator: Final[IWaypointMutator] = mutator
        self._bulk_mutator: Final[IWaypointBulkMutator] = bulk_mutator

    @property
    def waypoints(self) -> Sequence[Waypoint]:
        '''
            Returns read-only view of waypoints.

            :return: Tuple of Waypoint instances.
            :exceptions: None.
        '''
        return self._query.waypoints

    @property
    def count(self) -> int:
        '''
            Returns total number of waypoints.

            :return: Number of waypoints.
            :exceptions: None.
        '''
        return self._query.count

    def add(self, point: Waypoint) -> None:
        '''
            Appends a waypoint to storage.

            :param point: Waypoint entity to append.
            :exceptions: None.
        '''
        self._mutator.add(point)

    def insert(self, index: int, point: Waypoint) -> None:
        '''
            Inserts a waypoint at specific index.

            :param index: Target index.
            :param point: Waypoint entity to insert.
            :exceptions: None.
        '''
        self._mutator.insert(index, point)

    def update(self, index: int, point: Waypoint) -> bool:
        '''
            Updates a waypoint at specific index.

            :param index: Target index.
            :param point: Replacement Waypoint entity.
            :return: True if updated, False otherwise.
            :exceptions: None.
        '''
        return self._mutator.update(index, point)

    def remove(self, index: int) -> bool:
        '''
            Removes a waypoint at specific index.

            :param index: Target index.
            :return: True if removed, False otherwise.
            :exceptions: None.
        '''
        return self._mutator.remove(index)

    def clear(self) -> None:
        '''
            Clears all stored waypoints.

            :exceptions: None.
        '''
        self._bulk_mutator.clear()

    def replace(self, waypoints: Sequence[Waypoint]) -> None:
        '''
            Replaces all stored waypoints with a new sequence.

            :param waypoints: Sequence of Waypoint entities.
            :exceptions: None.
        '''
        self._bulk_mutator.replace(waypoints)
