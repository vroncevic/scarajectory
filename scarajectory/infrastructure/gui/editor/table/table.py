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

from math import hypot
from tkinter import END, HORIZONTAL, VERTICAL, Widget
from tkinter.ttk import Frame, Scrollbar, Treeview
from typing import ClassVar, Final

from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.resize.ihandler import ITableResizeHandler
from scarajectory.infrastructure.gui.editor.table.selection.ihandler import ITableSelectionHandler

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

            :constants:
                | COLUMNS - Tuple of column identifiers for treeview table.
                | SHOW_MODE - Display mode for treeview headings.
                | SELECT_MODE - Row selection mode for treeview widget.
                | TABLE_HEIGHT - Visible row count for treeview table widget.
                | EVENT_SELECT - Virtual event triggered on treeview row selection.
                | EVENT_CONFIGURE - Tkinter event triggered on widget geometry change.
                | FMT_COORD - Number formatting template for Cartesian coordinates and reach.
                | FMT_PHI - Number formatting template for tool rotation angle.
                | FMT_SPEED - Number formatting template for waypoint speed.
            :attributes:
                | _bundle - Injected waypoint table dependencies collaborator bundle.
                | _resize_handler - Injected table resize event handler collaborator.
                | _selection_handler - Injected row selection event handler collaborator.
                | _tree - Treeview table widget.
                | _is_updating - Guard flag preventing recursive selection feedback during refresh.
            :methods:
                | __init__ - Initializes table view widget and builds treeview subcomponents.
                | delete_selected - Deletes the currently selected waypoint.
                | refresh_table - Refreshes table rows from active plan.
                | on_trajectory_updated - Refreshes table data on plan change.
                | get_version - Returns component version string.
    '''

    COLUMNS: ClassVar[tuple[str, ...]] = (
        'idx', 'x', 'y', 'z', 'phi', 'speed', 'reach'
    )
    SHOW_MODE: ClassVar[str] = 'headings'
    SELECT_MODE: ClassVar[str] = 'browse'
    TABLE_HEIGHT: ClassVar[int] = 10

    EVENT_SELECT: ClassVar[str] = '<<TreeviewSelect>>'
    EVENT_CONFIGURE: ClassVar[str] = '<Configure>'

    FMT_COORD: ClassVar[str] = '{:.1f}'
    FMT_PHI: ClassVar[str] = '{:.2f}'
    FMT_SPEED: ClassVar[str] = '{:.1f}'

    _bundle: TableBundle
    _resize_handler: ITableResizeHandler
    _selection_handler: ITableSelectionHandler
    _tree: Treeview
    _is_updating: bool

    def __init__(
        self,
        parent: Widget,
        *,
        bundle: TableBundle,
        resize_handler: ITableResizeHandler,
        selection_handler: ITableSelectionHandler,
    ) -> None:
        '''
            Initializes table view widget and builds treeview subcomponents.

            :param parent: Parent container widget.
            :param bundle: Injected TableBundle instance.
            :param resize_handler: Injected ITableResizeHandler instance.
            :param selection_handler: Injected ITableSelectionHandler instance.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._is_updating = False
        self._bundle: Final[TableBundle] = bundle
        self._resize_handler: Final[ITableResizeHandler] = resize_handler
        self._selection_handler: Final[ITableSelectionHandler] = (
            selection_handler
        )
        self._bundle.dispatcher.add_observer(self)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._tree = Treeview(
            self,
            columns=self.COLUMNS,
            show=self.SHOW_MODE,
            height=self.TABLE_HEIGHT,
            selectmode=self.SELECT_MODE,
        )

        self._tree.heading('idx', text='#')
        self._tree.heading('x', text='X (mm)')
        self._tree.heading('y', text='Y (mm)')
        self._tree.heading('z', text='Z (mm)')
        self._tree.heading('phi', text='Phi (deg)')
        self._tree.heading('speed', text='Speed (mm/s)')
        self._tree.heading('reach', text='Radius (mm)')

        self._tree.column('idx', width=35, minwidth=30, stretch=False, anchor='center')
        self._tree.column('x', width=65, minwidth=50, stretch=False, anchor='e')
        self._tree.column('y', width=65, minwidth=50, stretch=False, anchor='e')
        self._tree.column('z', width=60, minwidth=45, stretch=False, anchor='e')
        self._tree.column('phi', width=65, minwidth=50, stretch=False, anchor='e')
        self._tree.column('speed', width=85, minwidth=65, stretch=False, anchor='e')
        self._tree.column('reach', width=75, minwidth=60, stretch=False, anchor='e')

        v_scroll: Scrollbar = Scrollbar(
            self, orient=VERTICAL, command=self._tree.yview
        )
        h_scroll: Scrollbar = Scrollbar(
            self, orient=HORIZONTAL, command=self._tree.xview
        )
        self._tree.configure(
            yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set
        )

        self._tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        self._tree.bind(
            self.EVENT_SELECT,
            lambda _e: (
                None
                if self._is_updating
                else self._selection_handler.handle_selection(
                    self._tree, self._bundle.selection
                )
            ),
        )
        self.bind(
            self.EVENT_CONFIGURE,
            lambda event: self._resize_handler.handle_resize(
                self._tree, event
            ),
        )

    def delete_selected(self) -> None:
        '''
            Deletes the currently selected waypoint.

            :exceptions: None.
        '''
        idx: int = self._bundle.selection.selected_index

        if 0 <= idx < self._bundle.store.count:
            self._bundle.mutation.remove_point(idx)

    def refresh_table(self) -> None:
        '''
            Refreshes table rows from active plan.

            :exceptions: None.
        '''
        self._is_updating = True

        try:
            for item in self._tree.get_children():
                self._tree.delete(item)

            for i, pt in enumerate(self._bundle.store.waypoints):
                r: float = hypot(pt.x, pt.y)
                item_id: str = self._tree.insert(
                    '', END,
                    values=(
                        f'{i+1}',
                        self.FMT_COORD.format(pt.x),
                        self.FMT_COORD.format(pt.y),
                        self.FMT_COORD.format(pt.z),
                        self.FMT_PHI.format(pt.phi),
                        self.FMT_SPEED.format(pt.speed),
                        self.FMT_COORD.format(r),
                    ),
                )

                if i == self._bundle.selection.selected_index:
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

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
