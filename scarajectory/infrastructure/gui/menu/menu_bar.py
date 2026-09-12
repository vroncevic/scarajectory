# -*- coding: UTF-8 -*-

'''
Module
    menu_bar.py
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
    Top application menu bar constructing File, Edit, View menus and hotkeys.
'''

from __future__ import annotations

from tkinter import Menu, Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo
from typing import Final

from scarajectory.core.service.iservice import IService
from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.editor.itable import ITable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppMenuBar:
    '''
        Application menu bar component building File, Edit, View menus and binding hotkeys.

        It defines:

            :attributes:
                | _root - Application root Tk window.
                | _service - Core trajectory service instance.
                | _canvas - CAD canvas interface.
                | _table - Waypoint table interface.
            :methods:
                | __init__ - Initializes and attaches menu bar to root window.
                | open_json_dialog - Shows open file dialog and loads selected trajectory plan.
                | save_json_dialog - Shows save file dialog and saves current trajectory plan.
                | import_dsl_dialog - Shows open file dialog and compiles selected SCARA DSL script into plan.
                | export_dsl_dialog - Shows save file dialog and exports active trajectory plan to SCARA DSL format.
    '''

    _root: Tk
    _service: IService
    _canvas: ICanvas
    _table: ITable

    def __init__(
        self,
        root: Tk,
        service: IService,
        canvas: ICanvas,
        table: ITable
    ) -> None:
        '''
            Initializes and attaches menu bar to root window.

            :param root: Application root Tk window.
            :param service: IService instance.
            :param canvas: ICanvas interface instance.
            :param table: ITable interface instance.
        '''
        self._root: Final[Tk] = root
        self._service: Final[IService] = service
        self._canvas: Final[ICanvas] = canvas
        self._table: Final[ITable] = table

        self._build_menu()
        self._bind_hotkeys()

    def _build_menu(self) -> None:
        '''
            Constructs File, Edit, View cascades and sets root menu.
        '''
        menubar = Menu(self._root, bg='#21252b', fg='#abb2bf', activebackground='#61afef', activeforeground='#ffffff')

        file_m = Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        file_m.add_command(label='New (Ctrl+N)', command=self._service.new_plan)
        file_m.add_command(label='Open JSON... (Ctrl+O)', command=self.open_json_dialog)
        file_m.add_command(label='Save JSON... (Ctrl+S)', command=self.save_json_dialog)
        file_m.add_separator()
        file_m.add_command(label='Import SCARA DSL (.scara)...', command=self.import_dsl_dialog)
        file_m.add_command(label='Export SCARA DSL (.scara)...', command=self.export_dsl_dialog)
        file_m.add_separator()
        file_m.add_command(label='Exit', command=self._root.quit)
        menubar.add_cascade(label='File', menu=file_m)

        edit_m = Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        edit_m.add_command(label='Undo (Ctrl+Z)', command=self._service.undo)
        edit_m.add_command(label='Redo (Ctrl+Y)', command=self._service.redo)
        edit_m.add_separator()
        edit_m.add_command(label='Clear All', command=self._service.clear_plan)
        menubar.add_cascade(label='Edit', menu=edit_m)

        view_m = Menu(menubar, tearoff=0, bg='#21252b', fg='#abb2bf')
        view_m.add_command(label='Zoom In (+)', command=self._canvas.zoom_in)
        view_m.add_command(label='Zoom Out (-)', command=self._canvas.zoom_out)
        view_m.add_command(label='Fit Workspace', command=self._canvas.fit_reach_view)
        view_m.add_command(label='Reset 100%', command=self._canvas.reset_view)
        menubar.add_cascade(label='View', menu=view_m)

        self._root.config(menu=menubar)

    def _bind_hotkeys(self) -> None:
        '''
            Binds keyboard shortcuts to window.
        '''
        self._root.bind('<Control-n>', lambda e: self._service.new_plan())
        self._root.bind('<Control-o>', lambda e: self.open_json_dialog())
        self._root.bind('<Control-s>', lambda e: self.save_json_dialog())
        self._root.bind('<Control-z>', lambda e: self._service.undo())
        self._root.bind('<Control-y>', lambda e: self._service.redo())
        self._root.bind('<Delete>', lambda e: self._table.delete_selected())
        self._root.bind('<BackSpace>', lambda e: self._table.delete_selected())

    def open_json_dialog(self) -> None:
        '''
            Shows open file dialog and loads selected trajectory plan.
        '''
        path: str = askopenfilename(filetypes=[('SCARA Plan JSON', '*.json'), ('All Files', '*.*')])
        if path:
            try:
                self._service.load_plan(path)
                self._canvas.fit_reach_view()
            except OSError as exc:
                showerror('Load Error', f'Failed to load plan: {exc}')

    def save_json_dialog(self) -> None:
        '''
            Shows save file dialog and saves current trajectory plan.
        '''
        path: str = asksaveasfilename(defaultextension='.json', filetypes=[('SCARA Plan JSON', '*.json')])
        if path:
            try:
                self._service.save_plan(path)
                showinfo('Save Plan', 'Plan saved successfully!')
            except OSError as exc:
                showerror('Save Error', f'Failed to save plan: {exc}')

    def import_dsl_dialog(self) -> None:
        '''
            Shows open file dialog and compiles selected SCARA DSL script into plan.
        '''
        path: str = askopenfilename(
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')]
        )
        if path:
            try:
                content: str = self._service.get_storage().load_text_file(path)
                plan = self._service.get_dsl_service().compile_script(source=content)
                self._service.get_plan().set_waypoints(plan.waypoints)
                self._canvas.fit_reach_view()
                showinfo(
                    'Import SCARA DSL',
                    f'Successfully imported {plan.count} waypoints from DSL script!'
                )
            except Exception as exc:
                showerror('Import Error', f'Failed to compile SCARA DSL script:\n{exc}')

    def export_dsl_dialog(self) -> None:
        '''
            Shows save file dialog and exports active trajectory plan to SCARA DSL format.
        '''
        path: str = asksaveasfilename(
            defaultextension='.scara',
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')]
        )
        if path:
            try:
                content: str = self._service.get_dsl_service().export_plan(plan=self._service.get_plan())
                self._service.get_storage().save_text_file(content, path)
                showinfo('Export SCARA DSL', 'DSL script exported successfully!')
            except OSError as exc:
                showerror('Export Error', f'Failed to export DSL script:\n{exc}')
