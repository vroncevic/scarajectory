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
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.canvas.renderer.renderer import CanvasRenderer
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.bundle import TrajectoryRenderBundle
from scarajectory.infrastructure.gui.canvas.status.ipresenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

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
        Vector CAD drawing canvas with dynamic sizing and deadzone protection.

        It defines:

            :attributes:
                | settings - Active canvas configuration DTO.
                | tool_mode - Active interactive drawing tool mode.
                | navigator - Canvas view navigator controller.
                | status_presenter - Canvas status presenter.
                | _bundle - Injected domain services and storage dependency bundle.
                | _vp - Viewport transformation matrix.
                | _state - Interactive mouse pan, drag and selection state.
            :methods:
                | __init__ - Initializes vector CAD canvas widget and assigns dependencies.
                | attach_presentation - Associates navigator and status presenter with canvas.
                | get_view_dimensions - Returns current width and height in pixels.
                | redraw - Clears and redraws entire vector scene.
                | set_tool_mode - Changes active drawing/selection tool.
                | update_settings - Updates default parameters and deadzone settings.
    '''

    settings: CanvasSettings
    tool_mode: CanvasToolMode
    navigator: ICanvasViewNavigator
    status_presenter: ICanvasStatusPresenter

    _bundle: CanvasBundle
    _vp: ViewportTransform
    _state: CanvasInteractionState

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
        self._vp: Final[ViewportTransform] = vp
        self._state: Final[CanvasInteractionState] = state
        self.settings = bundle.settings
        self.tool_mode = CanvasToolMode.POINT

    def attach_presentation(
        self,
        navigator: ICanvasViewNavigator,
        status_presenter: ICanvasStatusPresenter,
    ) -> None:
        '''
            Associates view navigator and status presenter with this canvas.

            :param navigator: ICanvasViewNavigator collaborator.
            :param status_presenter: ICanvasStatusPresenter collaborator.
            :exceptions: None.
        '''
        self.navigator = navigator
        self.status_presenter = status_presenter

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
        self.tool_mode = mode
        self._state.reset_drag()
        self.redraw()

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates default parameters and deadzone settings.

            :param settings: Updated CanvasSettings instance.
            :exceptions: None.
        '''
        self.settings = settings
        self.redraw()

    def redraw(self) -> None:
        '''
            Clears and redraws entire vector scene.

            :exceptions: None.
        '''
        w: int = self.winfo_width()
        h: int = self.winfo_height()

        if w < 10 or h < 10:
            return

        self.delete('all')

        CanvasRenderer.draw_background(
            self,
            self._vp,
            self._bundle.validator,
            self._bundle.boundary_adapter,
        )

        CanvasRenderer.draw_trajectory(
            self,
            self._vp,
            TrajectoryRenderBundle(
                store=self._bundle.store,
                selection=self._bundle.selection,
                validator=self._bundle.validator,
            ),
        )

        if self._state.is_dragging:
            CanvasRenderer.draw_preview(
                self,
                self._vp,
                self.tool_mode,
                (self._state.drag_start_world, self._state.drag_current_world),
            )
