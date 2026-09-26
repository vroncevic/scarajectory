# -*- coding: UTF-8 -*-

'''
Module
    canvas_mouse_handler.py
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
    Translates mouse interaction and drag events into CAD vector canvas operations.
'''

from __future__ import annotations

from math import hypot
from tkinter import Event
from typing import ClassVar, Final

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.discretization.iwaypoint_factory import IWaypointFactory
from scarajectory.core.service.trajectory.discretization.ishape_discretizer import IShapeDiscretizer
from scarajectory.core.service.trajectory.discretization.waypoint_factory import WaypointFactory
from scarajectory.core.service.trajectory.discretization.shape_discretizer import ShapeDiscretizer
from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform
from scarajectory.infrastructure.gui.canvas.canvas_tool_handler import CanvasToolHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasMouseHandler:
    '''
        Handles mouse press, drag, release, and wheel interaction for CAD vector drawing.

        It defines:

            :attributes:
                | SELECT_HIT_RADIUS_PX - Hit detection pixel radius for selecting waypoints.
                | FREEHAND_MIN_DISTANCE_MM - Minimum distance threshold in mm for freehand point sampling.
                | CIRCLE_MIN_RADIUS_MM - Minimum radius threshold in mm for inserting circle shapes.
                | CIRCLE_DEFAULT_STEPS - Number of waypoint segments used for circle discretization.
                | _plan - Active trajectory plan interface.
                | _vp - Viewport transformation matrix.
                | _state - Interactive mouse pan, drag, and selection state.
            :methods:
                | __init__ - Initializes handler with injected plan, viewport, and interaction state.
                | create_waypoint_at - Builds a Waypoint via WaypointFactory at given world coordinates.
                | handle_mouse_down - Processes mouse button press for tool interaction or panning.
                | handle_mouse_drag - Processes mouse motion for active tool or viewport panning.
                | handle_drag_select - Updates dragged waypoint position during select tool drag.
                | handle_drag_freehand - Samples and appends waypoints along freehand motion path.
                | handle_mouse_up - Processes mouse button release and commits shape insertions.
                | commit_point - Commits a single waypoint to the trajectory plan.
                | commit_line - Discretizes and commits straight line segment to plan.
                | commit_circle - Discretizes and commits circular trajectory to plan.
                | commit_rectangle - Discretizes and commits rectangular perimeter to plan.
                | format_cursor_status - Computes world coordinates and zoom percentage for cursor status.
    '''

    SELECT_HIT_RADIUS_PX: ClassVar[float] = 12.0
    FREEHAND_MIN_DISTANCE_MM: ClassVar[float] = 5.0
    CIRCLE_MIN_RADIUS_MM: ClassVar[float] = 5.0
    CIRCLE_DEFAULT_STEPS: ClassVar[int] = 16

    _plan: ITrajectoryPlan
    _vp: ViewportTransform
    _state: CanvasInteractionState

    def __init__(
        self,
        plan: ITrajectoryPlan,
        vp: ViewportTransform,
        state: CanvasInteractionState,
        waypoint_factory: IWaypointFactory | None = None,
        discretizer: IShapeDiscretizer | None = None,
    ) -> None:
        '''
            Initializes handler with injected plan, viewport, and interaction state.

            :param plan: Active ITrajectoryPlan instance.
            :param vp: ViewportTransform instance.
            :param state: CanvasInteractionState instance.
            :exceptions: None.
        '''
        self._plan: Final[ITrajectoryPlan] = plan
        self._vp: Final[ViewportTransform] = vp
        self._state: Final[CanvasInteractionState] = state
        self._waypoint_factory: Final[IWaypointFactory] = (
            waypoint_factory if waypoint_factory is not None else WaypointFactory
        )
        self._discretizer: Final[IShapeDiscretizer] = (
            discretizer
            if discretizer is not None
            else ShapeDiscretizer(waypoint_factory=self._waypoint_factory)
        )

    def create_waypoint_at(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> Waypoint:
        '''
            Builds a Waypoint via WaypointFactory at given world coordinates.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :return: New Waypoint instance.
            :exceptions: None.
        '''
        return self._waypoint_factory.create(
            x=wx,
            y=wy,
            z=settings.default_z,
            phi=0.0,
            speed=settings.default_speed,
            name='',
            command='',
        )

    def handle_mouse_down(
        self,
        event: Event,
        width: int,
        height: int,
        tool_mode: CanvasToolMode,
        settings: CanvasSettings,
    ) -> None:
        '''
            Processes mouse button press for tool interaction or viewport panning.

            :param event: Tkinter mouse Event.
            :param width: Current canvas pixel width.
            :param height: Current canvas pixel height.
            :param tool_mode: Active CanvasToolMode.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        if getattr(event, 'num', 1) in (2, 3):
            self._state.pan_x = event.x
            self._state.pan_y = event.y
            self._state.is_panning = True
            return

        wx, wy = self._vp.screen_to_world(event.x, event.y, width, height)
        self._state.drag_start_world = (wx, wy)
        self._state.drag_current_world = (wx, wy)
        self._state.dragged_node_idx = -1

        hit_r_world: float = self.SELECT_HIT_RADIUS_PX / self._vp.scale
        hit_idx: int = CanvasToolHandler.find_hit_index(self._plan.waypoints, wx, wy, hit_r_world)

        if tool_mode == CanvasToolMode.SELECT:
            if hit_idx >= 0:
                self._state.dragged_node_idx = hit_idx
                self._plan.set_selected_index(hit_idx)
            else:
                self._plan.set_selected_index(-1)
        elif tool_mode == CanvasToolMode.FREEHAND:
            self._plan.add_point(self.create_waypoint_at(wx, wy, settings))

    def handle_drag_select(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint position during select tool drag.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Always False (local redraw handled).
            :exceptions: None.
        '''
        if self._state.dragged_node_idx >= 0:
            cur_pt = self._plan.waypoints[self._state.dragged_node_idx]
            self._plan.update_point(
                self._state.dragged_node_idx,
                self._waypoint_factory.create(
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
        if self._plan.count > 0:
            last = self._plan.waypoints[-1]
            if CanvasToolHandler.is_freehand_distance_met(
                last, wx, wy, self.FREEHAND_MIN_DISTANCE_MM
            ):
                self._plan.add_point(self.create_waypoint_at(wx, wy, settings))
        return False

    def handle_mouse_drag(
        self,
        event: Event,
        width: int,
        height: int,
        tool_mode: CanvasToolMode,
        settings: CanvasSettings,
    ) -> bool:
        '''
            Processes mouse motion for active tool or viewport panning.

            :param event: Tkinter mouse Event.
            :param width: Current canvas pixel width.
            :param height: Current canvas pixel height.
            :param tool_mode: Active CanvasToolMode.
            :param settings: Active CanvasSettings.
            :return: True if canvas redraw is needed, False otherwise.
            :exceptions: None.
        '''
        if self._state.is_panning:
            self._vp.pan_x += event.x - self._state.pan_x
            self._vp.pan_y += event.y - self._state.pan_y
            self._state.pan_x = event.x
            self._state.pan_y = event.y
            return True

        wx, wy = self._vp.screen_to_world(event.x, event.y, width, height)
        self._state.drag_current_world = (wx, wy)

        if tool_mode == CanvasToolMode.SELECT:
            return self.handle_drag_select(wx, wy)
        elif tool_mode == CanvasToolMode.FREEHAND:
            return self.handle_drag_freehand(wx, wy, settings)
        elif tool_mode in (CanvasToolMode.CIRCLE, CanvasToolMode.RECTANGLE, CanvasToolMode.LINE):
            return True

        return False

    def commit_point(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Commits single point to the trajectory plan.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        self._plan.add_point(self.create_waypoint_at(wx, wy, settings))

    def commit_line(
        self,
        x0: float,
        y0: float,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits straight line segment to plan.

            :param x0: Starting world X coordinate.
            :param y0: Starting world Y coordinate.
            :param wx: Ending world X coordinate.
            :param wy: Ending world Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        if hypot(wx - x0, wy - y0) > 1.0:
            line_pts = self._discretizer.discretize_line((x0, y0), (wx, wy), z=settings.default_z, speed=settings.default_speed)
            self._plan.set_waypoints(list(self._plan.waypoints) + line_pts)

    def commit_circle(
        self,
        x0: float,
        y0: float,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits circular trajectory to plan.

            :param x0: Center world X coordinate.
            :param y0: Center world Y coordinate.
            :param wx: Boundary world X coordinate.
            :param wy: Boundary world Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        radius: float = hypot(wx - x0, wy - y0)
        if radius >= self.CIRCLE_MIN_RADIUS_MM:
            circle_pts = self._discretizer.discretize_circle(
                (x0, y0), radius, self.CIRCLE_DEFAULT_STEPS, z=settings.default_z, speed=settings.default_speed
            )
            self._plan.set_waypoints(list(self._plan.waypoints) + circle_pts)

    def commit_rectangle(
        self,
        x0: float,
        y0: float,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> None:
        '''
            Discretizes and commits rectangular perimeter to plan.

            :param x0: Starting corner world X coordinate.
            :param y0: Starting corner world Y coordinate.
            :param wx: Opposite corner world X coordinate.
            :param wy: Opposite corner world Y coordinate.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        if abs(wx - x0) > 2.0 and abs(wy - y0) > 2.0:
            rect_pts = self._discretizer.discretize_rectangle((x0, y0), (wx, wy), z=settings.default_z, speed=settings.default_speed)
            self._plan.set_waypoints(list(self._plan.waypoints) + rect_pts)

    def handle_mouse_up(
        self,
        event: Event,
        width: int,
        height: int,
        tool_mode: CanvasToolMode,
        settings: CanvasSettings,
    ) -> None:
        '''
            Processes mouse button release and commits shape insertions to plan.

            :param event: Tkinter mouse Event.
            :param width: Current canvas pixel width.
            :param height: Current canvas pixel height.
            :param tool_mode: Active CanvasToolMode.
            :param settings: Active CanvasSettings.
            :exceptions: None.
        '''
        if self._state.is_panning:
            self._state.is_panning = False
            return

        wx, wy = self._vp.screen_to_world(event.x, event.y, width, height)

        if self._state.drag_start_world:
            x0, y0 = self._state.drag_start_world
            if tool_mode == CanvasToolMode.POINT:
                self.commit_point(wx, wy, settings)
            elif tool_mode == CanvasToolMode.LINE:
                self.commit_line(x0, y0, wx, wy, settings)
            elif tool_mode == CanvasToolMode.CIRCLE:
                self.commit_circle(x0, y0, wx, wy, settings)
            elif tool_mode == CanvasToolMode.RECTANGLE:
                self.commit_rectangle(x0, y0, wx, wy, settings)

        self._state.reset_drag()

    def format_cursor_status(self, event: Event, width: int, height: int) -> str:
        '''
            Computes world coordinates and zoom percentage for cursor status bar display.

            :param event: Tkinter mouse Event.
            :param width: Current canvas pixel width.
            :param height: Current canvas pixel height.
            :return: Formatted status readout string.
            :exceptions: None.
        '''
        wx, wy = self._vp.screen_to_world(event.x, event.y, width, height)
        r: float = hypot(wx, wy)
        zoom_pct: int = int((self._vp.scale / ViewportTransform.DEFAULT_ZOOM) * 100)
        return f'Cursor: X={wx:6.1f} mm | Y={wy:6.1f} mm | R={r:5.1f} mm | Zoom: {zoom_pct}%'
