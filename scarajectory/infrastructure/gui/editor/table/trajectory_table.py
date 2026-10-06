# -*- coding: UTF-8 -*-

'''
Module
    trajectory_table.py
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

from math import hypot
from tkinter import BOTH, END, LEFT, RIGHT, VERTICAL, Widget, Y
from tkinter.ttk import Frame, Scrollbar, Treeview
from typing import Final

from scarajectory.core.service.trajectory.plan.mutation.iplan_point_mutator import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.selection_handler import TableSelectionHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryTable(Frame):
    '''
        Tabular display of waypoints with selection synchronization and inspection.

        It defines:

            :attributes:
                | _store - Injected waypoint query collaborator.
                | _selection - Injected selection coordinator collaborator.
                | _mutation - Injected plan mutation service collaborator.
                | _dispatcher - Injected observer dispatcher collaborator.
                | _tree - Treeview table widget.
                | _is_updating - Guard flag preventing recursive selection feedback during refresh.
            :methods:
                | __init__ - Initializes table view widget.
                | create_widgets - Builds treeview table and scrollbars.
                | delete_selected - Deletes the currently selected waypoint.
                | refresh_table - Refreshes table rows from active plan.
                | on_trajectory_updated - Refreshes table data on plan change.
                | on_point_selected - Synchronizes row selection.
    '''

    _store: IWaypointStore
    _selection: IPlanSelectionCoordinator
    _mutation: IPlanPointMutator
    _dispatcher: IPlanObserverDispatcher
    _tree: Treeview
    _is_updating: bool

    def __init__(
        self,
        parent: Widget,
        bundle: TableBundle,
    ) -> None:
        '''
            Initializes table view widget.

            :param parent: Parent container widget.
            :param bundle: Injected TableBundle instance.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._is_updating = False
        self._store: Final[IWaypointStore] = bundle.store
        self._selection: Final[IPlanSelectionCoordinator] = bundle.selection
        self._mutation: Final[IPlanPointMutator] = bundle.mutation
        self._dispatcher: Final[IPlanObserverDispatcher] = bundle.dispatcher
        self._dispatcher.add_observer(self)
        self.create_widgets()

    def create_widgets(self) -> None:
        '''
            Builds treeview table and scrollbars.

            :exceptions: None.
        '''
        cols: tuple[str, ...] = ('idx', 'x', 'y', 'z', 'phi', 'speed', 'reach')
        self._tree = Treeview(
            self, columns=cols, show='headings', height=10, selectmode='browse'
        )

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

        scrollbar: Scrollbar = Scrollbar(
            self, orient=VERTICAL, command=self._tree.yview
        )
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self._tree.bind(
            '<<TreeviewSelect>>',
            lambda _e: (
                None
                if self._is_updating
                else TableSelectionHandler.handle_selection(
                    self._tree, self._selection
                )
            )
        )

    def delete_selected(self) -> None:
        '''
            Deletes the currently selected waypoint.

            :exceptions: None.
        '''
        idx: int = self._selection.selected_index

        if 0 <= idx < self._store.count:
            self._mutation.remove_point(idx)

    def refresh_table(self) -> None:
        '''
            Refreshes table rows from active plan.

            :exceptions: None.
        '''
        self._is_updating = True
        try:
            for item in self._tree.get_children():
                self._tree.delete(item)

            for i, pt in enumerate(self._store.waypoints):
                r: float = hypot(pt.x, pt.y)
                item_id: str = self._tree.insert(
                    '', END,
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

                if i == self._selection.selected_index:
                    self._tree.selection_set(item_id)
                    self._tree.see(item_id)
        finally:
            self._is_updating = False

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
        self._is_updating = True
        try:
            children = self._tree.get_children()

            if 0 <= index < len(children):
                target = children[index]

                if self._tree.selection() != (target,):
                    self._tree.selection_set(target)
                    self._tree.see(target)

            elif index == -1:
                self._tree.selection_remove(self._tree.selection())

        finally:
            self._is_updating = False
