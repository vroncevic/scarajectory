# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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

from typing import ClassVar, Final

from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.infrastructure.gui.dsl.handler.execution.bundle import ExecutionHandlerBundle
from scarajectory.infrastructure.gui.emulator.launcher.ilauncher import IEmulatorLauncher
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslExecutionHandler:
    '''
        Action handler executing DSL compilation, kinematic validation, plan export, and preview.

        It defines:

            :attributes:
                | MSG_EMPTY_COMPILE - Warning message shown when compiling empty editor.
                | MSG_EMPTY_VALIDATE - Warning message shown when validating empty editor.
                | MSG_EMPTY_PREVIEW - Warning message shown when previewing empty editor.
                | LOG_LEVEL_WARNING - Warning log level tag.
                | LOG_LEVEL_SUCCESS - Success log level tag.
                | LOG_LEVEL_ERROR - Error log level tag.
                | LOG_LEVEL_INFO - Informational log level tag.
                | TAG_WARNING - Marker substring indicating warning message.
                | _store - Injected waypoint query collaborator.
                | _mutation - Injected plan mutation service collaborator.
                | _dsl - Injected SCARA DSL pipeline role services bundle.
                | _launcher - SCARAEmu emulator process launcher.
                | _editor - Code editor structural protocol subcomponent.
                | _console - Diagnostic console view structural protocol subcomponent.
            :methods:
                | __init__ - Initializes the execution action handler with bundle.
                | compile_to_plan - Compiles DSL code to active trajectory plan.
                | validate_code - Runs syntax and reachability validation on editor code.
                | export_plan_to_editor - Serializes current active plan into DSL code.
                | preview_in_scaraemu - Launches SCARAEmu emulator preview.
                | get_version - Returns the handler version string representation.
    '''

    MSG_EMPTY_COMPILE: ClassVar[str] = '❌ Editor is empty. Nothing to compile.'
    MSG_EMPTY_VALIDATE: ClassVar[str] = (
        '❌ Editor is empty. Nothing to validate.'
    )
    MSG_EMPTY_PREVIEW: ClassVar[str] = (
        '[WARN]: DSL editor is empty. Nothing to preview.'
    )
    LOG_LEVEL_WARNING: ClassVar[str] = 'warning'
    LOG_LEVEL_SUCCESS: ClassVar[str] = 'success'
    LOG_LEVEL_ERROR: ClassVar[str] = 'error'
    LOG_LEVEL_INFO: ClassVar[str] = 'info'
    TAG_WARNING: ClassVar[str] = '[WARNING]'

    _store: IWaypointStore
    _mutation: IPlanBulkMutator
    _dsl: DslPipelineBundle
    _launcher: IEmulatorLauncher
    _editor: IDslCodeEditor
    _console: IDslConsoleView

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
        self._editor: Final[IDslCodeEditor] = bundle.editor
        self._console: Final[IDslConsoleView] = bundle.console

    def compile_to_plan(self) -> None:
        '''
            Compiles editor code and replaces waypoints in the active trajectory plan.

            :exceptions: None.
        '''
        source: str = self._editor.get_text().strip()

        if not source:
            self._console.append_log(
                self.MSG_EMPTY_COMPILE,
                level=self.LOG_LEVEL_WARNING,
            )
            return

        try:
            compiled_plan = self._dsl.plan_compiler.compile_script(
                source=source
            )
            self._mutation.set_waypoints(compiled_plan.waypoints)
            msg: str = (
                f'✅ Successfully compiled and synchronized!\n'
                f'Waypoints in Plan: {compiled_plan.count} | '
                f'Kinematic Feasibility: PASSED'
            )
            self._console.append_log(msg, level=self.LOG_LEVEL_SUCCESS)

        except Exception as exc:
            err_msg: str = (
                self._dsl.diagnostics.compile_error_handler.format_error(
                    error=exc
                )
            )
            self._console.append_log(
                f'❌ {err_msg}', level=self.LOG_LEVEL_ERROR
            )

    def validate_code(self) -> None:
        '''
            Validates editor code syntax and kinematics without modifying the plan.

            :exceptions: None.
        '''
        source: str = self._editor.get_text().strip()

        if not source:
            self._console.append_log(
                self.MSG_EMPTY_VALIDATE,
                level=self.LOG_LEVEL_WARNING,
            )
            return

        is_valid, messages = self._dsl.validator.validate_script(source=source)
        if is_valid:
            for msg in messages:
                self._console.append_log(f'✅ {msg}', level=self.LOG_LEVEL_SUCCESS)
        else:
            for msg in messages:
                level: str = (
                    self.LOG_LEVEL_WARNING
                    if self.TAG_WARNING in msg
                    else self.LOG_LEVEL_ERROR
                )
                prefix: str = (
                    '⚠️ ' if level == self.LOG_LEVEL_WARNING else '❌ '
                )
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
            level=self.LOG_LEVEL_INFO,
        )

    def preview_in_scaraemu(self) -> None:
        '''
            Exports active DSL script and launches SCARAEmu for visual twin preview.

            :exceptions: None.
        '''
        code: str = self._editor.get_text().strip()

        if not code:
            self._console.append_log(
                self.MSG_EMPTY_PREVIEW,
                level=self.LOG_LEVEL_WARNING,
            )
            return

        success, message = self._launcher.launch_preview(dsl_code=code)
        self._console.append_log(
            message,
            level=self.LOG_LEVEL_SUCCESS if success else self.LOG_LEVEL_ERROR,
        )

    def get_version(self) -> str:
        '''
            Returns the handler version string representation.

            :return: Handler version string.
            :exceptions: None.
        '''
        return __version__
