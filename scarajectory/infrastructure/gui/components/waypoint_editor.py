# -*- coding: UTF-8 -*-

'''
Module
    waypoint_editor.py
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
    Waypoint editor component wrapping tabular view and numeric coordinate editing strip.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Final

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.infrastructure.gui.table import TrajectoryTable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditor(ttk.LabelFrame):
    '''
        Waypoint table and inline coordinate editor panel.

        It defines:

            :attributes:
                | _plan - ITrajectoryPlan instance.
                | _table - Tabular waypoint view widget.
                | _entry_x - Entry field for X coordinate.
                | _entry_y - Entry field for Y coordinate.
                | _entry_z - Entry field for Z coordinate.
                | _entry_phi - Entry field for Phi angle.
                | _entry_spd - Entry field for Speed.
            :methods:
                | __init__ - Initializes waypoint editor container and widgets.
                | delete_selected - Deletes currently selected waypoint.
                | on_trajectory_updated - Populates coordinate entries on plan changes.
                | on_point_selected - Populates coordinate entries on waypoint selection.
    '''

    _plan: ITrajectoryPlan
    _table: TrajectoryTable
    _entry_x: ttk.Entry
    _entry_y: ttk.Entry
    _entry_z: ttk.Entry
    _entry_phi: ttk.Entry
    _entry_spd: ttk.Entry

    def __init__(self, parent: tk.Widget, plan: ITrajectoryPlan, **kwargs: object) -> None:
        '''
            Initializes waypoint editor container and widgets.

            :param parent: Parent Tk widget.
            :param plan: ITrajectoryPlan instance.
            :exceptions: None.
        '''
        super().__init__(parent, text=' [ Trajectory Waypoints ] ', padding=6, **kwargs)
        self._plan: Final[ITrajectoryPlan] = plan
        self._plan.add_observer(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        '''
            Builds table and bottom coordinate entry strip.

            :exceptions: None.
        '''
        self._table = TrajectoryTable(self, plan=self._plan)
        self._table.pack(fill=tk.BOTH, expand=True)

        edit_strip = ttk.Frame(self, padding=3)
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
        ttk.Button(edit_strip, text='Delete', command=self.delete_selected).pack(side=tk.LEFT, padx=2)

    def delete_selected(self) -> None:
        '''
            Deletes currently selected waypoint.

            :exceptions: None.
        '''
        self._table.delete_selected()

    def _on_apply_point_edit(self) -> None:
        '''
            Applies coordinate edits to selected waypoint.

            :exceptions: None.
        '''
        idx: int = self._plan.selected_index
        if 0 <= idx < self._plan.count:
            try:
                cur = self._plan.waypoints[idx]
                updated = Waypoint(
                    x=float(self._entry_x.get()),
                    y=float(self._entry_y.get()),
                    z=float(self._entry_z.get()),
                    phi=float(self._entry_phi.get()),
                    speed=float(self._entry_spd.get()),
                    name=cur.name
                )
                self._plan.update_point(idx, updated)
            except ValueError:
                messagebox.showerror('Input Error', 'Invalid numeric values.')

    def on_trajectory_updated(self) -> None:
        '''
            Populates coordinate entries on plan changes.

            :exceptions: None.
        '''
        idx: int = self._plan.selected_index
        if 0 <= idx < self._plan.count:
            pt = self._plan.waypoints[idx]
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
            Populates coordinate entries on waypoint selection.

            :param index: Selected index.
            :exceptions: None.
        '''
        _ = index
        self.on_trajectory_updated()
