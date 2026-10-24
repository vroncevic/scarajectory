# -*- coding: UTF-8 -*-

'''
Module
    layout.py
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
from typing import ClassVar

from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.infrastructure.gui.menu.imenu_bar import IAppMenuBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MenuLayoutBuilder:
    '''
        Constructs and mounts the top application menu bar widget hierarchy.

        It defines:

            :constants:
                | COLOR_BG - Background hex color code.
                | COLOR_FG - Foreground hex color code.
                | COLOR_ACTIVE_BG - Active background hex color code.
                | COLOR_ACTIVE_FG - Active foreground hex color code.
                | TEAROFF_DISABLED - Integer flag disabling menu tearoff.
            :methods:
                | build_menu - Constructs File, Edit, View cascades and menu.
                | get_version - Returns the component version string.
    '''

    COLOR_BG: ClassVar[str] = '#21252b'
    COLOR_FG: ClassVar[str] = '#abb2bf'
    COLOR_ACTIVE_BG: ClassVar[str] = '#61afef'
    COLOR_ACTIVE_FG: ClassVar[str] = '#ffffff'
    TEAROFF_DISABLED: ClassVar[int] = 0

    def build_menu(
        self,
        root: Tk,
        menu_bar: IAppMenuBar,
        bundle: MenuBundle,
    ) -> None:
        '''
            Constructs File, Edit, View cascades and sets root menu.

            :param root: Application root Tk window.
            :param menu_bar: IAppMenuBar interface instance.
            :param bundle: Injected MenuBundle collaborator instance.
            :exceptions: None.
        '''
        menubar = Menu(
            root,
            bg=self.COLOR_BG,
            fg=self.COLOR_FG,
            activebackground=self.COLOR_ACTIVE_BG,
            activeforeground=self.COLOR_ACTIVE_FG,
        )

        file_m = Menu(
            menubar,
            tearoff=self.TEAROFF_DISABLED,
            bg=self.COLOR_BG,
            fg=self.COLOR_FG,
        )
        file_m.add_command(label='New (Ctrl+N)', command=bundle.mutation.clear)
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

        edit_m = Menu(
            menubar,
            tearoff=self.TEAROFF_DISABLED,
            bg=self.COLOR_BG,
            fg=self.COLOR_FG,
        )
        edit_m.add_command(label='Undo (Ctrl+Z)', command=bundle.history.undo)
        edit_m.add_command(label='Redo (Ctrl+Y)', command=bundle.history.redo)
        edit_m.add_separator()
        edit_m.add_command(label='Clear All', command=bundle.mutation.clear)
        menubar.add_cascade(label='Edit', menu=edit_m)

        view_m = Menu(
            menubar,
            tearoff=self.TEAROFF_DISABLED,
            bg=self.COLOR_BG,
            fg=self.COLOR_FG,
        )
        view_m.add_command(label='Zoom In (+)', command=bundle.navigator.zoom_in)
        view_m.add_command(label='Zoom Out (-)', command=bundle.navigator.zoom_out)
        view_m.add_command(
            label='Fit Workspace', command=bundle.navigator.fit_reach_view
        )
        view_m.add_command(label='Reset 100%', command=bundle.navigator.reset_view)
        menubar.add_cascade(label='View', menu=view_m)

        root.config(menu=menubar)

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
