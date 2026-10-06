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

from tkinter import BOTH, END, LEFT, X, Widget
from tkinter.ttk import Button, Entry, Frame, Label, LabelFrame
from typing import Final

from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.trajectory_table import TrajectoryTable
from scarajectory.infrastructure.gui.editor.waypoint_coordinate_inputs import WaypointCoordinateInputs
from scarajectory.infrastructure.gui.editor.waypoint_edit_applier import WaypointEditApplier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditor(LabelFrame):
    '''
        Waypoint table and inline coordinate editor panel.

        It defines:

            :attributes:
                | _bundle - Injected table collaborator bundle.
                | _table - Tabular waypoint view widget.
                | _entry_x - Entry field for X coordinate.
                | _entry_y - Entry field for Y coordinate.
                | _entry_z - Entry field for Z coordinate.
                | _entry_phi - Entry field for Phi angle.
                | _entry_spd - Entry field for Speed.
            :methods:
                | __init__ - Initializes waypoint editor container and widgets.
                | create_widgets - Builds table and bottom coordinate entry strip.
                | apply_point_edit - Applies coordinate edits to selected waypoint.
                | delete_selected - Deletes currently selected waypoint.
                | on_trajectory_updated - Populates coordinate entries on plan changes.
                | on_point_selected - Populates coordinate entries on waypoint selection.
    '''

    _bundle: TableBundle
    _table: TrajectoryTable
    _entry_x: Entry
    _entry_y: Entry
    _entry_z: Entry
    _entry_phi: Entry
    _entry_spd: Entry

    def __init__(
        self,
        parent: Widget,
        bundle: TableBundle,
    ) -> None:
        '''
            Initializes waypoint editor container and widgets.

            :param parent: Parent Tk widget.
            :param bundle: Injected TableBundle instance.
            :exceptions: None.
        '''
        super().__init__(
            parent, text=' [ Trajectory Waypoints ] ', padding=6
        )
        self._bundle: Final[TableBundle] = bundle
        self._bundle.dispatcher.add_observer(self)
        self.create_widgets()

    def create_widgets(self) -> None:
        '''
            Builds table and bottom coordinate entry strip.

            :exceptions: None.
        '''
        self._table = TrajectoryTable(self, bundle=self._bundle)
        self._table.pack(fill=BOTH, expand=True)

        edit_strip = Frame(self, padding=3)
        edit_strip.pack(fill=X, pady=(4, 0))

        Label(edit_strip, text='X:').pack(side=LEFT)
        self._entry_x = Entry(edit_strip, width=6)
        self._entry_x.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Y:').pack(side=LEFT, padx=(4, 0))
        self._entry_y = Entry(edit_strip, width=6)
        self._entry_y.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Z:').pack(side=LEFT, padx=(4, 0))
        self._entry_z = Entry(edit_strip, width=5)
        self._entry_z.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Phi:').pack(side=LEFT, padx=(4, 0))
        self._entry_phi = Entry(edit_strip, width=5)
        self._entry_phi.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Spd:').pack(side=LEFT, padx=(4, 0))
        self._entry_spd = Entry(edit_strip, width=5)
        self._entry_spd.pack(side=LEFT, padx=2)

        Button(edit_strip, text='Apply', command=self.apply_point_edit).pack(side=LEFT, padx=4)
        Button(edit_strip, text='Delete', command=self.delete_selected).pack(side=LEFT, padx=2)

    def delete_selected(self) -> None:
        '''
            Deletes currently selected waypoint.

            :exceptions: None.
        '''
        self._table.delete_selected()

    def refresh_table(self) -> None:
        '''
            Refreshes table rows from active plan.

            :exceptions: None.
        '''
        self._table.refresh_table()

    def apply_point_edit(self) -> None:
        '''
            Applies coordinate edits to selected waypoint.

            :exceptions: None.
        '''
        inputs = WaypointCoordinateInputs(
            x=self._entry_x.get(),
            y=self._entry_y.get(),
            z=self._entry_z.get(),
            phi=self._entry_phi.get(),
            speed=self._entry_spd.get(),
        )
        WaypointEditApplier.apply_edit(inputs, self._bundle)

    def on_trajectory_updated(self) -> None:
        '''
            Populates coordinate entries on plan changes.

            :exceptions: None.
        '''
        idx: int = self._bundle.selection.selected_index

        if 0 <= idx < self._bundle.store.count:
            pt = self._bundle.store.waypoints[idx]

            for ent, val in (
                (self._entry_x, f'{pt.x:.2f}'),
                (self._entry_y, f'{pt.y:.2f}'),
                (self._entry_z, f'{pt.z:.2f}'),
                (self._entry_phi, f'{pt.phi:.2f}'),
                (self._entry_spd, f'{pt.speed:.1f}'),
            ):
                ent.delete(0, END)
                ent.insert(0, val)

    def on_point_selected(self, index: int) -> None:
        '''
            Populates coordinate entries on waypoint selection.

            :param index: Selected index.
            :exceptions: None.
        '''
        _ = index
        self.on_trajectory_updated()
