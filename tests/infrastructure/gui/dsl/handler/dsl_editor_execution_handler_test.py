# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_execution_handler_test.py
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
    Unit tests for DslEditorExecutionHandler actions.
'''

from __future__ import annotations

from types import SimpleNamespace
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.handler.execution_handler_factory import DslEditorExecutionHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.execution_handler import DslEditorExecutionHandler
from scarajectory.infrastructure.gui.dsl.handler.execution_handler_bundle import ExecutionHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.iexecution_delegate import IDslExecutionDelegate
from scarajectory.setup.pipeline.dsl_diagnostic_bundle import DslDiagnosticBundle
from scarajectory.setup.pipeline.dsl_pipeline_bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorExecutionHandler(TestCase):
    '''Test cases verifying DslEditorExecutionHandler actions.'''

    mocks: SimpleNamespace
    handler: DslEditorExecutionHandler

    def setUp(self) -> None:
        compile_error_handler = MagicMock()
        compile_error_handler.format_error.side_effect = (
            lambda error: f'compile error: {error}'
        )

        diagnostics = DslDiagnosticBundle(
            compile_error_handler=compile_error_handler,
            lint_error_handler=MagicMock(),
            decompile_error_handler=MagicMock(),
            export_error_handler=MagicMock(),
            diagnostic_formatter=MagicMock(),
        )

        mocks = SimpleNamespace(
            store=MagicMock(count=5),
            mutation=MagicMock(),
            compiler=MagicMock(),
            decompiler=MagicMock(),
            plan_compiler=MagicMock(),
            plan_exporter=MagicMock(),
            validator=MagicMock(),
            diagnostics=diagnostics,
            launcher=MagicMock(),
            editor=MagicMock(),
            console=MagicMock(),
        )
        dsl_bundle = DslPipelineBundle(
            compiler=mocks.compiler,
            decompiler=mocks.decompiler,
            plan_compiler=mocks.plan_compiler,
            plan_exporter=mocks.plan_exporter,
            validator=mocks.validator,
            diagnostics=diagnostics,
        )
        bundle = ExecutionHandlerBundle(
            store=mocks.store,
            mutation=mocks.mutation,
            dsl=dsl_bundle,
            launcher=mocks.launcher,
            editor=mocks.editor,
            console=mocks.console,
        )
        self.mocks = mocks
        self.handler = DslEditorExecutionHandlerFactory.create(bundle=bundle)

    def test_protocol_conformance(self) -> None:
        '''Tests structural protocol conformance against IDslExecutionDelegate.'''
        self.assertIsInstance(self.handler, IDslExecutionDelegate)
        self.assertIsInstance(DslEditorExecutionHandlerFactory.get_version(), str)

    def test_compile_to_plan_empty_source(self) -> None:
        '''Tests that compile_to_plan with empty editor logs warning and aborts.'''
        self.mocks.editor.get_text.return_value = '   \n  '
        self.handler.compile_to_plan()
        self.mocks.console.append_log.assert_called_once_with(
            '❌ Editor is empty. Nothing to compile.', level='warning'
        )
        self.mocks.plan_compiler.compile_script.assert_not_called()
        self.mocks.mutation.set_waypoints.assert_not_called()

    def test_compile_to_plan_success(self) -> None:
        '''Tests successful compilation and plan synchronization.'''
        self.mocks.editor.get_text.return_value = 'MOVE P1\nMOVE P2'
        mock_compiled = MagicMock(count=2, waypoints=[MagicMock(), MagicMock()])
        self.mocks.plan_compiler.compile_script.return_value = mock_compiled
        self.handler.compile_to_plan()
        self.mocks.plan_compiler.compile_script.assert_called_once_with(
            source='MOVE P1\nMOVE P2'
        )
        self.mocks.mutation.set_waypoints.assert_called_once_with(
            mock_compiled.waypoints
        )
        self.mocks.console.append_log.assert_called_once()
        call_args = self.mocks.console.append_log.call_args
        log_msg: str = call_args[0][0]
        self.assertIn('Successfully compiled', log_msg)
        self.assertEqual(call_args.kwargs['level'], 'success')

    def test_compile_to_plan_error(self) -> None:
        '''Tests compile_to_plan handles compilation exceptions gracefully.'''
        self.mocks.editor.get_text.return_value = 'INVALID SYNTAX'
        self.mocks.plan_compiler.compile_script.side_effect = ValueError(
            'Syntax error at line 1'
        )
        self.handler.compile_to_plan()
        self.mocks.console.append_log.assert_called_once()
        call_args = self.mocks.console.append_log.call_args
        log_msg: str = call_args[0][0]
        self.assertIn('compile error: Syntax error at line 1', log_msg)
        self.assertEqual(call_args.kwargs['level'], 'error')

    def test_validate_code_empty(self) -> None:
        '''Tests validate_code with empty text logs warning and returns early.'''
        self.mocks.editor.get_text.return_value = ''
        self.handler.validate_code()
        self.mocks.console.append_log.assert_called_once_with(
            '❌ Editor is empty. Nothing to validate.', level='warning'
        )
        self.mocks.validator.validate_script.assert_not_called()

    def test_validate_code_valid(self) -> None:
        '''Tests validate_code with valid script logs messages as success.'''
        self.mocks.editor.get_text.return_value = 'MOVE P1'
        self.mocks.validator.validate_script.return_value = (
            True, ['All syntax valid']
        )
        self.handler.validate_code()
        self.mocks.validator.validate_script.assert_called_once_with(
            source='MOVE P1'
        )
        self.mocks.console.append_log.assert_called_once_with(
            '✅ All syntax valid', level='success'
        )

    def test_validate_code_invalid(self) -> None:
        '''Tests validate_code with invalid script logs messages as error and warning.'''
        self.mocks.editor.get_text.return_value = 'BAD_CMD'
        self.mocks.validator.validate_script.return_value = (
            False, ['[ERROR] Unknown token: BAD_CMD', '[WARNING] Unused variable']
        )
        self.handler.validate_code()
        self.assertEqual(self.mocks.console.append_log.call_count, 2)
        call_1 = self.mocks.console.append_log.call_args_list[0]
        call_2 = self.mocks.console.append_log.call_args_list[1]
        self.assertIn('Unknown token', call_1[0][0])
        self.assertEqual(call_1.kwargs['level'], 'error')
        self.assertIn('Unused variable', call_2[0][0])
        self.assertEqual(call_2.kwargs['level'], 'warning')

    def test_export_plan_to_editor(self) -> None:
        '''Tests export_plan_to_editor updates editor and logs waypoint count.'''
        self.mocks.plan_exporter.export_plan.return_value = 'GENERATED_DSL_CODE'
        self.handler.export_plan_to_editor()
        self.mocks.plan_exporter.export_plan.assert_called_once_with(
            plan=self.mocks.store
        )
        self.mocks.editor.set_text.assert_called_once_with('GENERATED_DSL_CODE')
        self.mocks.console.append_log.assert_called_once_with(
            'ℹ️ Exported 5 waypoints to SCARA DSL format.', level='info'
        )

    def test_preview_in_scaraemu_empty_code(self) -> None:
        '''Tests preview_in_scaraemu with empty editor logs warning and aborts.'''
        self.mocks.editor.get_text.return_value = '   '
        self.handler.preview_in_scaraemu()
        self.mocks.console.append_log.assert_called_once_with(
            '[WARN]: DSL editor is empty. Nothing to preview.', level='warning'
        )
        self.mocks.launcher.launch_preview.assert_not_called()

    def test_preview_in_scaraemu_success(self) -> None:
        '''Tests preview_in_scaraemu launches emulator and logs success.'''
        self.mocks.editor.get_text.return_value = 'MOVE P1'
        self.mocks.launcher.launch_preview.return_value = (
            True, 'Emulator launched successfully'
        )
        self.handler.preview_in_scaraemu()
        self.mocks.launcher.launch_preview.assert_called_once_with(
            dsl_code='MOVE P1'
        )
        self.mocks.console.append_log.assert_called_once_with(
            'Emulator launched successfully', level='success'
        )

    def test_preview_in_scaraemu_failure(self) -> None:
        '''Tests preview_in_scaraemu logs error when emulator launch fails.'''
        self.mocks.editor.get_text.return_value = 'MOVE P1'
        self.mocks.launcher.launch_preview.return_value = (
            False, 'SCARAEmu executable not found'
        )
        self.handler.preview_in_scaraemu()
        self.mocks.console.append_log.assert_called_once_with(
            'SCARAEmu executable not found', level='error'
        )


if __name__ == '__main__':
    main()
