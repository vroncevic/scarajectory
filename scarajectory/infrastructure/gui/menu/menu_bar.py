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
    Top application menu bar coordinating file I/O operations and bindings.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo
from typing import ClassVar, Final

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.menu.builder.bundle import MenuBuildersBundle
from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

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
        Top application menu bar coordinating file I/O operations and bindings.

        It defines:

            :constants:
                | EXT_JSON - Default JSON file extension.
                | EXT_SCARA - Default SCARA DSL file extension.
                | FILTER_JSON - File dialog filters for opening JSON plan files.
                | FILTER_SAVE_JSON - File dialog filters for saving JSON plan files.
                | FILTER_DSL - File dialog filters for importing SCARA DSL scripts.
                | FILTER_SAVE_DSL - File dialog filters for exporting SCARA DSL scripts.
            :attributes:
                | _root - Application root Tk window.
                | _navigator - Viewport navigation interface.
                | _table - Waypoint table interface.
                | _plan - Trajectory plan management pipeline bundle.
                | _loader - Plan loader service interface.
                | _storer - Plan storer service interface.
                | _dsl - SCARA DSL pipeline role services bundle.
            :methods:
                | __init__ - Initializes and attaches menu bar to root window.
                | open_json_dialog - Shows open file dialog and loads plan.
                | save_json_dialog - Shows save file dialog and saves plan.
                | import_dsl_dialog - Compiles DSL script into plan.
                | export_dsl_dialog - Exports active plan to DSL format.
                | get_version - Returns component version string.
    '''

    EXT_JSON: ClassVar[str] = '.json'
    EXT_SCARA: ClassVar[str] = '.scara'
    FILTER_JSON: ClassVar[tuple[tuple[str, str], ...]] = (
        ('SCARA Plan JSON', '*.json'),
        ('All Files', '*.*'),
    )
    FILTER_SAVE_JSON: ClassVar[tuple[tuple[str, str], ...]] = (
        ('SCARA Plan JSON', '*.json'),
    )
    FILTER_DSL: ClassVar[tuple[tuple[str, str], ...]] = (
        ('SCARA DSL Scripts', '*.scara'),
        ('All Files', '*.*'),
    )
    FILTER_SAVE_DSL: ClassVar[tuple[tuple[str, str], ...]] = (
        ('SCARA DSL Scripts', '*.scara'),
        ('All Files', '*.*'),
    )

    _root: Tk
    _navigator: ICanvasViewNavigator
    _table: ITable
    _plan: PlanPipelineBundle
    _loader: IPlanLoader
    _storer: IPlanStorer
    _dsl: DslPipelineBundle

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
        self._plan: Final[PlanPipelineBundle] = bundle.plan
        self._loader: Final[IPlanLoader] = bundle.loader
        self._storer: Final[IPlanStorer] = bundle.storer
        self._dsl: Final[DslPipelineBundle] = bundle.dsl

        builders.layout_builder.build_menu(
            root=self._root,
            menu_bar=self,
            bundle=bundle,
        )
        builders.hotkey_binder.bind_hotkeys(
            root=self._root,
            menu_bar=self,
            bundle=bundle,
        )

    def open_json_dialog(self) -> None:
        '''
            Shows open file dialog and loads selected trajectory plan.

            :exceptions: None.
        '''
        path: str = askopenfilename(filetypes=self.FILTER_JSON)

        if path:
            try:
                waypoints = self._loader.load_plan(path)
                self._plan.mutation.set_waypoints(waypoints)
                self._navigator.fit_reach_view()

            except OSError as exc:
                showerror('Load Error', f'Failed to load plan: {exc}')

    def save_json_dialog(self) -> None:
        '''
            Shows save file dialog and saves current trajectory plan.

            :exceptions: None.
        '''
        path: str = asksaveasfilename(
            defaultextension=self.EXT_JSON,
            filetypes=self.FILTER_SAVE_JSON,
        )

        if path:
            try:
                self._storer.save_plan(self._plan.store, path)
                showinfo('Save Plan', 'Plan saved successfully!')

            except OSError as exc:
                showerror('Save Error', f'Failed to save plan: {exc}')

    def import_dsl_dialog(self) -> None:
        '''
            Shows open file dialog and compiles DSL script into plan.

            :exceptions: None.
        '''
        path: str = askopenfilename(filetypes=self.FILTER_DSL)

        if path:
            try:
                content: str = self._loader.load_text_file(path)
                plan = self._dsl.plan_compiler.compile_script(source=content)
                self._plan.mutation.set_waypoints(plan.waypoints)
                self._navigator.fit_reach_view()
                count: int = plan.count
                showinfo(
                    'Import SCARA DSL',
                    f'Successfully imported {count} waypoints from script!'
                )

            except (ValueError, OSError, RuntimeError) as exc:
                showerror(
                    'Import Error',
                    f'Failed to compile SCARA DSL script:\n{exc}'
                )

    def export_dsl_dialog(self) -> None:
        '''
            Shows save file dialog and exports plan to SCARA DSL.

            :exceptions: None.
        '''
        path: str = asksaveasfilename(
            defaultextension=self.EXT_SCARA,
            filetypes=self.FILTER_SAVE_DSL,
        )

        if path:
            try:
                content: str = self._dsl.plan_exporter.export_plan(
                    plan=self._plan.store
                )
                self._storer.save_text_file(content, path)
                showinfo(
                    'Export SCARA DSL', 'DSL script exported successfully!'
                )

            except OSError as exc:
                showerror(
                    'Export Error', f'Failed to export DSL script:\n{exc}'
                )

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
