# -*- coding: UTF-8 -*-

'''
Module
    app_menu_bar.py
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
    Top application menu bar coordinator and file I/O action handlers.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo
from typing import Final

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.menu.builders_bundle import MenuBuildersBundle
from scarajectory.infrastructure.gui.menu.bundle import MenuBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppMenuBar:
    '''
        Top application menu bar coordinating file I/O operations and bindings.

        It defines:

            :attributes:
                | _root - Application root Tk window.
                | _navigator - Viewport navigation interface.
                | _table - Waypoint table interface.
                | _store - Waypoint store interface.
                | _mutation - Plan mutation service interface.
                | _storage - Plan storage service interface.
                | _dsl_service - SCARA DSL service interface.
            :methods:
                | __init__ - Initializes and attaches menu bar to root window.
                | open_json_dialog - Shows open file dialog and loads plan.
                | save_json_dialog - Shows save file dialog and saves plan.
                | import_dsl_dialog - Compiles DSL script into plan.
                | export_dsl_dialog - Exports active plan to DSL format.
    '''

    _root: Tk
    _navigator: ICanvasViewNavigator
    _table: ITable
    _store: IWaypointStore
    _mutation: IPlanBulkMutator
    _storage: IPlanStorageService
    _dsl_service: IScaraDslService

    def __init__(
        self,
        root: Tk,
        bundle: MenuBundle,
        builders: MenuBuildersBundle,
    ) -> None:
        '''
            Initializes and attaches menu bar to root window.

            :param root: Application root Tk window.
            :param bundle: Injected MenuBundle container instance.
            :param builders: Injected MenuBuildersBundle container instance.
            :exceptions: None.
        '''
        self._root: Final[Tk] = root
        self._navigator: Final[ICanvasViewNavigator] = bundle.navigator
        self._table: Final[ITable] = bundle.table
        self._store: Final[IWaypointStore] = bundle.store
        self._mutation: Final[IPlanBulkMutator] = bundle.mutation
        self._storage: Final[IPlanStorageService] = bundle.storage
        self._dsl_service: Final[IScaraDslService] = bundle.dsl_service

        builders.layout_builder.build_menu(
            root=self._root,
            menu_bar=self,
            mutation=bundle.mutation,
            history=bundle.history,
            navigator=self._navigator,
        )
        builders.hotkey_binder.bind_hotkeys(
            root=self._root,
            menu_bar=self,
            mutation=bundle.mutation,
            history=bundle.history,
            table=self._table,
        )

    def open_json_dialog(self) -> None:
        '''
            Shows open file dialog and loads selected trajectory plan.
        '''
        path: str = askopenfilename(
            filetypes=[('SCARA Plan JSON', '*.json'), ('All Files', '*.*')]
        )

        if path:
            try:
                waypoints = self._storage.load_plan(path)
                self._mutation.set_waypoints(waypoints)
                self._navigator.fit_reach_view()

            except OSError as exc:
                showerror('Load Error', f'Failed to load plan: {exc}')

    def save_json_dialog(self) -> None:
        '''
            Shows save file dialog and saves current trajectory plan.
        '''
        path: str = asksaveasfilename(
            defaultextension='.json',
            filetypes=[('SCARA Plan JSON', '*.json')],
        )

        if path:
            try:
                self._storage.save_plan(self._store, path)
                showinfo('Save Plan', 'Plan saved successfully!')

            except OSError as exc:
                showerror('Save Error', f'Failed to save plan: {exc}')

    def import_dsl_dialog(self) -> None:
        '''
            Shows open file dialog and compiles DSL script into plan.
        '''
        path: str = askopenfilename(
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')]
        )

        if path:
            try:
                content: str = self._storage.load_text_file(path)
                plan = self._dsl_service.compile_script(source=content)
                self._mutation.set_waypoints(plan.waypoints)
                self._navigator.fit_reach_view()
                count: int = plan.count
                showinfo(
                    'Import SCARA DSL',
                    f'Successfully imported {count} waypoints from script!'
                )

            except Exception as exc:
                showerror(
                    'Import Error',
                    f'Failed to compile SCARA DSL script:\n{exc}'
                )

    def export_dsl_dialog(self) -> None:
        '''
            Shows save file dialog and exports plan to SCARA DSL.
        '''
        path: str = asksaveasfilename(
            defaultextension='.scara',
            filetypes=[('SCARA DSL Scripts', '*.scara'), ('All Files', '*.*')]
        )

        if path:
            try:
                content: str = self._dsl_service.export_plan(plan=self._store)
                self._storage.save_text_file(content, path)
                showinfo(
                    'Export SCARA DSL', 'DSL script exported successfully!'
                )

            except OSError as exc:
                showerror(
                    'Export Error', f'Failed to export DSL script:\n{exc}'
                )
