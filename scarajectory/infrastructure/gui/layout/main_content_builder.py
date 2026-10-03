# -*- coding: UTF-8 -*-

'''
Module
    main_content_builder.py
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
from typing import Final

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.controls.controls_panel import ControlsPanel
from scarajectory.infrastructure.gui.editor.waypoint_editor import WaypointEditor
from scarajectory.infrastructure.gui.layout.icanvas_pane_builder import ICanvasPaneBuilder
from scarajectory.infrastructure.gui.layout.ieditor_pane_builder import IEditorPaneBuilder
from scarajectory.infrastructure.gui.layout.itoolbar_layout_builder import IToolbarLayoutBuilder
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MainContentBuilder:
    '''
        Constructs and mounts primary split-view desktop components for ScarajectoryGUI.

        It defines:

            :attributes:
                | _canvas_pane_builder - Sub-builder for left canvas pane.
                | _toolbar_builder - Sub-builder for top toolbar.
                | _editor_pane_builder - Sub-builder for right editor pane.
            :methods:
                | __init__ - Initializes MainContentBuilder with injected layout builders.
                | build_content - Builds split view layout with Toolbar, Canvas, Table and Controls.
                | get_version - Returns builder version string.
    '''

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
        bundle: ScarajectoryGUIInitBundle,
    ) -> tuple[TrajectoryCanvas, Toolbar, WaypointEditor, ControlsPanel]:
        '''
            Builds split view layout with Toolbar, Canvas, Table and Controls.

            :param root: Root Tkinter window.
            :param bundle: GUI initialization dependencies bundle.
            :return: Tuple containing Canvas, Toolbar, WaypointEditor, and ControlsPanel.
            :exceptions: None.
        '''
        settings = CanvasSettings(
            default_z=20.0,
            default_speed=bundle.validator.bounds.default_speed,
            enforce_deadzone=True,
        )
        main_paned = PanedWindow(root, orient=HORIZONTAL)
        canvas = self._canvas_pane_builder.build(
            main_paned, bundle=bundle, settings=settings
        )
        toolbar = self._toolbar_builder.build(
            root, canvas=canvas, bundle=bundle, settings=settings
        )
        main_paned.pack(fill=BOTH, expand=True, padx=8, pady=4)
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
