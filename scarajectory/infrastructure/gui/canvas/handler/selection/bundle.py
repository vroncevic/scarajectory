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
    Parameter bundle holding collaborators for selection mouse handler.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class SelectionHandlerBundle:
    '''
        Immutable container holding dependencies for CanvasSelectionMouseHandler.

        It defines:

            :attributes:
                | store - Active waypoint query and storage service.
                | selection - Active waypoint selection coordinator.
                | mutation - Plan point mutator service.
                | vp - Viewport coordinate transformation engine.
                | state - Interactive mouse and selection state.
                | validator - Kinematic reachability validator.
    '''

    store: IWaypointStore
    selection: IPlanSelectionCoordinator
    mutation: IPlanPointMutator
    vp: ViewportTransform
    state: CanvasInteractionState
    validator: ITrajectoryValidator
