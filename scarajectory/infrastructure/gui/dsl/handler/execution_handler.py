# -*- coding: UTF-8 -*-

'''
Module
    execution_handler.py
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
    Handles DSL compilation, validation, plan export, and emulator preview actions.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.dsl.code_editor import DslCodeEditor
from scarajectory.infrastructure.gui.dsl.console_view import DslConsoleView
from scarajectory.infrastructure.gui.dsl.handler.execution_handler_bundle import ExecutionHandlerBundle
from scarajectory.infrastructure.gui.emulator.iemulator_launcher import IEmulatorLauncher
from scarajectory.setup.pipeline.dsl_pipeline_bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorExecutionHandler:
    '''
        Action handler executing DSL compilation, kinematic validation, plan export, and preview.

        It defines:

            :attributes:
                | _store - Injected waypoint query collaborator.
                | _mutation - Injected plan mutation service collaborator.
                | _dsl - Injected SCARA DSL pipeline role services bundle.
                | _launcher - SCARAEmu emulator process launcher.
                | _editor - Code editor subcomponent.
                | _console - Diagnostic console view subcomponent.
            :methods:
                | __init__ - Initializes the execution action handler with bundle.
                | compile_to_plan - Compiles DSL code to active trajectory plan.
                | validate_code - Runs syntax and reachability validation on editor code.
                | export_plan_to_editor - Serializes current active plan into DSL code.
                | preview_in_scaraemu - Launches SCARAEmu emulator preview.
    '''

    _store: IWaypointStore
    _mutation: IPlanBulkMutator
    _dsl: DslPipelineBundle
    _launcher: IEmulatorLauncher
    _editor: DslCodeEditor
    _console: DslConsoleView

    def __init__(
        self,
        *,
        bundle: ExecutionHandlerBundle,
    ) -> None:
        '''
            Initializes the execution action handler with collaborators bundle.

            :param bundle: Required ExecutionHandlerBundle container.
            :exceptions: None.
        '''
        self._store: Final[IWaypointStore] = bundle.store
        self._mutation: Final[IPlanBulkMutator] = bundle.mutation
        self._dsl: Final[DslPipelineBundle] = bundle.dsl
        self._launcher: Final[IEmulatorLauncher] = bundle.launcher
        self._editor: Final[DslCodeEditor] = bundle.editor
        self._console: Final[DslConsoleView] = bundle.console

    def compile_to_plan(self) -> None:
        '''
            Compiles editor code and replaces waypoints in the active trajectory plan.

            :exceptions: None.
        '''
        source: str = self._editor.get_text().strip()

        if not source:
            self._console.append_log(
                '❌ Editor is empty. Nothing to compile.',
                level='warning',
            )
            return

        try:
            compiled_plan = self._dsl.plan_compiler.compile_script(source=source)
            self._mutation.set_waypoints(compiled_plan.waypoints)
            msg: str = (
                f'✅ Successfully compiled and synchronized!\n'
                f'Waypoints in Plan: {compiled_plan.count} | '
                f'Kinematic Feasibility: PASSED'
            )
            self._console.append_log(msg, level='success')

        except Exception as exc:
            err_msg: str = self._dsl.diagnostics.compile_error_handler.format_error(
                error=exc
            )
            self._console.append_log(f'❌ {err_msg}', level='error')

    def validate_code(self) -> None:
        '''
            Validates editor code syntax and kinematics without modifying the plan.

            :exceptions: None.
        '''
        source: str = self._editor.get_text().strip()

        if not source:
            self._console.append_log(
                '❌ Editor is empty. Nothing to validate.',
                level='warning',
            )
            return

        is_valid, messages = self._dsl.validator.validate_script(source=source)
        if is_valid:
            for msg in messages:
                self._console.append_log(f'✅ {msg}', level='success')
        else:
            for msg in messages:
                level: str = 'warning' if '[WARNING]' in msg else 'error'
                prefix: str = '⚠️ ' if level == 'warning' else '❌ '
                self._console.append_log(f'{prefix}{msg}', level=level)

    def export_plan_to_editor(self) -> None:
        '''
            Serializes active plan waypoints into the editor text.

            :exceptions: None.
        '''
        script: str = self._dsl.plan_exporter.export_plan(plan=self._store)
        self._editor.set_text(script)
        self._console.append_log(
            f'ℹ️ Exported {self._store.count} waypoints to SCARA DSL format.',
            level='info',
        )

    def preview_in_scaraemu(self) -> None:
        '''
            Exports active DSL script and launches SCARAEmu for visual twin preview.

            :exceptions: None.
        '''
        code: str = self._editor.get_text().strip()

        if not code:
            self._console.append_log(
                '[WARN]: DSL editor is empty. Nothing to preview.',
                level='warning',
            )
            return

        success, message = self._launcher.launch_preview(dsl_code=code)
        self._console.append_log(
            message,
            level='success' if success else 'error',
        )
