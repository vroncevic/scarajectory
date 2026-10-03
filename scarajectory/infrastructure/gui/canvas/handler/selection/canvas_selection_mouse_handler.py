# -*- coding: UTF-8 -*-

'''
Module
    canvas_selection_mouse_handler.py
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
    Dedicated handler translating mouse interaction into waypoint selection
    and dragging.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.mutation.iplan_point_mutator import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.canvas.handler.canvas_tool_handler import CanvasToolHandler
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasSelectionMouseHandler:
    '''
        Handles hit detection, selection toggle, and waypoint drag updates.

        It defines:

            :attributes:
                | SELECT_HIT_RADIUS_PX - Hit detection pixel radius.
                | _store - Injected waypoint store query collaborator.
                | _selection - Injected selection coordinator collaborator.
                | _mutation - Injected plan mutation service collaborator.
                | _vp - Viewport transformation matrix.
                | _state - Interactive mouse pan, drag, and selection state.
            :methods:
                | __init__ - Initializes handler with injected collaborators.
                | handle_select_down - Processes mouse down for hit detection.
                | handle_select_drag - Updates dragged point during motion.
                | find_hit_index - Computes nearest index within hit radius.
                | clear_selection - Clears active selection and dragged index.
    '''

    SELECT_HIT_RADIUS_PX: ClassVar[float] = 12.0

    _store: IWaypointStore
    _selection: IPlanSelectionCoordinator
    _mutation: IPlanPointMutator
    _vp: ViewportTransform
    _state: CanvasInteractionState

    def __init__(
        self,
        store: IWaypointStore,
        selection: IPlanSelectionCoordinator,
        mutation: IPlanPointMutator,
        vp: ViewportTransform,
        state: CanvasInteractionState,
    ) -> None:
        '''
            Initializes selection handler with injected collaborators.

            :param store: Injected IWaypointStore instance.
            :param selection: Injected IPlanSelectionCoordinator instance.
            :param mutation: Injected IPlanPointMutator instance.
            :param vp: ViewportTransform instance.
            :param state: CanvasInteractionState instance.
            :exceptions: None.
        '''
        self._store: Final[IWaypointStore] = store
        self._selection: Final[IPlanSelectionCoordinator] = selection
        self._mutation: Final[IPlanPointMutator] = mutation
        self._vp: Final[ViewportTransform] = vp
        self._state: Final[CanvasInteractionState] = state

    def handle_select_down(self, wx: float, wy: float) -> int:
        '''
            Processes mouse down for selection hit detection.

            :param wx: World X coordinate in mm.
            :param wy: World Y coordinate in mm.
            :return: Hit waypoint index, or -1 if no waypoint hit.
            :exceptions: None.
        '''
        hit_idx: int = self.find_hit_index(wx, wy)

        if hit_idx >= 0:
            self._state.dragged_node_idx = hit_idx
            self._selection.set_selected_index(hit_idx)
        else:
            self._state.dragged_node_idx = -1
            self._selection.set_selected_index(-1)
        return hit_idx

    def handle_select_drag(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint during selection motion.

            :param wx: World X coordinate in mm.
            :param wy: World Y coordinate in mm.
            :return: True if canvas redraw requested, False otherwise.
            :exceptions: None.
        '''
        if self._state.dragged_node_idx >= 0:
            cur_pt: Waypoint = self._store.waypoints[
                self._state.dragged_node_idx
            ]
            self._mutation.update_point(
                self._state.dragged_node_idx,
                Waypoint(
                    x=wx,
                    y=wy,
                    z=cur_pt.z,
                    phi=cur_pt.phi,
                    speed=cur_pt.speed,
                    name=cur_pt.name,
                    command=cur_pt.command,
                ),
            )

        return False

    def find_hit_index(self, wx: float, wy: float) -> int:
        '''
            Computes nearest waypoint index within hit radius.

            :param wx: World X coordinate in mm.
            :param wy: World Y coordinate in mm.
            :return: Hit waypoint index, or -1 if none found.
            :exceptions: None.
        '''
        hit_r_world: float = self.SELECT_HIT_RADIUS_PX / self._vp.scale

        return CanvasToolHandler.find_hit_index(
            self._store.waypoints, wx, wy, hit_r_world
        )

    def clear_selection(self) -> None:
        '''
            Clears active selection and dragged index.

            :exceptions: None.
        '''
        self._state.dragged_node_idx = -1
        self._selection.set_selected_index(-1)
