# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_tab.py
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
    Dedicated SCARA DSL code editor and compiler tab integrated into the controls notebook.
'''

from __future__ import annotations

from tkinter import BOTH, Widget, X
from tkinter.ttk import Frame
from typing import Final

from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.dsl.scara_dsl_service import ScaraDslService
from scarajectory.core.service.trajectory.iplan_storage_service import (
    IPlanStorageService,
)
from scarajectory.core.service.trajectory.itrajectory_validator import (
    ITrajectoryValidator,
)
from scarajectory.infrastructure.gui.dsl.dsl_code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.dsl_console_view import DslConsoleView
from scarajectory.infrastructure.gui.dsl.dsl_document_manager import (
    DslDocumentManager,
)
from scarajectory.infrastructure.gui.dsl.dsl_editor_toolbar import (
    DslEditorToolbar,
)
from scarajectory.infrastructure.gui.dsl.dsl_example_catalog import (
    DslExampleCatalog,
)
from scarajectory.infrastructure.gui.dsl.emulator_launcher import (
    EmulatorLauncher,
)
from scarajectory.infrastructure.gui.dsl.iemulator_launcher import (
    IEmulatorLauncher,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorTab(Frame):
    '''
        SCARA DSL script editor with syntax highlighting, compilation, validation and export.

        It defines:

            :attributes:
                | _plan - Active trajectory plan instance.
                | _dsl_service - High-level DSL compilation and serialization service.
                | _launcher - SCARAEmu emulator process launcher.
                | _catalog - Example scripts and demonstration catalog.
                | _doc_manager - Document persistence and modal dialog manager.
                | _toolbar - Toolbar subcomponent.
                | _editor - Code editor subcomponent.
                | _console - Diagnostic console view subcomponent.
            :methods:
                | __init__ - Initializes the editor tab layout and mounts subcomponents.
                | compile_to_plan - Compiles editor code and updates the active plan.
                | validate_code - Validates editor code syntax and kinematics without mutating plan.
                | export_plan_to_editor - Serializes current plan into the editor text.
                | preview_in_scaraemu - Launches SCARAEmu visualizer with active script.
                | open_file - Opens a .scara file into the editor.
                | save_file - Saves editor contents to a .scara file.
                | load_example - Inserts standard demonstration SCARA script.
    '''

    _plan: ITrajectoryPlan
    _dsl_service: IScaraDslService
    _launcher: IEmulatorLauncher
    _catalog: DslExampleCatalog
    _doc_manager: DslDocumentManager
    _toolbar: DslEditorToolbar
    _editor: DslCodeEditor
    _console: DslConsoleView

    def __init__(
        self,
        parent: Widget,
        *,
        plan: ITrajectoryPlan,
        validator: ITrajectoryValidator | None = None,
        dsl_service: IScaraDslService | None = None,
        storage: IPlanStorageService | None = None,
        launcher: IEmulatorLauncher | None = None,
        catalog: DslExampleCatalog | None = None,
        document_manager: DslDocumentManager | None = None,
        **kwargs: object,
    ) -> None:
        '''
            Initializes the SCARA DSL editor tab.

            :param parent: Parent container widget.
            :param plan: Active ITrajectoryPlan instance.
            :param validator: Optional ITrajectoryValidator instance.
            :param dsl_service: Optional IScaraDslService instance.
            :param storage: Optional IPlanStorageService instance.
            :param launcher: Optional IEmulatorLauncher instance.
            :param catalog: Optional DslExampleCatalog instance.
            :param document_manager: Optional DslDocumentManager instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=4, **kwargs)
        self._plan = plan
        self._dsl_service = (
            dsl_service
            if dsl_service is not None
            else ScaraDslService(validator=validator)
        )
        self._launcher = (
            launcher
            if launcher is not None
            else EmulatorLauncher()
        )
        self._catalog = (
            catalog
            if catalog is not None
            else DslExampleCatalog(storage=storage)
        )
        self._doc_manager = (
            document_manager
            if document_manager is not None
            else DslDocumentManager(storage=storage)
        )

        self._build_layout()
        self._load_initial_content()

    def _build_layout(self) -> None:
        '''
            Constructs action toolbar, code editor, and status console.

            :exceptions: None.
        '''
        self._toolbar = DslEditorToolbar(
            self,
            on_compile=self.compile_to_plan,
            on_validate=self.validate_code,
            on_export=self.export_plan_to_editor,
            on_preview=self.preview_in_scaraemu,
            on_open=self.open_file,
            on_save=self.save_file,
            on_example_selected=self._on_example_selected,
        )
        self._toolbar.pack(fill=X)

        example_files: list[str] = self._catalog.get_example_files()
        if example_files:
            self._toolbar.set_example_files(example_files)

        self._editor = DslCodeEditor(self)
        self._editor.pack(fill=BOTH, expand=True)

        self._console = DslConsoleView(self)
        self._console.pack(fill=X, pady=(4, 0))

    def _load_initial_content(self) -> None:
        '''
            Loads either the exported active plan or the demonstration script into the editor.

            :exceptions: None.
        '''
        if self._plan.count > 0:
            self.export_plan_to_editor()
        elif self._toolbar.get_selected_example():
            self._on_example_selected(self._toolbar.get_selected_example())
        else:
            self.load_example()

    def compile_to_plan(self) -> None:
        '''
            Compiles editor code and replaces waypoints in the active TrajectoryPlan.

            :exceptions: None.
        '''
        source: str = self._editor.get_text().strip()
        if not source:
            self._console.log('❌ Editor is empty. Nothing to compile.', is_error=True)
            return

        try:
            compiled_plan = self._dsl_service.compile_script(source=source)
            self._plan.set_waypoints(compiled_plan.waypoints)
            msg = (
                f'✅ Successfully compiled and synchronized!\n'
                f'Waypoints in Plan: {compiled_plan.count} | '
                f'Kinematic Feasibility: PASSED'
            )
            self._console.log(msg, is_error=False)
        except Exception as exc:
            self._console.log(f'❌ Compilation error: {exc}', is_error=True)

    def validate_code(self) -> None:
        '''
            Validates editor code syntax and kinematics without modifying the plan.

            :exceptions: None.
        '''
        source: str = self._editor.get_text().strip()
        if not source:
            self._console.log('❌ Editor is empty. Nothing to validate.', is_error=True)
            return

        is_valid, messages = self._dsl_service.validate_script(source=source)
        self._console.log('\n'.join(messages), is_error=not is_valid)

    def export_plan_to_editor(self) -> None:
        '''
            Serializes the active plan waypoints into the editor.

            :exceptions: None.
        '''
        script = self._dsl_service.export_plan(plan=self._plan)
        self._editor.set_text(script)
        self._console.log(
            f'ℹ️ Exported {self._plan.count} waypoints to SCARA DSL format.',
            is_error=False,
        )

    def preview_in_scaraemu(self) -> None:
        '''
            Exports active DSL script to temporary file and launches SCARAEmu for visual twin preview.

            :exceptions: None.
        '''
        code: str = self._editor.get_text().strip()
        if not code:
            self._console.log(
                '[WARN]: DSL editor is empty. Nothing to preview.',
                is_error=True,
            )
            return

        success, message = self._launcher.launch_preview(dsl_code=code)
        self._console.log(message, is_error=not success)

    def open_file(self) -> None:
        '''
            Opens a .scara file and loads it into the editor.

            :exceptions: None.
        '''
        result = self._doc_manager.open_document(parent=self)
        if result is not None:
            content, filepath = result
            self._editor.set_text(content)
            self._console.log(f'ℹ️ Loaded file: {filepath}', is_error=False)

    def save_file(self) -> None:
        '''
            Saves editor content to a .scara file.

            :exceptions: None.
        '''
        content: str = self._editor.get_text()
        filepath = self._doc_manager.save_document(parent=self, content=content)
        if filepath is not None:
            self._console.log(f'ℹ️ Saved file: {filepath}', is_error=False)

    def _on_example_selected(self, selected: str | None = None) -> None:
        '''
            Loads the selected example script from disk into the editor.

            :param selected: Optional name of example file.
            :exceptions: None.
        '''
        name = selected or self._toolbar.get_selected_example()
        if name:
            content = self._catalog.load_example_content(filename=name)
            if content is not None:
                self._editor.set_text(content)
                self._console.log(f'ℹ️ Loaded example: {name}', is_error=False)
                return
        self.load_example()

    def load_example(self) -> None:
        '''
            Inserts standard demonstration SCARA script.

            :exceptions: None.
        '''
        self._editor.set_text(self._catalog.get_default_script())
        self._console.log('ℹ️ Demonstration SCARA DSL script loaded.', is_error=False)
