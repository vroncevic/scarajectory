# -*- coding: UTF-8 -*-

'''
Module
    menu_hotkey_binder.py
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
    Dedicated hotkey binder component for application shortcut key bindings.
'''

from __future__ import annotations

from tkinter import Tk

from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.menu.iapp_menu_bar import IAppMenuBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MenuHotkeyBinder:
    '''
        Binds application-wide keyboard shortcuts to Tkinter root window.

        It defines:

            :methods:
                | bind_hotkeys - Registers shortcut key combinations to actions.
    '''

    def bind_hotkeys(
        self,
        root: Tk,
        menu_bar: IAppMenuBar,
        mutation: IPlanBulkMutator,
        history: ITrajectoryHistory,
        table: ITable,
    ) -> None:
        '''
            Binds keyboard shortcuts to window.

            :param root: Application root Tk window.
            :param menu_bar: IAppMenuBar interface instance.
            :param mutation: IPlanBulkMutator domain mutation instance.
            :param history: ITrajectoryHistory domain history instance.
            :param table: ITable table interface instance.
            :exceptions: None.
        '''
        root.bind('<Control-n>', lambda e: mutation.clear())
        root.bind('<Control-o>', lambda e: menu_bar.open_json_dialog())
        root.bind('<Control-s>', lambda e: menu_bar.save_json_dialog())
        root.bind('<Control-z>', lambda e: history.undo())
        root.bind('<Control-y>', lambda e: history.redo())
        root.bind('<Delete>', lambda e: table.delete_selected())
        root.bind('<BackSpace>', lambda e: table.delete_selected())
