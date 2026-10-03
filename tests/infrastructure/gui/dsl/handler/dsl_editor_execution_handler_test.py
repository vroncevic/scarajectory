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
    Unit tests for DslEditorExecutionHandler and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.handler.execution_handler import DslEditorExecutionHandler
from scarajectory.infrastructure.gui.dsl.handler.execution_handler_bundle import ExecutionHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.execution_handler_factory import DslEditorExecutionHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.iexecution_delegate import IDslExecutionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorExecutionHandler(TestCase):
    '''
        Test cases verifying DslEditorExecutionHandler compilation, validation, and preview.
    '''

    def setUp(self) -> None:
        self.mock_store = MagicMock()
        self.mock_store.count = 5
        self.mock_mutation = MagicMock()
        self.mock_dsl_service = MagicMock()
        self.mock_launcher = MagicMock()
        self.mock_editor = MagicMock()
        self.mock_console = MagicMock()

        bundle = ExecutionHandlerBundle(
            store=self.mock_store,
            mutation=self.mock_mutation,
            dsl_service=self.mock_dsl_service,
            launcher=self.mock_launcher,
            editor=self.mock_editor,
            console=self.mock_console,
        )
        self.handler: DslEditorExecutionHandler = (
            DslEditorExecutionHandlerFactory.create(bundle=bundle)
        )

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance against IDslExecutionDelegate.
        '''
        self.assertIsInstance(self.handler, IDslExecutionDelegate)

    def test_compile_to_plan_empty_source(self) -> None:
        '''
            Tests that compile_to_plan with empty editor logs error and aborts.
        '''
        self.mock_editor.get_text.return_value = '   \n  '
        self.handler.compile_to_plan()

        self.mock_console.log.assert_called_once_with(
            '❌ Editor is empty. Nothing to compile.',
            is_error=True,
        )
        self.mock_dsl_service.compile_script.assert_not_called()
        self.mock_mutation.set_waypoints.assert_not_called()

    def test_compile_to_plan_success(self) -> None:
        '''
            Tests successful compilation and plan synchronization.
        '''
        self.mock_editor.get_text.return_value = 'MOVE P1\nMOVE P2'
        mock_compiled = MagicMock()
        mock_compiled.count = 2
        mock_compiled.waypoints = [MagicMock(), MagicMock()]
        self.mock_dsl_service.compile_script.return_value = mock_compiled

        self.handler.compile_to_plan()

        self.mock_dsl_service.compile_script.assert_called_once_with(
            source='MOVE P1\nMOVE P2'
        )
        self.mock_mutation.set_waypoints.assert_called_once_with(
            mock_compiled.waypoints
        )
        self.mock_console.log.assert_called_once()
        log_msg: str = self.mock_console.log.call_args[0][0]
        is_error: bool = self.mock_console.log.call_args.kwargs['is_error']
        self.assertIn('Successfully compiled', log_msg)
        self.assertFalse(is_error)

    def test_compile_to_plan_error(self) -> None:
        '''
            Tests compile_to_plan handles compilation exceptions gracefully.
        '''
        self.mock_editor.get_text.return_value = 'INVALID SYNTAX'
        self.mock_dsl_service.compile_script.side_effect = ValueError('Syntax error at line 1')

        self.handler.compile_to_plan()

        self.mock_console.log.assert_called_once()
        log_msg: str = self.mock_console.log.call_args[0][0]
        is_error: bool = self.mock_console.log.call_args.kwargs['is_error']
        self.assertIn('Compilation error: Syntax error at line 1', log_msg)
        self.assertTrue(is_error)

    def test_validate_code_empty(self) -> None:
        '''
            Tests validate_code with empty text logs error and returns early.
        '''
        self.mock_editor.get_text.return_value = ''
        self.handler.validate_code()

        self.mock_console.log.assert_called_once_with(
            '❌ Editor is empty. Nothing to validate.',
            is_error=True,
        )
        self.mock_dsl_service.validate_script.assert_not_called()

    def test_validate_code_valid(self) -> None:
        '''
            Tests validate_code with valid script logs messages as non-error.
        '''
        self.mock_editor.get_text.return_value = 'MOVE P1'
        self.mock_dsl_service.validate_script.return_value = (True, ['All syntax valid'])

        self.handler.validate_code()

        self.mock_dsl_service.validate_script.assert_called_once_with(
            source='MOVE P1'
        )
        self.mock_console.log.assert_called_once_with(
            'All syntax valid',
            is_error=False,
        )

    def test_validate_code_invalid(self) -> None:
        '''
            Tests validate_code with invalid script logs messages as error.
        '''
        self.mock_editor.get_text.return_value = 'BAD_CMD'
        self.mock_dsl_service.validate_script.return_value = (False, ['Unknown token: BAD_CMD'])

        self.handler.validate_code()

        self.mock_console.log.assert_called_once_with(
            'Unknown token: BAD_CMD',
            is_error=True,
        )

    def test_export_plan_to_editor(self) -> None:
        '''
            Tests export_plan_to_editor updates editor and logs waypoint count.
        '''
        self.mock_dsl_service.export_plan.return_value = 'GENERATED_DSL_CODE'

        self.handler.export_plan_to_editor()

        self.mock_dsl_service.export_plan.assert_called_once_with(
            plan=self.mock_store
        )
        self.mock_editor.set_text.assert_called_once_with('GENERATED_DSL_CODE')
        self.mock_console.log.assert_called_once_with(
            'ℹ️ Exported 5 waypoints to SCARA DSL format.',
            is_error=False,
        )

    def test_preview_in_scaraemu_empty_code(self) -> None:
        '''
            Tests preview_in_scaraemu with empty editor logs warning and aborts.
        '''
        self.mock_editor.get_text.return_value = '   '
        self.handler.preview_in_scaraemu()

        self.mock_console.log.assert_called_once_with(
            '[WARN]: DSL editor is empty. Nothing to preview.',
            is_error=True,
        )
        self.mock_launcher.launch_preview.assert_not_called()

    def test_preview_in_scaraemu_success(self) -> None:
        '''
            Tests preview_in_scaraemu launches emulator and logs success.
        '''
        self.mock_editor.get_text.return_value = 'MOVE P1'
        self.mock_launcher.launch_preview.return_value = (True, 'Emulator launched successfully')

        self.handler.preview_in_scaraemu()

        self.mock_launcher.launch_preview.assert_called_once_with(
            dsl_code='MOVE P1'
        )
        self.mock_console.log.assert_called_once_with(
            'Emulator launched successfully',
            is_error=False,
        )

    def test_preview_in_scaraemu_failure(self) -> None:
        '''
            Tests preview_in_scaraemu logs error when emulator launch fails.
        '''
        self.mock_editor.get_text.return_value = 'MOVE P1'
        self.mock_launcher.launch_preview.return_value = (False, 'SCARAEmu executable not found')

        self.handler.preview_in_scaraemu()

        self.mock_console.log.assert_called_once_with(
            'SCARAEmu executable not found',
            is_error=True,
        )


if __name__ == '__main__':
    main()
