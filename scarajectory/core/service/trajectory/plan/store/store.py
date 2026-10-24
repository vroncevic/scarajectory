# -*- coding: UTF-8 -*-

'''
Module
    store.py
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

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.bulk_mutator.ibulk_mutator import IWaypointBulkMutator
from scarajectory.core.service.trajectory.plan.store.mutator.mutator import WaypointMutator
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointStore(WaypointMutator):
    '''
        Concrete implementation of waypoint storage and buffer operations.

        It defines:

            :attributes:
                | _query - Injected collaborator handling read-only queries.
                | _bulk_mutator - Injected collaborator handling bulk operations.
            :methods:
                | __init__ - Initializes waypoint storage with waypoint list and collaborators.
                | waypoints - Returns read-only view of waypoints.
                | count - Returns total number of waypoints.
                | clear - Clears all stored waypoints.
                | replace - Replaces all stored waypoints with a new sequence.
    '''

    _query: IWaypointQuery
    _bulk_mutator: IWaypointBulkMutator

    def __init__(
        self,
        waypoints: list[TrajectoryWaypoint],
        *,
        query: IWaypointQuery,
        bulk_mutator: IWaypointBulkMutator,
    ) -> None:
        '''
            Initializes waypoint storage with waypoint list and collaborators.

            :param waypoints: Reference to shared waypoint list.
            :param query: Injected IWaypointQuery collaborator.
            :param bulk_mutator: Injected IWaypointBulkMutator collaborator.
            :exceptions: None.
        '''
        super().__init__(waypoints)
        self._query: Final[IWaypointQuery] = query
        self._bulk_mutator: Final[IWaypointBulkMutator] = bulk_mutator

    @property
    def waypoints(self) -> Sequence[TrajectoryWaypoint]:
        '''
            Returns read-only view of waypoints.

            :return: Tuple of TrajectoryWaypoint instances.
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

    def clear(self) -> None:
        '''
            Clears all stored waypoints.

            :exceptions: None.
        '''
        self._bulk_mutator.clear()

    def replace(self, waypoints: Sequence[TrajectoryWaypoint]) -> None:
        '''
            Replaces all stored waypoints with a new sequence.

            :param waypoints: Sequence of TrajectoryWaypoint entities.
            :exceptions: None.
        '''
        self._bulk_mutator.replace(waypoints)
