# -*- coding: UTF-8 -*-

'''
Module
    canvas_drag_handler.py
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
    Dedicated handler translating interactive dragging events for selection and freehand tools.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.mutation.iplan_point_mutator import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.canvas.handler.canvas_tool_handler import CanvasToolHandler
from scarajectory.infrastructure.gui.canvas.handler.icanvas_waypoint_builder import ICanvasWaypointBuilder
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

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
            :methods:
                | __init__ - Initializes handler with injected collaborators.
                | handle_drag_select - Updates dragged waypoint position during selection drag.
                | handle_drag_freehand - Samples and appends waypoints along freehand motion path.
    '''

    FREEHAND_MIN_DISTANCE_MM: ClassVar[float] = 5.0

    _store: IWaypointStore
    _mutation: IPlanPointMutator
    _state: CanvasInteractionState
    _shape_handler: ICanvasWaypointBuilder

    def __init__(
        self,
        *,
        store: IWaypointStore,
        mutation: IPlanPointMutator,
        state: CanvasInteractionState,
        shape_handler: ICanvasWaypointBuilder,
    ) -> None:
        '''
            Initializes drag handler with injected collaborators.

            :param store: Injected IWaypointStore instance.
            :param mutation: Injected IPlanPointMutator instance.
            :param state: CanvasInteractionState instance.
            :param shape_handler: Injected ICanvasWaypointBuilder instance.
        '''
        self._store: Final[IWaypointStore] = store
        self._mutation: Final[IPlanPointMutator] = mutation
        self._state: Final[CanvasInteractionState] = state
        self._shape_handler: Final[ICanvasWaypointBuilder] = shape_handler

    def handle_drag_select(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint position during select tool drag.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Always False (local redraw handled).
        '''
        if self._state.dragged_node_idx >= 0:
            cur_pt: Waypoint = self._store.waypoints[self._state.dragged_node_idx]
            self._mutation.update_point(
                self._state.dragged_node_idx,
                self._shape_handler.create_relocated_waypoint(cur_pt, wx, wy),
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
        '''
        if self._store.count > 0:
            last: Waypoint = self._store.waypoints[-1]
            if CanvasToolHandler.is_freehand_distance_met(
                last, wx, wy, self.FREEHAND_MIN_DISTANCE_MM
            ):
                new_pt: Waypoint = self._shape_handler.create_waypoint_at(
                    wx, wy, settings
                )
                self._mutation.add_point(new_pt)
        return False
