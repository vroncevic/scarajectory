# -*- coding: UTF-8 -*-

'''
Module
    trajectory_canvas.py
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
    Vector CAD drawing canvas with dynamic sizing and deadzone protection.
'''

from __future__ import annotations

from tkinter import Canvas, Widget
from typing import Final

from scarajectory.infrastructure.gui.canvas.bundle import CanvasBundle
from scarajectory.infrastructure.gui.canvas.status.icanvas_status_presenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.canvas.render.renderer import CanvasRenderer
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryCanvas(Canvas):
    '''
        Vector CAD drawing canvas with dynamic sizing and deadzone protection.

        It defines:

            :attributes:
                | _bundle - Injected domain services and storage dependency bundle.
                | _settings - Active canvas configuration DTO.
                | _tool_mode - Active interactive drawing tool.
                | _vp - Viewport transformation matrix.
                | _state - Interactive mouse pan, drag and selection state.
                | _navigator - Viewport zoom, pan, and framing coordinator interface.
                | _status_presenter - Cursor status presenter collaborator interface.
            :methods:
                | __init__ - Initializes vector CAD canvas widget and assigns dependencies.
                | mount_navigation - Mounts view navigator and status presenter interfaces.
                | get_view_dimensions - Returns current width and height in pixels.
                | redraw - Clears and redraws entire vector scene.
                | set_tool_mode - Changes active drawing/selection tool.
                | update_settings - Updates default parameters and deadzone settings.
    '''

    _bundle: CanvasBundle
    _settings: CanvasSettings
    _tool_mode: CanvasToolMode
    _vp: ViewportTransform
    _state: CanvasInteractionState
    _navigator: ICanvasViewNavigator
    _status_presenter: ICanvasStatusPresenter

    def __init__(
        self,
        parent: Widget,
        *,
        bundle: CanvasBundle,
        vp: ViewportTransform,
        state: CanvasInteractionState,
    ) -> None:
        '''
            Initializes the vector CAD canvas widget and assigns dependencies.

            :param parent: Parent Tk widget container.
            :param bundle: Required CanvasBundle dependency container.
            :param vp: Required ViewportTransform instance.
            :param state: Required CanvasInteractionState instance.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            bg='#181a1f',
            highlightthickness=1,
            highlightbackground='#333842',
        )
        self._bundle: Final[CanvasBundle] = bundle
        self._settings = bundle.settings
        self._tool_mode = CanvasToolMode.POINT
        self._vp: Final[ViewportTransform] = vp
        self._state: Final[CanvasInteractionState] = state

    def mount_navigation(
        self,
        *,
        navigator: ICanvasViewNavigator,
        status_presenter: ICanvasStatusPresenter,
    ) -> None:
        '''
            Mounts injected navigation and status presentation collaborators.

            :param navigator: Injected ICanvasViewNavigator interface.
            :param status_presenter: Injected ICanvasStatusPresenter interface.
            :exceptions: None.
        '''
        self._navigator: Final[ICanvasViewNavigator] = navigator
        self._status_presenter: Final[ICanvasStatusPresenter] = (
            status_presenter
        )

    @property
    def navigator(self) -> ICanvasViewNavigator:
        '''
            Returns viewport navigation coordinator.

            :return: ICanvasViewNavigator interface.
            :exceptions: None.
        '''
        return self._navigator

    @property
    def status_presenter(self) -> ICanvasStatusPresenter:
        '''
            Returns cursor status presenter component.

            :return: ICanvasStatusPresenter interface.
            :exceptions: None.
        '''
        return self._status_presenter

    @property
    def tool_mode(self) -> CanvasToolMode:
        '''
            Returns active drawing or selection tool mode.

            :return: CanvasToolMode enum value.
            :exceptions: None.
        '''
        return self._tool_mode

    @property
    def settings(self) -> CanvasSettings:
        '''
            Returns active canvas configuration settings.

            :return: CanvasSettings instance.
            :exceptions: None.
        '''
        return self._settings

    def get_view_dimensions(self) -> tuple[int, int]:
        '''
            Returns current width and height of canvas viewport in pixels.

            :return: Tuple of (width, height) integers.
            :exceptions: None.
        '''
        return self.winfo_width(), self.winfo_height()

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Changes active drawing/selection tool.

            :param mode: CanvasToolMode enum value.
            :exceptions: None.
        '''
        self._tool_mode = mode
        self._state.reset_drag()
        self.redraw()

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates default parameters and deadzone settings.

            :param settings: Updated CanvasSettings instance.
            :exceptions: None.
        '''
        self._settings = settings
        self.redraw()

    def redraw(self) -> None:
        '''
            Clears and redraws entire vector scene.

            :exceptions: None.
        '''
        self.delete('all')
        w: int = self.winfo_width()
        h: int = self.winfo_height()

        if w < 10 or h < 10:
            return

        CanvasRenderer.draw_background(
            self, self._vp, self._bundle.validator
        )
        CanvasRenderer.draw_trajectory(
            self,
            self._vp,
            self._bundle.store,
            self._bundle.selection,
            self._bundle.validator,
        )

        if self._state.drag_start_world and self._state.drag_current_world:
            CanvasRenderer.draw_preview(
                self,
                self._vp,
                self._tool_mode,
                (self._state.drag_start_world, self._state.drag_current_world),
            )
