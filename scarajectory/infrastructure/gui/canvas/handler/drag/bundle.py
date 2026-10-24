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
    Parameter bundle holding dependencies for CanvasDragHandler.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.handler.shape.ibuilder import ICanvasWaypointBuilder
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class DragHandlerBundle:
    '''
        Immutable container holding dependencies for CanvasDragHandler.

        It defines:

            :attributes:
                | store - Active waypoint query and storage service.
                | mutation - Plan point mutator service.
                | state - Interactive mouse pan, drag and selection state.
                | shape_handler - Injected waypoint builder for canvas geometry.
                | avoidance_adapter - Dead zone avoidance and bypass adapter.
                | validator - Kinematic reachability validator.
    '''

    store: IWaypointStore
    mutation: IPlanPointMutator
    state: CanvasInteractionState
    shape_handler: ICanvasWaypointBuilder
    avoidance_adapter: IDeadZoneAvoidanceAdapter
    validator: ITrajectoryValidator
