# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Parameter bundle holding dependencies for ShapePlanCoordinator.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ShapePlanCoordinatorBundle:
    '''
        Immutable container holding dependencies for ShapePlanCoordinator.

        It defines:

            :attributes:
                | store - Active waypoint query and storage service.
                | point_mutator - Active trajectory plan point mutator.
                | bulk_mutator - Active trajectory plan bulk mutator.
                | avoidance_adapter - Dead zone validation and query adapter.
                | planner_adapter - Shape contour avoidance planner adapter.
                | validator - Kinematic reachability validator.
    '''

    store: IWaypointStore
    point_mutator: IPlanPointMutator
    bulk_mutator: IPlanBulkMutator
    avoidance_adapter: IDeadZoneAvoidanceAdapter
    planner_adapter: IShapePlannerAdapter
    validator: ITrajectoryValidator
