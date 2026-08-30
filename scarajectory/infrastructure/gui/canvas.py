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
from typing import Final, override

from scarajectory.core.model.studio_waypoint import StudioWaypoint
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.canvas_settings_dto import CanvasSettingsDTO
from scarajectory.core.model.canvas_tool_mode import CanvasToolMode
from scarajectory.core.model.viewport_transform import ViewportTransform, DEFAULT_ZOOM, R_MAX_MM
from scarajectory.core.service.itrajectory_observer import ITrajectoryObserver
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.icanvas import ICanvas

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

R_MIN_MM: Final[float] = 30.0


class TrajectoryCanvas(tk.Canvas, ICanvas, ITrajectoryObserver):
    '''
        Vector CAD drawing canvas with dynamic sizing, interactive zoom/pan, and deadzone protection.

        It defines:

            :attributes:
                | _plan - Trajectory plan instance.
                | _validator - Kinematic reachability validator.
                | _settings - Active canvas settings DTO.
                | _tool_mode - Active interaction mode enum.
                | _vp - ViewportTransform coordinate manager.
            :methods:
                | __init__ - Initializes vector canvas.
                | set_tool_mode - Sets the active drawing tool mode.
                | update_settings - Updates default point properties.
                | set_hover_label - Sets label widget for cursor coordinates.
                | zoom_in - Scales view in by 1.25x.
                | zoom_out - Scales view out by 0.8x.
                | reset_view - Resets viewport zoom to 100%.
                | fit_reach_view - Fits maximum reach circle to canvas.
                | on_trajectory_updated - Redraws canvas on plan change.
                | on_point_selected - Redraws selection highlighting.
    '''

    _plan: Final[TrajectoryPlan]
    _validator: Final[ITrajectoryValidator]
    _settings: CanvasSettingsDTO
    _tool_mode: CanvasToolMode
    _vp: Final[ViewportTransform]
    _hover_label: ttk.Label | tk.Label | None
    _drag_idx: int
    _drag_start: tuple[float, float] | None
    _pan_start: tuple[float, float] | None

    def __init__(
        self,
        parent: tk.Widget,
        plan: TrajectoryPlan,
        validator: ITrajectoryValidator,
        settings: CanvasSettingsDTO = CanvasSettingsDTO(),
        **kwargs: object
    ) -> None:
        '''
            Initializes vector canvas with plan, validator, and settings DTO.

            :param parent: Parent container widget.
            :param plan: TrajectoryPlan instance.
            :param validator: ITrajectoryValidator instance.
            :param settings: CanvasSettingsDTO configuration.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            bg='#181a1f',
            highlightthickness=1,
            highlightbackground='#333842',
            **kwargs  # type: ignore[arg-type]
        )
        self._plan = plan
        self._validator = validator
        self._settings = settings
        self._tool_mode = CanvasToolMode.POINT
        self._vp = ViewportTransform()
        self._hover_label = None
        self._drag_idx = -1
        self._drag_start = None
        self._pan_start = None

        self._plan.add_observer(self)

        self.bind('<Configure>', lambda e: self._redraw())
        self.bind('<ButtonPress-1>', self._on_mouse_down)
        self.bind('<B1-Motion>', self._on_mouse_drag)
        self.bind('<ButtonRelease-1>', self._on_mouse_up)
        self.bind('<ButtonPress-3>', self._on_mouse_down)
        self.bind('<B3-Motion>', self._on_mouse_drag)
        self.bind('<Motion>', self._on_mouse_motion)
        self.bind('<MouseWheel>', self._on_mouse_motion)
        self.bind('<Button-4>', lambda e: self.zoom_in())
        self.bind('<Button-5>', lambda e: self.zoom_out())

    @override
    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Sets the active drawing tool mode.

            :param mode: CanvasToolMode enum.
            :exceptions: None.
        '''
        self._tool_mode = mode

    @override
    def update_settings(self, settings: CanvasSettingsDTO) -> None:
        '''
            Updates default point properties.

            :param settings: CanvasSettingsDTO instance.
            :exceptions: None.
        '''
        self._settings = settings
        self._redraw()

    def set_hover_label(self, label: ttk.Label | tk.Label) -> None:
        '''
            Sets label widget for cursor coordinates.

            :param label: Tkinter label widget.
            :exceptions: None.
        '''
        self._hover_label = label

    @override
    def zoom_in(self) -> None:
        '''
            Scales view in by 1.25x.

            :exceptions: None.
        '''
        self._vp.zoom_in()
        self._redraw()

    @override
    def zoom_out(self) -> None:
        '''
            Scales view out by 0.8x.

            :exceptions: None.
        '''
        self._vp.zoom_out()
        self._redraw()

    @override
    def reset_view(self) -> None:
        '''
            Resets viewport zoom to 100%.

            :exceptions: None.
        '''
        self._vp.reset()
        self._redraw()

    @override
    def fit_reach_view(self) -> None:
        '''
            Fits maximum reach circle to canvas.

            :exceptions: None.
        '''
        self._vp.fit_reach(self.winfo_width(), self.winfo_height())
        self._redraw()

    @override
    def on_trajectory_updated(self) -> None:
        '''
            Redraws canvas on plan change.

            :exceptions: None.
        '''
        self._redraw()

    @override
    def on_point_selected(self, index: int) -> None:
        '''
            Redraws selection highlighting.

            :param index: Selected index.
            :exceptions: None.
        '''
        self._redraw()

    def _redraw(self) -> None:
        '''
            Renders CAD grid, workspace boundaries, trajectory path, and waypoint nodes.

            :exceptions: None.
        '''
        self.delete('all')
        w: int = self.winfo_width()
        h: int = self.winfo_height()
        cx, cy = self._vp.world_to_screen(0, 0, w, h)

        # 1. Radial Polar Rays (every 30 degrees)
        rmax_px: float = R_MAX_MM * self._vp.scale
        for deg in (30, 60, 120, 150, 210, 240, 300, 330):
            rad: float = math.radians(deg)
            rx: float = cx + rmax_px * math.cos(rad)
            ry: float = cy - rmax_px * math.sin(rad)
            self.create_line(cx, cy, rx, ry, fill='#232830', dash=(2, 6))

        # 2. Concentric Distance Grid Rings (every 50mm up to 250mm)
        for r_mm in (50.0, 100.0, 150.0, 200.0, 250.0):
            r_px: float = r_mm * self._vp.scale
            self.create_oval(cx - r_px, cy - r_px, cx + r_px, cy + r_px, outline='#282c34', dash=(2, 4))
            self.create_text(cx + r_px + 2, cy - 4, text=f'{int(r_mm)}', fill='#5c6370', font=('DejaVu Sans', 7), anchor='w')

        # 3. Main Coordinate Axes & Ticks
        self.create_line(0, cy, w, cy, fill='#3e4451', width=1)
        self.create_line(cx, 0, cx, h, fill='#3e4451', width=1)
        self.create_text(w - 15, cy - 10, text='+X', fill='#61afef', font=('DejaVu Sans', 8, 'bold'))
        self.create_text(cx + 10, 15, text='+Y', fill='#61afef', font=('DejaVu Sans', 8, 'bold'))

        # 4. Reach Envelope & Inner Deadzone Boundary
        rmin_px: float = R_MIN_MM * self._vp.scale
        self.create_oval(cx - rmax_px, cy - rmax_px, cx + rmax_px, cy + rmax_px, outline='#61afef', width=2)
        self.create_oval(cx - rmin_px, cy - rmin_px, cx + rmin_px, cy + rmin_px, outline='#e06c75', width=1, dash=(4, 4))
        self.create_text(cx + rmax_px - 40, cy + rmax_px + 12, text='R_MAX (270mm)', fill='#61afef', font=('DejaVu Sans', 7))
        self.create_text(cx + rmin_px + 5, cy + rmin_px + 10, text='DEADZONE', fill='#e06c75', font=('DejaVu Sans', 7))

        # 5. Base Origin Node
        self.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill='#61afef', outline='#ffffff')
        self.create_text(cx + 8, cy - 8, text='(0,0) BASE', fill='#61afef', font=('DejaVu Sans', 8, 'bold'), anchor='w')

        # 6. Waypoints and Path Segments
        wps = self._plan.waypoints
        if len(wps) > 1:
            coords: list[float] = []
            for pt in wps:
                sx, sy = self._vp.world_to_screen(pt.x, pt.y, w, h)
                coords.extend([sx, sy])
            self.create_line(*coords, fill='#98c379', width=2)

        for i, pt in enumerate(wps):
            sx, sy = self._vp.world_to_screen(pt.x, pt.y, w, h)
            is_sel: bool = (i == self._plan.selected_index)
            color: str = '#e5c07b' if is_sel else '#98c379'
            radius: float = 6.0 if is_sel else 4.0
            self.create_oval(sx - radius, sy - radius, sx + radius, sy + radius, fill=color, outline='#ffffff', width=1)
            self.create_text(sx + 7, sy - 7, text=f'P{i+1}', fill=color, font=('DejaVu Sans', 8, 'bold'), anchor='w')

    def _on_mouse_down(self, event: tk.Event) -> None:
        '''
            Handles mouse down events for left click tool action or right click panning.

            :param event: Tk event.
            :exceptions: None.
        '''
        if event.num == 3:
            self._pan_start = (event.x - self._vp.pan_x, event.y - self._vp.pan_y)
            return

        w, h = self.winfo_width(), self.winfo_height()
        wx, wy = self._vp.screen_to_world(event.x, event.y, w, h)
        r: float = math.hypot(wx, wy)

        if self._settings.enforce_deadzone and (r < R_MIN_MM or r > R_MAX_MM):
            return

        if self._tool_mode == CanvasToolMode.POINT:
            self._plan.add_point(StudioWaypoint(x=wx, y=wy, z=self._settings.default_z, speed=self._settings.default_speed))
        elif self._tool_mode == CanvasToolMode.SELECT:
            for i, pt in enumerate(self._plan.waypoints):
                if math.hypot(pt.x - wx, pt.y - wy) <= (10.0 / self._vp.scale):
                    self._plan.set_selected_index(i)
                    self._drag_idx = i
                    break
        elif self._tool_mode in (CanvasToolMode.CIRCLE, CanvasToolMode.RECTANGLE, CanvasToolMode.FREEHAND):
            self._drag_start = (wx, wy)

    def _on_mouse_drag(self, event: tk.Event) -> None:
        '''
            Handles mouse drag events for panning, moving waypoints, or drawing.

            :param event: Tk event.
            :exceptions: None.
        '''
        if self._pan_start:
            self._vp.pan_x = event.x - self._pan_start[0]
            self._vp.pan_y = event.y - self._pan_start[1]
            self._redraw()
            return

        w, h = self.winfo_width(), self.winfo_height()
        wx, wy = self._vp.screen_to_world(event.x, event.y, w, h)
        if self._tool_mode == CanvasToolMode.SELECT and self._drag_idx >= 0:
            cur = self._plan.waypoints[self._drag_idx]
            self._plan.update_point(self._drag_idx, StudioWaypoint(x=wx, y=wy, z=cur.z, phi=cur.phi, speed=cur.speed, name=cur.name))
        elif self._tool_mode == CanvasToolMode.FREEHAND:
            wps = self._plan.waypoints
            if not wps or math.hypot(wps[-1].x - wx, wps[-1].y - wy) > 10.0:
                self._plan.add_point(StudioWaypoint(x=wx, y=wy, z=self._settings.default_z, speed=self._settings.default_speed))

    def _on_mouse_up(self, event: tk.Event) -> None:
        '''
            Finalizes geometric shape insertion on release.

            :param event: Tk event.
            :exceptions: None.
        '''
        self._pan_start = None
        w, h = self.winfo_width(), self.winfo_height()
        if self._drag_start and self._tool_mode == CanvasToolMode.CIRCLE:
            wx, wy = self._vp.screen_to_world(event.x, event.y, w, h)
            cx, cy = self._drag_start
            radius: float = math.hypot(wx - cx, wy - cy)
            if radius > 5.0:
                steps: int = 16
                for s in range(steps + 1):
                    ang: float = 2.0 * math.pi * (s % steps) / steps
                    self._plan.add_point(StudioWaypoint(
                        x=cx + radius * math.cos(ang),
                        y=cy + radius * math.sin(ang),
                        z=self._settings.default_z,
                        speed=self._settings.default_speed
                    ))
        elif self._drag_start and self._tool_mode == CanvasToolMode.RECTANGLE:
            x1, y1 = self._drag_start
            x2, y2 = self._vp.screen_to_world(event.x, event.y, w, h)
            for px, py in [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]:
                self._plan.add_point(StudioWaypoint(x=px, y=py, z=self._settings.default_z, speed=self._settings.default_speed))

        self._drag_idx = -1
        self._drag_start = None

    def _on_mouse_motion(self, event: tk.Event) -> None:
        '''
            Updates coordinate hover label or processes mouse wheel zoom.

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
            zoom_pct: int = int((self._vp.scale / DEFAULT_ZOOM) * 100)
            self._hover_label['text'] = (
                f'Cursor: X={wx:6.1f} mm | Y={wy:6.1f} mm | R={r:5.1f} mm | Zoom: {zoom_pct}%'
            )
