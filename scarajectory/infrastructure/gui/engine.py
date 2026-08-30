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
    Main Tkinter graphical interface adapter coordinating canvas, table and controls.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Final

from scarajectory.core.model.canvas_settings_dto import CanvasSettingsDTO
from scarajectory.core.model.canvas_tool_mode import CanvasToolMode
from scarajectory.core.model.stream_progress import StreamProgress
from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.service.iservice import IService
from scarajectory.infrastructure.gui.canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.controls import ControlsPanel
from scarajectory.infrastructure.gui.theme import ThemeManager
from scarajectory.infrastructure.gui.table import TrajectoryTable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
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
            :methods:
                | __init__ - Initializes GUI window and layout.
                | is_initialized - Checks if GUI components are initialized.
                | start - Starts the Tkinter main event loop.
                | stop - Closes and destroys the window.
                | load_file - Loads trajectory JSON file into plan.
                | on_stream_progress - Receives streamer progress updates.
                | on_serial_log - Receives serial traffic messages.
                | on_trajectory_updated - Receives plan modification notifications.
                | on_point_selected - Receives waypoint selection notifications.
    '''

    _root: Final[tk.Tk]
    _service: Final[IService]
    _canvas: TrajectoryCanvas
    _table: TrajectoryTable
    _controls: ControlsPanel
    _lbl_cursor: ttk.Label
    _spin_z: ttk.Spinbox
    _spin_speed: ttk.Spinbox
    _deadzone_var: tk.BooleanVar
    _entry_x: ttk.Entry
    _entry_y: ttk.Entry
    _entry_z: ttk.Entry
    _entry_phi: ttk.Entry
    _entry_spd: ttk.Entry

    def __init__(self, service: IService, root: tk.Tk | None = None) -> None:
        '''
            Initializes GUI window and layout.

            :param service: IService core logic instance.
            :param root: Optional root Tk window.
            :exceptions: None.
        '''
        self._service = service
        self._root = root if root is not None else tk.Tk()
        self._root.title('SCARAjectory — Motion Trajectory Studio & Streamer')
        sw: int = self._root.winfo_screenwidth()
        sh: int = self._root.winfo_screenheight()
        self._root.geometry(f'{sw}x{sh}+0+0')
        self._root.minsize(1100, 700)

        ThemeManager.apply_theme(self._root)
        self._create_menu()
        self._create_toolbar()
        self._create_main_content()

        self._service.get_plan().add_observer(self)
        streamer = self._service.get_streamer()
        if hasattr(streamer, 'set_observer'):
            streamer.set_observer(self)

        self._root.update_idletasks()
        try:
            self._root.attributes('-zoomed', True)
        except tk.TclError:
            try:
                self._root.state('zoomed')
            except tk.TclError:
                pass

        self._root.after(150, lambda: self._canvas.fit_reach_view())

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
        self._root.quit()

    def load_file(self, filepath: str) -> None:
        '''
            Loads trajectory JSON file into plan.

            :param filepath: Target JSON file path.
            :exceptions: None.
        '''
        try:
            self._service.load_plan(filepath)
        except (OSError, ValueError) as exc:
            messagebox.showerror('File Load Error', f'Failed to load {filepath}: {exc}')

    def on_stream_progress(self, progress: StreamProgress) -> None:
        '''
            Receives streamer progress updates.

            :param progress: StreamProgress metric container.
            :exceptions: None.
        '''
        self._controls.update_progress(progress)

    def on_serial_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Receives serial traffic messages.

            :param text: Message string content.
            :param is_outgoing: Flag indicating host transmission.
            :exceptions: None.
        '''
        self._controls.append_log(text, is_outgoing=is_outgoing)

    def on_trajectory_updated(self) -> None:
        '''
            Receives plan modification notifications.

            :exceptions: None.
        '''
        plan = self._service.get_plan()
        idx: int = plan.selected_index
        if 0 <= idx < plan.count:
            pt = plan.waypoints[idx]
            for ent, val in (
                (self._entry_x, f'{pt.x:.2f}'),
                (self._entry_y, f'{pt.y:.2f}'),
                (self._entry_z, f'{pt.z:.2f}'),
                (self._entry_phi, f'{pt.phi:.2f}'),
                (self._entry_spd, f'{pt.speed:.1f}')
            ):
                ent.delete(0, tk.END)
                ent.insert(0, val)

    def on_point_selected(self, index: int) -> None:
        '''
            Receives waypoint selection notifications.

            :param index: Selected index.
            :exceptions: None.
        '''
        self.on_trajectory_updated()

    def _create_menu(self) -> None:
        '''
            Creates top application menu bar and binds keyboard shortcuts.

            :exceptions: None.
        '''
        menubar = tk.Menu(self._root, bg='#21252b', fg='#abb2bf', activebackground='#61afef', activeforeground='#ffffff')

        def open_json() -> None:
            path = filedialog.askopenfilename(filetypes=[('SCARA Plan JSON', '*.json'), ('All Files', '*.*')])
            if path:
                self.load_file(path)

        def save_json() -> None:
            path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('SCARA Plan JSON', '*.json')])
            if path:
                try:
                    self._service.save_plan(path)
                    messagebox.showinfo('Save Plan', 'Plan saved successfully!')
                except OSError as exc:
                    messagebox.showerror('Save Error', f'Failed to save plan: {exc}')

        file_m = tk.Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        file_m.add_command(label='New (Ctrl+N)', command=self._service.get_plan().clear)
        file_m.add_command(label='Open JSON... (Ctrl+O)', command=open_json)
        file_m.add_command(label='Save JSON... (Ctrl+S)', command=save_json)
        file_m.add_separator()
        file_m.add_command(label='Exit', command=self._root.quit)
        menubar.add_cascade(label='File', menu=file_m)

        edit_m = tk.Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        edit_m.add_command(label='Undo (Ctrl+Z)', command=self._service.get_plan().undo)
        edit_m.add_command(label='Redo (Ctrl+Y)', command=self._service.get_plan().redo)
        edit_m.add_separator()
        edit_m.add_command(label='Clear All', command=self._service.get_plan().clear)
        menubar.add_cascade(label='Edit', menu=edit_m)

        view_m = tk.Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        view_m.add_command(label='Zoom In (+)', command=lambda: self._canvas.zoom_in())
        view_m.add_command(label='Zoom Out (-)', command=lambda: self._canvas.zoom_out())
        view_m.add_command(label='Fit Workspace', command=lambda: self._canvas.fit_reach_view())
        view_m.add_command(label='Reset 100%', command=lambda: self._canvas.reset_view())
        menubar.add_cascade(label='View', menu=view_m)

        self._root.config(menu=menubar)
        self._root.bind('<Control-n>', lambda e: self._service.get_plan().clear())
        self._root.bind('<Control-o>', lambda e: open_json())
        self._root.bind('<Control-s>', lambda e: save_json())
        self._root.bind('<Control-z>', lambda e: self._service.get_plan().undo())
        self._root.bind('<Control-y>', lambda e: self._service.get_plan().redo())
        self._root.bind('<Delete>', lambda e: self._table.delete_selected())
        self._root.bind('<BackSpace>', lambda e: self._table.delete_selected())

    def _create_toolbar(self) -> None:
        '''
            Creates toolbar with drawing tools, zoom buttons and defaults.

            :exceptions: None.
        '''
        toolbar = ttk.Frame(self._root, padding=(8, 6))
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(toolbar, text='Tool:', style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 4))
        tool_var = tk.StringVar(value='POINT')
        tools = [
            ('Point', 'POINT', CanvasToolMode.POINT),
            ('Select/Move', 'SELECT', CanvasToolMode.SELECT),
            ('Circle', 'CIRCLE', CanvasToolMode.CIRCLE),
            ('Rectangle', 'RECTANGLE', CanvasToolMode.RECTANGLE),
            ('Freehand', 'FREEHAND', CanvasToolMode.FREEHAND)
        ]
        for text, val, mode in tools:
            btn = ttk.Radiobutton(toolbar, text=text, value=val, variable=tool_var, command=lambda m=mode: self._canvas.set_tool_mode(m))
            btn.pack(side=tk.LEFT, padx=2)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Button(toolbar, text='[ + ]', width=4, command=lambda: self._canvas.zoom_in()).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text='[ - ]', width=4, command=lambda: self._canvas.zoom_out()).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text='Fit', width=4, command=lambda: self._canvas.fit_reach_view()).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text='100%', width=5, command=lambda: self._canvas.reset_view()).pack(side=tk.LEFT, padx=1)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Label(toolbar, text='Z (mm):').pack(side=tk.LEFT, padx=2)
        self._spin_z = ttk.Spinbox(toolbar, from_=0.0, to=100.0, increment=5.0, width=5)
        self._spin_z.set('20.0')
        self._spin_z.pack(side=tk.LEFT, padx=2)

        ttk.Label(toolbar, text='Speed (mm/s):').pack(side=tk.LEFT, padx=(6, 2))
        self._spin_speed = ttk.Spinbox(toolbar, from_=5.0, to=100.0, increment=5.0, width=5)
        self._spin_speed.set('40.0')
        self._spin_speed.pack(side=tk.LEFT, padx=2)

        self._spin_z.bind('<FocusOut>', lambda e: self._on_defaults_changed())
        self._spin_speed.bind('<FocusOut>', lambda e: self._on_defaults_changed())

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        self._deadzone_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text='Lock Deadzone (30-270mm)', variable=self._deadzone_var, command=self._on_defaults_changed).pack(
            side=tk.LEFT, padx=3
        )

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Button(toolbar, text='Undo', width=5, command=self._service.get_plan().undo).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text='Redo', width=5, command=self._service.get_plan().redo).pack(side=tk.LEFT, padx=2)

        self._lbl_cursor = ttk.Label(toolbar, text='Cursor: X=  0.0 mm | Y=  0.0 mm | R=  0.0 mm | Zoom: 100%', font=('DejaVu Sans Mono', 9))
        self._lbl_cursor.pack(side=tk.RIGHT, padx=8)

    def _create_main_content(self) -> None:
        '''
            Builds split view layout with Canvas on left, Table & Controls on right.

            :exceptions: None.
        '''
        main_paned = ttk.PanedWindow(self._root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=3)

        settings = CanvasSettingsDTO(default_z=20.0, default_speed=40.0, enforce_deadzone=True)
        self._canvas = TrajectoryCanvas(
            left_frame,
            plan=self._service.get_plan(),
            validator=self._service.get_validator(),
            settings=settings
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.set_hover_label(self._lbl_cursor)

        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        right_paned = ttk.PanedWindow(right_frame, orient=tk.VERTICAL)
        right_paned.pack(fill=tk.BOTH, expand=True)

        table_group = ttk.LabelFrame(right_paned, text=' [ Trajectory Waypoints ] ', padding=6)
        right_paned.add(table_group, weight=1)

        self._table = TrajectoryTable(table_group, plan=self._service.get_plan())
        self._table.pack(fill=tk.BOTH, expand=True)

        edit_strip = ttk.Frame(table_group, padding=3)
        edit_strip.pack(fill=tk.X, pady=(4, 0))

        ttk.Label(edit_strip, text='X:').pack(side=tk.LEFT)
        self._entry_x = ttk.Entry(edit_strip, width=6)
        self._entry_x.pack(side=tk.LEFT, padx=2)

        ttk.Label(edit_strip, text='Y:').pack(side=tk.LEFT, padx=(4, 0))
        self._entry_y = ttk.Entry(edit_strip, width=6)
        self._entry_y.pack(side=tk.LEFT, padx=2)

        ttk.Label(edit_strip, text='Z:').pack(side=tk.LEFT, padx=(4, 0))
        self._entry_z = ttk.Entry(edit_strip, width=5)
        self._entry_z.pack(side=tk.LEFT, padx=2)

        ttk.Label(edit_strip, text='Phi:').pack(side=tk.LEFT, padx=(4, 0))
        self._entry_phi = ttk.Entry(edit_strip, width=5)
        self._entry_phi.pack(side=tk.LEFT, padx=2)

        ttk.Label(edit_strip, text='Spd:').pack(side=tk.LEFT, padx=(4, 0))
        self._entry_spd = ttk.Entry(edit_strip, width=5)
        self._entry_spd.pack(side=tk.LEFT, padx=2)

        ttk.Button(edit_strip, text='Apply', command=self._on_apply_point_edit).pack(side=tk.LEFT, padx=4)
        ttk.Button(edit_strip, text='Delete', command=self._table.delete_selected).pack(side=tk.LEFT, padx=2)

        ctl_frame = ttk.Frame(right_paned)
        right_paned.add(ctl_frame, weight=1)
        self._controls = ControlsPanel(ctl_frame, service=self._service)
        self._controls.pack(fill=tk.BOTH, expand=True)

    def _on_defaults_changed(self) -> None:
        '''
            Applies updated defaults from toolbar to canvas.

            :exceptions: None.
        '''
        try:
            dz: float = float(self._spin_z.get())
            dsp: float = float(self._spin_speed.get())
            enforce: bool = self._deadzone_var.get()
            self._canvas.update_settings(CanvasSettingsDTO(default_z=dz, default_speed=dsp, enforce_deadzone=enforce))
        except ValueError:
            pass

    def _on_apply_point_edit(self) -> None:
        '''
            Applies coordinate edits to selected waypoint.

            :exceptions: None.
        '''
        plan = self._service.get_plan()
        idx: int = plan.selected_index
        if 0 <= idx < plan.count:
            try:
                cur = plan.waypoints[idx]
                updated = Waypoint(
                    x=float(self._entry_x.get()),
                    y=float(self._entry_y.get()),
                    z=float(self._entry_z.get()),
                    phi=float(self._entry_phi.get()),
                    speed=float(self._entry_spd.get()),
                    name=cur.name
                )
                plan.update_point(idx, updated)
            except ValueError:
                messagebox.showerror('Input Error', 'Invalid numeric values.')
