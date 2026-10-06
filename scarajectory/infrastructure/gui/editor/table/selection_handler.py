# -*- coding: UTF-8 -*-

'''
Module
    selection_handler.py
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
    Selection event handler synchronizing Treeview row selection with plan coordinator.
'''

from __future__ import annotations

from tkinter.ttk import Treeview

from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TableSelectionHandler:
    '''
        Handles row selection on Treeview widget and updates plan selection coordinator.

        It defines:

            :methods:
                | handle_selection - Processes row selection event from Treeview widget.
                | get_version - Returns handler version string.
    '''

    @classmethod
    def handle_selection(
        cls,
        tree: Treeview,
        selection: IPlanSelectionCoordinator
    ) -> None:
        '''
            Processes row selection event from Treeview widget.

            :param tree: Target Treeview widget.
            :param selection: Injected IPlanSelectionCoordinator instance.
            :exceptions: None.
        '''
        selected = tree.selection()

        if selected:
            item_id: str = selected[0]
            values = tree.item(item_id, 'values')

            if not values:
                return

            try:
                idx: int = int(str(values[0])) - 1

                if idx != selection.selected_index:
                    selection.set_selected_index(idx)

            except (ValueError, IndexError):
                pass

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns handler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
