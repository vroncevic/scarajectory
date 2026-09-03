# -*- coding: UTF-8 -*-

'''
Module
    table.py
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
    Tabular waypoint viewer and numerical editor widget.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Final

from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryTable(ttk.Frame):
    '''
        Tabular display of waypoints with selection synchronization and inspection.

        It defines:

            :attributes:
                | _plan - ITrajectoryPlan instance.
                | _tree - Treeview table widget.
            :methods:
                | __init__ - Initializes table view widget.
                | refresh_table - Refreshes table rows from active plan.
                | delete_selected - Deletes the currently selected waypoint.
                | on_trajectory_updated - Refreshes table data on plan change.
                | on_point_selected - Synchronizes row selection.
    '''

    _plan: ITrajectoryPlan
    _tree: ttk.Treeview

    def __init__(self, parent: tk.Widget, plan: ITrajectoryPlan, **kwargs: object) -> None:
        '''
            Initializes table view widget.

            :param parent: Parent container widget.
            :param plan: ITrajectoryPlan instance.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)
        self._plan: Final[ITrajectoryPlan] = plan
        self._plan.add_observer(self)
        self._create_widgets()

    def _create_widgets(self) -> None:
        '''
            Builds treeview table and scrollbars.

            :exceptions: None.
        '''
        cols: tuple[str, ...] = ('idx', 'x', 'y', 'z', 'phi', 'speed', 'reach')
        self._tree = ttk.Treeview(self, columns=cols, show='headings', height=10, selectmode='browse')

        self._tree.heading('idx', text='#')
        self._tree.heading('x', text='X (mm)')
        self._tree.heading('y', text='Y (mm)')
        self._tree.heading('z', text='Z (mm)')
        self._tree.heading('phi', text='Phi (deg)')
        self._tree.heading('speed', text='Speed (mm/s)')
        self._tree.heading('reach', text='Radius (mm)')

        self._tree.column('idx', width=35, anchor='center')
        self._tree.column('x', width=65, anchor='e')
        self._tree.column('y', width=65, anchor='e')
        self._tree.column('z', width=60, anchor='e')
        self._tree.column('phi', width=65, anchor='e')
        self._tree.column('speed', width=85, anchor='e')
        self._tree.column('reach', width=75, anchor='e')

        scrollbar: ttk.Scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree.bind('<<TreeviewSelect>>', self._on_tree_select)

    def delete_selected(self) -> None:
        '''
            Deletes the currently selected waypoint.

            :exceptions: None.
        '''
        idx: int = self._plan.selected_index
        if 0 <= idx < self._plan.count:
            self._plan.remove_point(idx)

    def refresh_table(self) -> None:
        '''
            Refreshes table rows from active plan.

            :exceptions: None.
        '''
        for item in self._tree.get_children():
            self._tree.delete(item)

        for i, pt in enumerate(self._plan.waypoints):
            r: float = pt.radial_distance
            item_id: str = self._tree.insert(
                '', tk.END,
                values=(
                    f'{i+1}',
                    f'{pt.x:.1f}',
                    f'{pt.y:.1f}',
                    f'{pt.z:.1f}',
                    f'{pt.phi:.2f}',
                    f'{pt.speed:.1f}',
                    f'{r:.1f}'
                )
            )
            if i == self._plan.selected_index:
                self._tree.selection_set(item_id)
                self._tree.see(item_id)

    def _on_tree_select(self, event: tk.Event) -> None:
        '''
            Handles row selection in table.

            :param event: Tk event.
            :exceptions: None.
        '''
        _ = event
        selected = self._tree.selection()

        if selected:
            item_id: str = selected[0]
            idx_str: str = str(self._tree.item(item_id, 'values')[0])

            try:
                idx: int = int(idx_str) - 1
                self._plan.set_selected_index(idx)
            except ValueError:
                pass

    def on_trajectory_updated(self) -> None:
        '''
            Refreshes table data on plan change.

            :exceptions: None.
        '''
        self.refresh_table()

    def on_point_selected(self, index: int) -> None:
        '''
            Synchronizes row selection with canvas selection.

            :param index: Selected index.
            :exceptions: None.
        '''
        children = self._tree.get_children()

        if 0 <= index < len(children):
            target = children[index]

            if self._tree.selection() != (target,):
                self._tree.selection_set(target)
                self._tree.see(target)
        elif index == -1:
            self._tree.selection_remove(self._tree.selection())
