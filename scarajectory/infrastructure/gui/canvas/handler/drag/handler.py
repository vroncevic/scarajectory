# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
    Dedicated handler translating interactive dragging events for selection
    and freehand tools.
'''

from __future__ import annotations

from math import hypot
from typing import ClassVar, Final

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.handler.drag.bundle import DragHandlerBundle
from scarajectory.infrastructure.gui.canvas.handler.shape.ibuilder import ICanvasWaypointBuilder
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasDragHandler:
    '''
        Handles dragging motion for waypoint relocation and freehand path sampling.

        It defines:

            :attributes:
                | FREEHAND_MIN_DISTANCE_MM - Minimum distance threshold in mm for freehand point sampling.
                | _store - Injected waypoint store query collaborator.
                | _mutation - Injected plan point mutator collaborator.
                | _state - Interactive mouse and selection state.
                | _shape_handler - Injected waypoint builder for canvas geometry.
                | _avoidance_adapter - Injected dead zone avoidance and detour adapter.
                | _validator - Injected kinematic reachability validator.
            :methods:
                | __init__ - Initializes handler with injected collaborators bundle.
                | handle_drag_select - Updates dragged waypoint position during selection drag.
                | handle_drag_freehand - Samples and appends waypoints along freehand motion path.
    '''

    FREEHAND_MIN_DISTANCE_MM: ClassVar[float] = 5.0

    _store: IWaypointStore
    _mutation: IPlanPointMutator
    _state: CanvasInteractionState
    _shape_handler: ICanvasWaypointBuilder
    _avoidance_adapter: IDeadZoneAvoidanceAdapter
    _validator: ITrajectoryValidator

    def __init__(self, bundle: DragHandlerBundle) -> None:
        '''
            Initializes drag handler with injected collaborators bundle.

            :param bundle: Injected DragHandlerBundle instance.
            :exceptions: None.
        '''
        self._store: Final[IWaypointStore] = bundle.store
        self._mutation: Final[IPlanPointMutator] = bundle.mutation
        self._state: Final[CanvasInteractionState] = bundle.state
        self._shape_handler: Final[ICanvasWaypointBuilder] = bundle.shape_handler
        self._avoidance_adapter: Final[IDeadZoneAvoidanceAdapter] = (
            bundle.avoidance_adapter
        )
        self._validator: Final[ITrajectoryValidator] = bundle.validator

    def handle_drag_select(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint position during select tool drag.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Always False (local redraw handled).
            :exceptions: None.
        '''
        if self._state.dragged_node_idx >= 0:
            cur_pt: TrajectoryWaypoint = self._store.waypoints[
                self._state.dragged_node_idx
            ]
            new_pt: TrajectoryWaypoint = self._shape_handler.create_relocated_waypoint(
                cur_pt, wx, wy
            )

            if (
                not self._avoidance_adapter.is_point_in_dead_zone(new_pt)
                and self._validator.validate_point(new_pt).is_valid
            ):
                self._mutation.update_point(
                    self._state.dragged_node_idx,
                    new_pt,
                )

        return False

    def handle_drag_freehand(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> bool:
        '''
            Samples and appends waypoints along freehand motion path.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :return: Always False (local redraw handled).
            :exceptions: None.
        '''
        if self._store.count > 0:
            last: TrajectoryWaypoint = self._store.waypoints[-1]

            if hypot(wx - last.x, wy - last.y) >= self.FREEHAND_MIN_DISTANCE_MM:
                new_pt: TrajectoryWaypoint = self._shape_handler.create_waypoint_at(
                    wx, wy, settings
                )

                if (
                    settings.enforce_deadzone
                    and not self._validator.validate_point(new_pt).is_valid
                ):
                    return False

                if self._avoidance_adapter.is_point_in_dead_zone(new_pt):
                    return False

                if self._avoidance_adapter.crosses_dead_zone(last, new_pt):
                    detour: list[TrajectoryWaypoint] = (
                        self._avoidance_adapter.plan_detour(last, new_pt)
                    )

                    for pt in detour:
                        if (
                            settings.enforce_deadzone
                            and not self._validator.validate_point(pt).is_valid
                        ):
                            return False
                        self._mutation.add_point(pt)
                else:
                    self._mutation.add_point(new_pt)

        return False
