# -*- coding: UTF-8 -*-

'''
Module
    toolbar.py
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
    Top toolbar housing CAD drawing tools, zoom controls, plan undo/redo and default settings.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Final

from scarajectory.core.model.canvas_tool_mode import CanvasToolMode
from scarajectory.core.model.canvas_settings_dto import CanvasSettingsDTO
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.infrastructure.gui.icanvas import ICanvas

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Toolbar(ttk.Frame):
    '''
        Application toolbar for mode selection, CAD actions, and kinematic defaults.

        It defines:

            :attributes:
                | _canvas - Active CAD canvas interface.
                | _plan - Active trajectory plan domain model.
                | _tool_var - Active CAD tool mode variable.
                | _spin_z - Default waypoint Z elevation spinbox.
                | _spin_speed - Default waypoint feedrate spinbox.
                | _deadzone_var - Deadzone kinematic boundary lock checkbox variable.
                | _lbl_cursor - Dynamic cursor coordinate and zoom readout label.
            :methods:
                | __init__ - Initializes toolbar widgets.
                | set_deadzone - Sets deadzone enforcement checkbox state.
                | get_cursor_label - Returns cursor info label widget.
    '''

    _canvas: Final[ICanvas]
    _plan: Final[ITrajectoryPlan]
    _tool_var: tk.StringVar
    _spin_z: ttk.Spinbox
    _spin_speed: ttk.Spinbox
    _deadzone_var: tk.BooleanVar
    _lbl_cursor: ttk.Label

    def __init__(
        self,
        parent: tk.Widget,
        canvas: ICanvas,
        plan: ITrajectoryPlan,
        **kwargs: object
    ) -> None:
        '''
            Initializes toolbar widgets.

            :param parent: Parent container widget.
            :param canvas: ICanvas interface instance.
            :param plan: ITrajectoryPlan instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=(8, 6), **kwargs)  # type: ignore[arg-type]
        self._canvas = canvas
        self._plan = plan
        self._build_layout()

    def _build_layout(self) -> None:
        '''
            Constructs CAD tools, zoom buttons, parameter inputs and cursor monitor.

            :exceptions: None.
        '''
        ttk.Label(self, text='Tool:', style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 4))
        self._tool_var = tk.StringVar(value='POINT')
        tools = [
            ('Point', 'POINT', CanvasToolMode.POINT),
            ('Line', 'LINE', CanvasToolMode.LINE),
            ('Select/Move', 'SELECT', CanvasToolMode.SELECT),
            ('Circle', 'CIRCLE', CanvasToolMode.CIRCLE),
            ('Rectangle', 'RECTANGLE', CanvasToolMode.RECTANGLE),
            ('Freehand', 'FREEHAND', CanvasToolMode.FREEHAND)
        ]
        for text, val, mode in tools:
            btn = ttk.Radiobutton(
                self,
                text=text,
                value=val,
                variable=self._tool_var,
                command=lambda m=mode: self._canvas.set_tool_mode(m)
            )
            btn.pack(side=tk.LEFT, padx=2)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Button(self, text='[ + ]', width=4, command=self._canvas.zoom_in).pack(side=tk.LEFT, padx=1)
        ttk.Button(self, text='[ - ]', width=4, command=self._canvas.zoom_out).pack(side=tk.LEFT, padx=1)
        ttk.Button(self, text='Fit', width=4, command=self._canvas.fit_reach_view).pack(side=tk.LEFT, padx=1)
        ttk.Button(self, text='100%', width=5, command=self._canvas.reset_view).pack(side=tk.LEFT, padx=1)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Label(self, text='Z (mm):').pack(side=tk.LEFT, padx=2)
        self._spin_z = ttk.Spinbox(self, from_=0.0, to=100.0, increment=5.0, width=5)
        self._spin_z.set('20.0')
        self._spin_z.pack(side=tk.LEFT, padx=2)

        ttk.Label(self, text='Speed (mm/s):').pack(side=tk.LEFT, padx=(6, 2))
        self._spin_speed = ttk.Spinbox(self, from_=5.0, to=100.0, increment=5.0, width=5)
        self._spin_speed.set('40.0')
        self._spin_speed.pack(side=tk.LEFT, padx=2)

        self._spin_z.bind('<FocusOut>', lambda e: self._on_defaults_changed())
        self._spin_speed.bind('<FocusOut>', lambda e: self._on_defaults_changed())

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        self._deadzone_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self,
            text='Enforce Reach Limits (30-270mm)',
            variable=self._deadzone_var,
            command=self._on_defaults_changed
        ).pack(side=tk.LEFT, padx=3)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Button(self, text='Undo', width=5, command=self._plan.undo).pack(side=tk.LEFT, padx=2)
        ttk.Button(self, text='Redo', width=5, command=self._plan.redo).pack(side=tk.LEFT, padx=2)

        self._lbl_cursor = ttk.Label(
            self,
            text='Cursor: X=  0.0 mm | Y=  0.0 mm | R=  0.0 mm | Zoom: 100%',
            font=('DejaVu Sans Mono', 9)
        )
        self._lbl_cursor.pack(side=tk.RIGHT, padx=8)
        self._canvas.set_hover_label(self._lbl_cursor)

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

    def set_deadzone(self, enabled: bool) -> None:
        '''
            Sets deadzone enforcement state.

            :param enabled: True to enforce deadzone, False to disable.
            :exceptions: None.
        '''
        self._deadzone_var.set(enabled)
        self._on_defaults_changed()

    def get_cursor_label(self) -> ttk.Label:
        '''
            Returns cursor monitor label widget.

            :return: ttk.Label instance.
            :exceptions: None.
        '''
        return self._lbl_cursor
