# -*- coding: UTF-8 -*-

'''
Module
    iwaypoint_store.py
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
    Interface protocol for trajectory waypoint storage and buffer operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.service.trajectory.plan.store.iwaypoint_bulk_mutator import IWaypointBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_mutator import IWaypointMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_query import IWaypointQuery

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWaypointStore(IWaypointQuery, IWaypointMutator, IWaypointBulkMutator, Protocol):
    '''
        Composite structural protocol for trajectory waypoint storage and buffer operations.
    '''
