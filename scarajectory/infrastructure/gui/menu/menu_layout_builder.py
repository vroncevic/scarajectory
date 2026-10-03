# -*- coding: UTF-8 -*-

'''
Module
    menu_layout_builder.py
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
    Builder component for application top menu cascades (File, Edit, View).
'''

from __future__ import annotations

from tkinter import Menu, Tk

from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.core.service.trajectory.plan.mutation.iplan_mutation_service import IPlanMutationService
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.menu.iapp_menu_bar import IAppMenuBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MenuLayoutBuilder:
    '''
        Constructs and mounts the top application menu bar widget hierarchy.

        It defines:

            :methods:
                | build_menu - Constructs File, Edit, View cascades and menu.
    '''

    def build_menu(
        self,
        root: Tk,
        menu_bar: IAppMenuBar,
        mutation: IPlanMutationService,
        history: ITrajectoryHistory,
        navigator: ICanvasViewNavigator,
    ) -> None:
        '''
            Constructs File, Edit, View cascades and sets root menu.

            :param root: Application root Tk window.
            :param menu_bar: IAppMenuBar interface instance.
            :param mutation: IPlanMutationService domain mutation instance.
            :param history: ITrajectoryHistory domain history instance.
            :param navigator: ICanvasViewNavigator interface instance.
            :exceptions: None.
        '''
        menubar = Menu(
            root,
            bg='#21252b',
            fg='#abb2bf',
            activebackground='#61afef',
            activeforeground='#ffffff',
        )

        file_m = Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        file_m.add_command(label='New (Ctrl+N)', command=mutation.clear)
        file_m.add_command(
            label='Open JSON... (Ctrl+O)',
            command=menu_bar.open_json_dialog,
        )
        file_m.add_command(
            label='Save JSON... (Ctrl+S)',
            command=menu_bar.save_json_dialog,
        )
        file_m.add_separator()
        file_m.add_command(
            label='Import SCARA DSL (.scara)...',
            command=menu_bar.import_dsl_dialog,
        )
        file_m.add_command(
            label='Export SCARA DSL (.scara)...',
            command=menu_bar.export_dsl_dialog,
        )
        file_m.add_separator()
        file_m.add_command(label='Exit', command=root.quit)
        menubar.add_cascade(label='File', menu=file_m)

        edit_m = Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        edit_m.add_command(label='Undo (Ctrl+Z)', command=history.undo)
        edit_m.add_command(label='Redo (Ctrl+Y)', command=history.redo)
        edit_m.add_separator()
        edit_m.add_command(label='Clear All', command=mutation.clear)
        menubar.add_cascade(label='Edit', menu=edit_m)

        view_m = Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        view_m.add_command(label='Zoom In (+)', command=navigator.zoom_in)
        view_m.add_command(label='Zoom Out (-)', command=navigator.zoom_out)
        view_m.add_command(
            label='Fit Workspace', command=navigator.fit_reach_view
        )
        view_m.add_command(label='Reset 100%', command=navigator.reset_view)
        menubar.add_cascade(label='View', menu=view_m)

        root.config(menu=menubar)
