# -*- coding: UTF-8 -*-

'''
Module
    canvas.py
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
    Interactive CAD Vector Canvas with dynamic resizing, zoom/pan and deadzone enforcement.
'''

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk
from typing import ClassVar, Final

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.model.canvas_settings_dto import CanvasSettingsDTO
from scarajectory.core.model.canvas_tool_mode import CanvasToolMode
from scarajectory.core.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.core.model.viewport_transform import ViewportTransform
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.components.canvas_renderer import CanvasRenderer
from scarajectory.infrastructure.gui.components.canvas_tool_handler import CanvasToolHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryCanvas(tk.Canvas):
    '''
        Vector CAD drawing canvas with dynamic sizing, interactive zoom/pan, and deadzone protection.

        It defines:

            :attributes:
                | R_MIN_MM - Minimum radius deadzone boundary in mm.
                | SELECT_HIT_RADIUS_PX - Hit detection pixel radius for selecting waypoints.
                | FREEHAND_MIN_DISTANCE_MM - Minimum distance threshold in mm for freehand point sampling.
                | CIRCLE_MIN_RADIUS_MM - Minimum radius threshold in mm for inserting circle shapes.
                | CIRCLE_DEFAULT_STEPS - Number of waypoint segments used for circle discretization.
                | _plan - ITrajectoryPlan instance.
                | _validator - Kinematic reachability validator.
                | _settings - Active canvas configuration DTO.
                | _tool_mode - Active interactive drawing tool.
                | _vp - Viewport transformation matrix.
                | _state - Interactive mouse pan, drag and selection state.
                | _hover_label - Hover status readout widget.
            :methods:
                | __init__ - Initializes the vector CAD canvas and binds events.
                | on_trajectory_updated - Redraws canvas on plan change.
                | on_point_selected - Redraws selection ring when waypoint selection changes.
                | set_hover_label - Configures status bar label for cursor readouts.
                | set_tool_mode - Changes active drawing/selection tool.
                | update_settings - Updates default parameters and deadzone settings.
                | fit_reach_view - Auto-fits the SCARA maximum reach circle into view.
                | reset_view - Resets zoom to 100% and centers workspace.
                | zoom_in - Scales view by factor.
                | zoom_out - Scales view by factor.
                | redraw - Clears and redraws entire vector scene.
    '''

    R_MIN_MM: ClassVar[float] = 30.0
    SELECT_HIT_RADIUS_PX: ClassVar[float] = 12.0
    FREEHAND_MIN_DISTANCE_MM: ClassVar[float] = 5.0
    CIRCLE_MIN_RADIUS_MM: ClassVar[float] = 5.0
    CIRCLE_DEFAULT_STEPS: ClassVar[int] = 16

    _plan: ITrajectoryPlan
    _validator: ITrajectoryValidator
    _settings: CanvasSettingsDTO
    _tool_mode: CanvasToolMode
    _vp: ViewportTransform
    _state: CanvasInteractionState
    _hover_label: ttk.Label | None

    def __init__(
        self,
        parent: tk.Widget,
        plan: ITrajectoryPlan,
        validator: ITrajectoryValidator,
        settings: CanvasSettingsDTO = CanvasSettingsDTO(),
        **kwargs: object
    ) -> None:
        '''
            Initializes the vector CAD canvas and binds events.

            :param parent: Parent Tk widget.
            :param plan: TrajectoryPlan instance.
            :param validator: ITrajectoryValidator instance.
            :param settings: CanvasSettingsDTO instance.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            bg='#181a1f',
            highlightthickness=1,
            highlightbackground='#333842',
            **kwargs
        )
        self._plan: Final[ITrajectoryPlan] = plan
        self._validator: Final[ITrajectoryValidator] = validator
        self._settings = settings
        self._tool_mode = CanvasToolMode.POINT
        self._vp = ViewportTransform()
        self._state = CanvasInteractionState()
        self._hover_label = None

        self._plan.add_observer(self)

        self.bind('<Configure>', lambda e: self.redraw())
        self.bind('<ButtonPress-1>', self._on_mouse_down)
        self.bind('<ButtonPress-2>', self._on_mouse_down)
        self.bind('<ButtonPress-3>', self._on_mouse_down)
        self.bind('<B1-Motion>', self._on_mouse_drag)
        self.bind('<B2-Motion>', self._on_mouse_drag)
        self.bind('<B3-Motion>', self._on_mouse_drag)
        self.bind('<ButtonRelease-1>', self._on_mouse_up)
        self.bind('<ButtonRelease-2>', self._on_mouse_up)
        self.bind('<ButtonRelease-3>', self._on_mouse_up)
        self.bind('<MouseWheel>', self._on_mouse_wheel_or_move)
        self.bind('<Motion>', self._on_mouse_wheel_or_move)

    def on_trajectory_updated(self) -> None:
        '''
            Redraws canvas on plan change.

            :exceptions: None.
        '''
        self.redraw()

    def on_point_selected(self, index: int) -> None:
        '''
            Redraws selection ring when waypoint selection changes.

            :param index: Selected index.
            :exceptions: None.
        '''
        _ = index
        self.redraw()

    def set_hover_label(self, label: ttk.Label) -> None:
        '''
            Configures status bar label for cursor readouts.

            :param label: ttk.Label instance.
            :exceptions: None.
        '''
        self._hover_label = label

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Changes active drawing/selection tool.

            :param mode: Target CanvasToolMode.
            :exceptions: None.
        '''
        self._tool_mode = mode
        self._state.reset_drag()
        self.redraw()

    def update_settings(self, settings: CanvasSettingsDTO) -> None:
        '''
            Updates default parameters and deadzone settings.

            :param settings: New CanvasSettingsDTO.
            :exceptions: None.
        '''
        self._settings = settings
        self.redraw()

    def fit_reach_view(self) -> None:
        '''
            Auto-fits the SCARA maximum reach circle into view.

            :exceptions: None.
        '''
        w, h = self.winfo_width(), self.winfo_height()
        self._vp.fit_reach(w, h)
        self.redraw()

    def reset_view(self) -> None:
        '''
            Resets zoom to 100% and centers workspace.

            :exceptions: None.
        '''
        self._vp.reset()
        self.redraw()

    def zoom_in(self) -> None:
        '''
            Scales view in by zoom factor.

            :exceptions: None.
        '''
        self._vp.zoom_in()
        self.redraw()

    def zoom_out(self) -> None:
        '''
            Scales view out by zoom factor.

            :exceptions: None.
        '''
        self._vp.zoom_out()
        self.redraw()

    def redraw(self) -> None:
        '''
            Clears and redraws entire vector scene.

            :exceptions: None.
        '''
        self.delete('all')
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10:
            return

        CanvasRenderer.draw_background(self, self._vp, self.R_MIN_MM)
        CanvasRenderer.draw_trajectory(self, self._vp, self._plan, self._validator)

        if self._state.drag_start_world and self._state.drag_current_world:
            CanvasRenderer.draw_preview(
                self, self._vp,
                self._tool_mode,
                (self._state.drag_start_world, self._state.drag_current_world)
            )

    def _on_mouse_down(self, event: tk.Event) -> None:
        '''
            Handles mouse button press for tool interaction or viewport pan.

            :param event: Tk event.
            :exceptions: None.
        '''
        if getattr(event, 'num', 1) in (2, 3):
            self._state.pan_x = event.x
            self._state.pan_y = event.y
            self._state.is_panning = True
            return

        w, h = self.winfo_width(), self.winfo_height()
        wx, wy = self._vp.screen_to_world(event.x, event.y, w, h)
        self._state.drag_start_world = (wx, wy)
        self._state.drag_current_world = (wx, wy)
        self._state.dragged_node_idx = -1

        hit_r_world: float = self.SELECT_HIT_RADIUS_PX / self._vp.scale
        hit_idx: int = CanvasToolHandler.find_hit_index(self._plan.waypoints, wx, wy, hit_r_world)

        if self._tool_mode == CanvasToolMode.SELECT:
            if hit_idx >= 0:
                self._state.dragged_node_idx = hit_idx
                self._plan.select_point(hit_idx)
            else:
                self._plan.select_point(-1)
        elif self._tool_mode == CanvasToolMode.FREEHAND:
            self._plan.add_point(Waypoint(x=wx, y=wy, z=self._settings.default_z, phi=0.0, speed=self._settings.default_speed))

    def _on_mouse_drag(self, event: tk.Event) -> None:
        '''
            Handles mouse drag motion for active CAD tool or panning.

            :param event: Tk event.
            :exceptions: None.
        '''
        if self._state.is_panning:
            self._vp.pan_x += event.x - self._state.pan_x
            self._vp.pan_y += event.y - self._state.pan_y
            self._state.pan_x = event.x
            self._state.pan_y = event.y
            self.redraw()
            return

        w, h = self.winfo_width(), self.winfo_height()
        wx, wy = self._vp.screen_to_world(event.x, event.y, w, h)
        self._state.drag_current_world = (wx, wy)

        if self._tool_mode == CanvasToolMode.SELECT and self._state.dragged_node_idx >= 0:
            cur_pt = self._plan.waypoints[self._state.dragged_node_idx]
            self._plan.update_point(
                self._state.dragged_node_idx,
                Waypoint(x=wx, y=wy, z=cur_pt.z, phi=cur_pt.phi, speed=cur_pt.speed, name=cur_pt.name)
            )
        elif self._tool_mode == CanvasToolMode.FREEHAND and self._plan.count > 0:
            last = self._plan.waypoints[-1]
            if CanvasToolHandler.is_freehand_distance_met(last, wx, wy, self.FREEHAND_MIN_DISTANCE_MM):
                self._plan.add_point(Waypoint(x=wx, y=wy, z=self._settings.default_z, phi=0.0, speed=self._settings.default_speed))
        elif self._tool_mode in (CanvasToolMode.CIRCLE, CanvasToolMode.RECTANGLE, CanvasToolMode.LINE):
            self.redraw()

    def _on_mouse_up(self, event: tk.Event) -> None:
        '''
            Finalizes shape insertion or pan operation on mouse release.

            :param event: Tk event.
            :exceptions: None.
        '''
        if self._state.is_panning:
            self._state.is_panning = False
            return

        w, h = self.winfo_width(), self.winfo_height()
        wx, wy = self._vp.screen_to_world(event.x, event.y, w, h)

        if self._state.drag_start_world:
            x0, y0 = self._state.drag_start_world
            if self._tool_mode == CanvasToolMode.POINT:
                self._plan.add_point(Waypoint(x=wx, y=wy, z=self._settings.default_z, phi=0.0, speed=self._settings.default_speed))
            elif self._tool_mode == CanvasToolMode.LINE:
                if math.hypot(wx - x0, wy - y0) > 1.0:
                    line_pts = CanvasToolHandler.discretize_line((x0, y0), (wx, wy), self._settings)
                    self._plan.set_waypoints(list(self._plan.waypoints) + line_pts)
            elif self._tool_mode == CanvasToolMode.CIRCLE:
                radius: float = math.hypot(wx - x0, wy - y0)
                if radius >= self.CIRCLE_MIN_RADIUS_MM:
                    circle_pts = CanvasToolHandler.discretize_circle(
                        (x0, y0), radius, self.CIRCLE_DEFAULT_STEPS, self._settings
                    )
                    self._plan.set_waypoints(list(self._plan.waypoints) + circle_pts)
            elif self._tool_mode == CanvasToolMode.RECTANGLE:
                if abs(wx - x0) > 2.0 and abs(wy - y0) > 2.0:
                    rect_pts = CanvasToolHandler.discretize_rectangle(
                        (x0, y0), (wx, wy), self._settings
                    )
                    self._plan.set_waypoints(list(self._plan.waypoints) + rect_pts)

        self._state.reset_drag()
        self.redraw()

    def _on_mouse_wheel_or_move(self, event: tk.Event) -> None:
        '''
            Handles mouse wheel zooming and hover label coordinate readout.

            :param event: Tk event.
            :exceptions: None.
        '''
        if hasattr(event, 'delta') and event.delta != 0:
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            return

        if self._hover_label:
            w, h = self.winfo_width(), self.winfo_height()
            wx, wy = self._vp.screen_to_world(event.x, event.y, w, h)
            r: float = math.hypot(wx, wy)
            zoom_pct: int = int((self._vp.scale / ViewportTransform.DEFAULT_ZOOM) * 100)
            self._hover_label['text'] = (
                f'Cursor: X={wx:6.1f} mm | Y={wy:6.1f} mm | R={r:5.1f} mm | Zoom: {zoom_pct}%'
            )
