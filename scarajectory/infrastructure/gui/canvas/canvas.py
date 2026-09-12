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

from tkinter import Canvas, Widget
from tkinter.ttk import Label
from typing import ClassVar, Final

from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.canvas_renderer import CanvasRenderer
from scarajectory.infrastructure.gui.canvas.canvas_mouse_handler import CanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.canvas_event_binder import CanvasEventBinder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryCanvas(Canvas):
    '''
        Vector CAD drawing canvas with dynamic sizing, interactive zoom/pan, and deadzone protection.

        It defines:

            :attributes:
                | R_MIN_MM - Fallback minimum radius deadzone boundary in mm.
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
                | r_min_mm - Returns active minimum workspace reach radius in mm.
                | r_max_mm - Returns active maximum workspace reach radius in mm.
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

    R_MIN_MM: ClassVar[float] = 86.1
    SELECT_HIT_RADIUS_PX: ClassVar[float] = 12.0
    FREEHAND_MIN_DISTANCE_MM: ClassVar[float] = 5.0
    CIRCLE_MIN_RADIUS_MM: ClassVar[float] = 5.0
    CIRCLE_DEFAULT_STEPS: ClassVar[int] = 16

    _plan: ITrajectoryPlan
    _validator: ITrajectoryValidator
    _settings: CanvasSettings
    _tool_mode: CanvasToolMode
    _vp: ViewportTransform
    _state: CanvasInteractionState
    _mouse_handler: CanvasMouseHandler
    _hover_label: Label | None

    def __init__(
        self,
        parent: Widget,
        plan: ITrajectoryPlan,
        validator: ITrajectoryValidator,
        settings: CanvasSettings = CanvasSettings(),
        **kwargs: object
    ) -> None:
        '''
            Initializes the vector CAD canvas and binds events.

            :param parent: Parent Tk widget.
            :param plan: TrajectoryPlan instance.
            :param validator: ITrajectoryValidator instance.
            :param settings: CanvasSettings instance.
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
        self._mouse_handler: Final[CanvasMouseHandler] = CanvasMouseHandler(
            self._plan, self._vp, self._state
        )
        self._event_binder = CanvasEventBinder(self, self._mouse_handler)
        self._hover_label = None

        self._plan.add_observer(self)
        self._event_binder.bind_events()

    @property
    def r_min_mm(self) -> float:
        '''
            Returns the dynamic inner workspace reach radius in mm.

            :return: Minimum reach radius float value.
        '''
        return self._validator.r_min

    @property
    def r_max_mm(self) -> float:
        '''
            Returns the dynamic outer workspace reach radius in mm.

            :return: Maximum reach radius float value.
        '''
        return self._validator.r_max

    def on_trajectory_updated(self) -> None:
        '''
            Redraws canvas on plan change.
        '''
        self.redraw()

    def on_point_selected(self, index: int) -> None:
        '''
            Redraws selection ring when waypoint selection changes.

            :param index: Selected index.
        '''
        _ = index
        self.redraw()

    def set_hover_label(self, label: Label) -> None:
        '''
            Configures status bar label for cursor readouts.

            :param label: Label instance.
        '''
        self._hover_label = label

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Changes active drawing/selection tool.

            :param mode: Target CanvasToolMode.
        '''
        self._tool_mode = mode
        self._state.reset_drag()
        self.redraw()

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates default parameters and deadzone settings.

            :param settings: New CanvasSettings.
        '''
        self._settings = settings
        self.redraw()

    def fit_reach_view(self) -> None:
        '''
            Auto-fits the SCARA maximum reach circle into view.
        '''
        w, h = self.winfo_width(), self.winfo_height()
        self._vp.fit_reach(w, h, self._validator.r_max)
        self.redraw()

    def reset_view(self) -> None:
        '''
            Resets zoom to 100% and centers workspace.
        '''
        self._vp.reset()
        self.redraw()

    def zoom_in(self) -> None:
        '''
            Scales view in by zoom factor.
        '''
        self._vp.zoom_in()
        self.redraw()

    def zoom_out(self) -> None:
        '''
            Scales view out by zoom factor.
        '''
        self._vp.zoom_out()
        self.redraw()

    def redraw(self) -> None:
        '''
            Clears and redraws entire vector scene.
        '''
        self.delete('all')
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10:
            return

        CanvasRenderer.draw_background(self, self._vp, self._validator)
        CanvasRenderer.draw_trajectory(self, self._vp, self._plan, self._validator)

        if self._state.drag_start_world and self._state.drag_current_world:
            CanvasRenderer.draw_preview(
                self, self._vp,
                self._tool_mode,
                (self._state.drag_start_world, self._state.drag_current_world)
            )

