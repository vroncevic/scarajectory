# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Main Tkinter graphical interface adapter coordinating menu, toolbar, canvas, table and controls.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Final

from scarajectory.core.model.canvas_settings import CanvasSettings
from scarajectory.core.model.stream_progress import StreamProgress
from scarajectory.core.service.iservice import IService
from scarajectory.infrastructure.gui.icanvas import ICanvas
from scarajectory.infrastructure.gui.icontrols import IControls
from scarajectory.infrastructure.gui.itable import ITable
from scarajectory.infrastructure.gui.canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.controls import ControlsPanel
from scarajectory.infrastructure.gui.theme import ThemeManager
from scarajectory.infrastructure.gui.components.waypoint_editor import WaypointEditor
from scarajectory.infrastructure.gui.components.toolbar import Toolbar
from scarajectory.infrastructure.gui.components.menu_bar import AppMenuBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScarajectoryGUI:
    '''
        Main Tkinter GUI adapter coordinating vector canvas, tabular view, and controls.

        It defines:

            :attributes:
                | _root - Root Tkinter application window.
                | _service - Core trajectory service instance.
                | _canvas - Vector CAD drawing canvas component.
                | _table - Tabular waypoint view component.
                | _controls - Tabbed control panels component.
                | _toolbar - Top toolbar subcomponent.
                | _menu_bar - Application top menu bar subcomponent.
            :methods:
                | __init__ - Initializes GUI window and layout.
                | is_initialized - Checks if GUI components are initialized.
                | start - Starts the Tkinter main event loop.
                | stop - Closes and destroys the window.
                | load_file - Loads trajectory JSON file into plan.
                | set_deadzone - Sets deadzone enforcement state.
                | on_stream_progress - Receives streamer progress updates.
                | on_serial_log - Receives serial traffic messages.
                | on_trajectory_updated - Receives plan modification notifications.
                | on_point_selected - Receives waypoint selection notifications.
    '''

    _root: tk.Tk
    _service: IService
    _canvas: ICanvas
    _table: ITable
    _controls: IControls
    _toolbar: Toolbar
    _menu_bar: AppMenuBar

    def __init__(self, service: IService, root: tk.Tk | None = None) -> None:
        '''
            Initializes GUI window and layout.

            :param service: IService core logic instance.
            :param root: Optional root Tk window.
            :exceptions: None.
        '''
        self._service: Final[IService] = service
        self._root: Final[tk.Tk] = root if root is not None else tk.Tk()
        self._root.title('SCARAjectory — Motion Trajectory Studio & Streamer')
        sw: int = self._root.winfo_screenwidth()
        sh: int = self._root.winfo_screenheight()
        self._root.geometry(f'{sw}x{sh}+0+0')
        self._root.minsize(1100, 700)

        ThemeManager.apply_theme(self._root)
        self._create_main_content()

        self._menu_bar = AppMenuBar(
            root=self._root,
            service=self._service,
            canvas=self._canvas,
            table=self._table
        )

        self._service.get_plan().add_observer(self)
        self._service.get_streamer().set_observer(self)

        self._root.update_idletasks()

        try:
            self._root.attributes('-zoomed', True)
        except tk.TclError:
            try:
                self._root.state('zoomed')
            except tk.TclError:
                pass

        self._root.after(150, self._canvas.fit_reach_view)

    def is_initialized(self) -> bool:
        '''
            Checks if GUI components are initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return self._root is not None and self._canvas is not None and self._table is not None

    def start(self) -> None:
        '''
            Starts the Tkinter main event loop.

            :exceptions: None.
        '''
        self._root.mainloop()

    def stop(self) -> None:
        '''
            Closes and destroys the window.

            :exceptions: None.
        '''
        try:
            self._service.stop_streaming()
        except (AttributeError, RuntimeError):
            pass
        self._root.quit()
        self._root.destroy()

    def load_file(self, filepath: str) -> None:
        '''
            Loads trajectory JSON file into plan.

            :param filepath: JSON file path.
            :exceptions: None.
        '''
        try:
            self._service.load_plan(filepath)
            self._canvas.fit_reach_view()
        except OSError as exc:
            messagebox.showerror('Load Error', f'Failed to load plan: {exc}')

    def set_deadzone(self, enabled: bool) -> None:
        '''
            Sets deadzone enforcement state.

            :param enabled: True to enforce deadzone, False to disable.
            :exceptions: None.
        '''
        self._toolbar.set_deadzone(enabled)

    def on_stream_progress(self, progress: StreamProgress) -> None:
        '''
            Receives streamer progress updates.

            :param progress: StreamProgress model.
            :exceptions: None.
        '''
        self._controls.update_progress(progress)

    def on_serial_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Receives serial traffic messages.

            :param text: Log line text.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        self._controls.append_log(text, is_outgoing)

    def on_trajectory_updated(self) -> None:
        '''
            Receives plan modification notifications.

            :exceptions: None.
        '''

    def on_point_selected(self, index: int) -> None:
        '''
            Receives waypoint selection notifications.

            :param index: Selected index.
            :exceptions: None.
        '''
        _ = index

    def _create_main_content(self) -> None:
        '''
            Builds split view layout with Toolbar, Canvas, Table and Controls.

            :exceptions: None.
        '''
        settings = CanvasSettings(default_z=20.0, default_speed=40.0, enforce_deadzone=True)

        main_paned = ttk.PanedWindow(self._root, orient=tk.HORIZONTAL)

        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)

        self._canvas = TrajectoryCanvas(
            left_frame,
            plan=self._service.get_plan(),
            validator=self._service.get_validator(),
            settings=settings
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

        self._toolbar = Toolbar(
            self._root,
            canvas=self._canvas,
            plan=self._service.get_plan()
        )
        self._toolbar.pack(side=tk.TOP, fill=tk.X)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        right_paned = ttk.PanedWindow(right_frame, orient=tk.VERTICAL)
        right_paned.pack(fill=tk.BOTH, expand=True)

        self._table = WaypointEditor(right_paned, plan=self._service.get_plan())
        right_paned.add(self._table, weight=1)

        ctl_frame = ttk.Frame(right_paned)
        right_paned.add(ctl_frame, weight=1)
        self._controls = ControlsPanel(
            ctl_frame,
            plan=self._service.get_plan(),
            validator=self._service.get_validator(),
            streamer=self._service.get_streamer()
        )
        self._controls.pack(fill=tk.BOTH, expand=True)
