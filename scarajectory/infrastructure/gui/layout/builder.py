# -*- coding: UTF-8 -*-

'''
Module
    builder.py
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
    Builder assembling primary desktop layout components: Canvas, Toolbar, Editor, and Controls.
'''

from __future__ import annotations

from tkinter import BOTH, HORIZONTAL, Tk
from tkinter.ttk import PanedWindow
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.controls.panel import ControlsPanel
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.editor.editor import WaypointEditor
from scarajectory.infrastructure.gui.layout.canvas.ibuilder import ICanvasPaneBuilder
from scarajectory.infrastructure.gui.layout.editor.ibuilder import IEditorPaneBuilder
from scarajectory.infrastructure.gui.layout.toolbar.ibuilder import IToolbarLayoutBuilder
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MainContentBuilder:
    '''
        Constructs and mounts primary split-view desktop components for ScarajectoryGUI.

        It defines:

            :constants:
                | PAD_X - Horizontal padding for main paned window container.
                | PAD_Y - Vertical padding for main paned window container.
            :attributes:
                | _canvas_pane_builder - Sub-builder for left canvas pane.
                | _toolbar_builder - Sub-builder for top toolbar.
                | _editor_pane_builder - Sub-builder for right editor pane.
            :methods:
                | __init__ - Initializes MainContentBuilder with injected layout builders.
                | build_content - Builds split view layout with Toolbar, Canvas, Table and Controls.
                | get_version - Returns builder version string.
    '''

    PAD_X: ClassVar[int] = 8
    PAD_Y: ClassVar[int] = 4

    _canvas_pane_builder: ICanvasPaneBuilder
    _toolbar_builder: IToolbarLayoutBuilder
    _editor_pane_builder: IEditorPaneBuilder

    def __init__(
        self,
        *,
        canvas_pane_builder: ICanvasPaneBuilder,
        toolbar_builder: IToolbarLayoutBuilder,
        editor_pane_builder: IEditorPaneBuilder,
    ) -> None:
        '''
            Initializes MainContentBuilder with injected layout sub-builders.

            :param canvas_pane_builder: Canvas pane layout builder component.
            :param toolbar_builder: Toolbar layout builder component.
            :param editor_pane_builder: Editor pane layout builder component.
            :exceptions: None.
        '''
        self._canvas_pane_builder: Final[ICanvasPaneBuilder] = (
            canvas_pane_builder
        )
        self._toolbar_builder: Final[IToolbarLayoutBuilder] = toolbar_builder
        self._editor_pane_builder: Final[IEditorPaneBuilder] = (
            editor_pane_builder
        )

    def build_content(
        self,
        root: Tk,
        *,
        bundle: GUIDependencies,
    ) -> tuple[TrajectoryCanvas, Toolbar, WaypointEditor, ControlsPanel]:
        '''
            Builds split view layout with Toolbar, Canvas, Table and Controls.

            :param root: Root Tkinter window.
            :param bundle: GUI initialization dependencies bundle.
            :return: Tuple containing Canvas, Toolbar, WaypointEditor, and ControlsPanel.
            :exceptions: None.
        '''
        settings = CanvasSettings(
            default_z=CanvasSettings.DEFAULT_Z_MM,
            default_speed=CanvasSettings.DEFAULT_SPEED_MMS,
            enforce_deadzone=CanvasSettings.DEFAULT_ENFORCE_DEADZONE,
        )
        main_paned = PanedWindow(root, orient=HORIZONTAL)
        canvas = self._canvas_pane_builder.build(
            main_paned, bundle=bundle, settings=settings
        )
        toolbar = self._toolbar_builder.build(
            root, canvas=canvas, bundle=bundle, settings=settings
        )
        main_paned.pack(
            fill=BOTH, expand=True, padx=self.PAD_X, pady=self.PAD_Y
        )
        table, controls = self._editor_pane_builder.build(
            main_paned, bundle=bundle
        )

        return canvas, toolbar, table, controls

    def get_version(self) -> str:
        '''
            Returns the builder version string.

            :return: Builder version string.
            :exceptions: None.
        '''
        return __version__
