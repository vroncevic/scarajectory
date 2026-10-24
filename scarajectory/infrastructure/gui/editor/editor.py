# -*- coding: UTF-8 -*-

'''
Module
    editor.py
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
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.editor.applier.iapplier import IWaypointEditApplier
from scarajectory.infrastructure.gui.editor.applier.inputs import WaypointCoordinateInputs
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.factory import TrajectoryTableFactory
from scarajectory.infrastructure.gui.editor.table.table import TrajectoryTable

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

            :constants:
                | TITLE_TEXT - Container border title text.
                | PADDING_FRAME - Container frame padding in pixels.
                | PADDING_STRIP - Edit input strip padding in pixels.
                | WIDTH_LONG - Column character width for long numeric entries.
                | WIDTH_SHORT - Column character width for short numeric entries.
                | FMT_COORD - Number formatting template for Cartesian coordinates.
                | FMT_PHI - Number formatting template for tool rotation angle.
                | FMT_SPEED - Number formatting template for waypoint speed.
            :attributes:
                | _bundle - Injected table collaborator bundle.
                | _applier - Injected waypoint edit applier collaborator.
                | _table - Tabular waypoint view widget.
                | _entries - Tuple of coordinate entry widgets in order x, y, z, phi, spd.
            :methods:
                | __init__ - Initializes waypoint editor container and widgets.
                | delete_selected - Deletes currently selected waypoint.
                | refresh_table - Refreshes table rows from active plan.
                | apply_point_edit - Applies coordinate edits to selected waypoint.
                | on_trajectory_updated - Populates coordinate entries on plan changes.
                | get_version - Returns component version string.
    '''

    TITLE_TEXT: ClassVar[str] = ' [ Trajectory Waypoints ] '
    PADDING_FRAME: ClassVar[int] = 6
    PADDING_STRIP: ClassVar[int] = 3
    WIDTH_LONG: ClassVar[int] = 6
    WIDTH_SHORT: ClassVar[int] = 5
    FMT_COORD: ClassVar[str] = '{:.2f}'
    FMT_PHI: ClassVar[str] = '{:.2f}'
    FMT_SPEED: ClassVar[str] = '{:.1f}'

    _bundle: TableBundle
    _applier: IWaypointEditApplier
    _table: TrajectoryTable
    _entries: tuple[Entry, ...]

    def __init__(
        self,
        parent: Widget,
        *,
        bundle: TableBundle,
        table_factory: type[TrajectoryTableFactory],
        applier: IWaypointEditApplier,
    ) -> None:
        '''
            Initializes waypoint editor container and widgets.

            :param parent: Parent Tk widget.
            :param bundle: Injected TableBundle instance.
            :param table_factory: Factory type constructing TrajectoryTable.
            :param applier: Injected IWaypointEditApplier instance.
            :exceptions: None.
        '''
        super().__init__(
            parent, text=self.TITLE_TEXT, padding=self.PADDING_FRAME
        )
        self._bundle: Final[TableBundle] = bundle
        self._applier: Final[IWaypointEditApplier] = applier
        self._bundle.dispatcher.add_observer(self)

        self._table = table_factory.create(self, bundle=self._bundle)
        self._table.pack(fill=BOTH, expand=True)

        edit_strip = Frame(self, padding=self.PADDING_STRIP)
        edit_strip.pack(fill=X, pady=(4, 0))

        Label(edit_strip, text='X:').pack(side=LEFT)
        entry_x = Entry(edit_strip, width=self.WIDTH_LONG)
        entry_x.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Y:').pack(side=LEFT, padx=(4, 0))
        entry_y = Entry(edit_strip, width=self.WIDTH_LONG)
        entry_y.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Z:').pack(side=LEFT, padx=(4, 0))
        entry_z = Entry(edit_strip, width=self.WIDTH_SHORT)
        entry_z.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Phi:').pack(side=LEFT, padx=(4, 0))
        entry_phi = Entry(edit_strip, width=self.WIDTH_SHORT)
        entry_phi.pack(side=LEFT, padx=2)

        Label(edit_strip, text='Spd:').pack(side=LEFT, padx=(4, 0))
        entry_spd = Entry(edit_strip, width=self.WIDTH_SHORT)
        entry_spd.pack(side=LEFT, padx=2)

        self._entries = (entry_x, entry_y, entry_z, entry_phi, entry_spd)

        Button(
            edit_strip, text='Apply', command=self.apply_point_edit
        ).pack(side=LEFT, padx=4)
        Button(
            edit_strip, text='Delete', command=self.delete_selected
        ).pack(side=LEFT, padx=2)

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
            x=self._entries[0].get(),
            y=self._entries[1].get(),
            z=self._entries[2].get(),
            phi=self._entries[3].get(),
            speed=self._entries[4].get(),
        )
        self._applier.apply_edit(inputs=inputs, bundle=self._bundle)

    def on_trajectory_updated(self) -> None:
        '''
            Populates coordinate entries on plan changes.

            :exceptions: None.
        '''
        idx: int = self._bundle.selection.selected_index

        if 0 <= idx < self._bundle.store.count:
            pt = self._bundle.store.waypoints[idx]

            for ent, val in zip(
                self._entries,
                (
                    self.FMT_COORD.format(pt.x),
                    self.FMT_COORD.format(pt.y),
                    self.FMT_COORD.format(pt.z),
                    self.FMT_PHI.format(pt.phi),
                    self.FMT_SPEED.format(pt.speed),
                ),
            ):
                ent.delete(0, END)
                ent.insert(0, val)

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
