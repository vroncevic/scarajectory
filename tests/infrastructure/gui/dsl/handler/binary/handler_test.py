# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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
    Unit tests for DslBinaryHandler component.
'''

from __future__ import annotations

from types import SimpleNamespace
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.infrastructure.gui.dsl.handler.binary.bundle import BinaryHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.binary.factory import DslBinaryHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.binary.handler import DslBinaryHandler
from scarajectory.infrastructure.gui.dsl.handler.binary.idelegate import IDslBinaryDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslBinaryHandler(TestCase):
    '''
        Test cases verifying DslBinaryHandler export and import workflows.
    '''

    mocks: SimpleNamespace
    handler: DslBinaryHandler

    def setUp(self) -> None:
        mock_compile_error_handler = MagicMock()
        mock_compile_error_handler.format_error.side_effect = (
            lambda error: f'{error}'
        )
        mock_decompile_error_handler = MagicMock()
        mock_decompile_error_handler.format_error.side_effect = (
            lambda error: f'{error}'
        )
        mock_diagnostics = MagicMock()
        mock_diagnostics.compile_error_handler = mock_compile_error_handler
        mock_diagnostics.decompile_error_handler = mock_decompile_error_handler

        self.mocks = SimpleNamespace(
            parent=MagicMock(),
            editor=MagicMock(),
            console=MagicMock(),
            compiler=MagicMock(),
            decompiler=MagicMock(),
            loader=MagicMock(),
            storer=MagicMock(),
            compile_error_handler=mock_compile_error_handler,
            decompile_error_handler=mock_decompile_error_handler,
            diagnostics=mock_diagnostics,
        )
        self.mocks.dsl = MagicMock()
        self.mocks.dsl.compiler = self.mocks.compiler
        self.mocks.dsl.decompiler = self.mocks.decompiler
        self.mocks.dsl.diagnostics = self.mocks.diagnostics

        bundle = BinaryHandlerBundle(
            parent=self.mocks.parent,
            editor=self.mocks.editor,
            console=self.mocks.console,
            dsl=self.mocks.dsl,
            loader=self.mocks.loader,
            storer=self.mocks.storer,
        )
        self.handler = DslBinaryHandlerFactory.create(bundle=bundle)

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance against IDslBinaryDelegate.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler, IDslBinaryDelegate)

    def test_get_version(self) -> None:
        '''
            Tests handler version string representation.

            :exceptions: None.
        '''
        self.assertEqual(self.handler.get_version(), '1.0.3')

    def test_export_empty_content(self) -> None:
        '''
            Tests that export when editor is empty logs a warning and returns.

            :exceptions: None.
        '''
        self.mocks.editor.get_text.return_value = '   '

        self.handler.export_binary_file()

        self.mocks.console.append_log.assert_called_once_with(
            '❌ Editor is empty. Nothing to export to binary.',
            level='warning',
        )
        self.mocks.compiler.compile.assert_not_called()

    @patch(
        'scarajectory.infrastructure.gui.dsl.handler.binary.handler.asksaveasfilename'
    )
    def test_export_cancelled(self, mock_save_dialog: MagicMock) -> None:
        '''
            Tests that cancelling save dialog aborts export.

            :exceptions: None.
        '''
        self.mocks.editor.get_text.return_value = 'MOVE LINEAR X=10.0 Y=20.0'
        mock_save_dialog.return_value = ''

        self.handler.export_binary_file()

        self.mocks.compiler.compile.assert_not_called()
        self.mocks.storer.save_binary_file.assert_not_called()

    @patch(
        'scarajectory.infrastructure.gui.dsl.handler.binary.handler.asksaveasfilename'
    )
    def test_export_success(self, mock_save_dialog: MagicMock) -> None:
        '''
            Tests successful compilation and saving of binary program.

            :exceptions: None.
        '''
        self.mocks.editor.get_text.return_value = 'MOVE LINEAR X=10.0 Y=20.0'
        mock_save_dialog.return_value = '/path/to/prog.bin'
        mock_program = MagicMock(spec=BinaryProgram)
        mock_program.steps = [MagicMock(), MagicMock()]
        mock_program.raw_bytes = b'\x01\x02\x03'
        self.mocks.compiler.compile.return_value = mock_program

        self.handler.export_binary_file()

        self.mocks.compiler.compile.assert_called_once_with(
            source='MOVE LINEAR X=10.0 Y=20.0'
        )
        self.mocks.storer.save_binary_file.assert_called_once_with(
            content=b'\x01\x02\x03',
            filepath='/path/to/prog.bin',
        )
        self.mocks.console.append_log.assert_called_once()
        call_args = self.mocks.console.append_log.call_args
        self.assertIn('Successfully exported binary program', call_args[0][0])
        self.assertEqual(call_args.kwargs['level'], 'success')

    @patch(
        'scarajectory.infrastructure.gui.dsl.handler.binary.handler.asksaveasfilename'
    )
    def test_export_compilation_failure(
        self, mock_save_dialog: MagicMock
    ) -> None:
        '''
            Tests that compiler error during export is logged to console.

            :exceptions: None.
        '''
        self.mocks.editor.get_text.return_value = 'INVALID COMMAND'
        mock_save_dialog.return_value = '/path/to/prog.bin'
        self.mocks.compiler.compile.side_effect = RuntimeError('Syntax error')

        self.handler.export_binary_file()

        self.mocks.storer.save_binary_file.assert_not_called()
        self.mocks.console.append_log.assert_called_once_with(
            '❌ Binary export failed: Syntax error',
            level='error',
        )

    @patch(
        'scarajectory.infrastructure.gui.dsl.handler.binary.handler.askopenfilename'
    )
    def test_import_cancelled(self, mock_open_dialog: MagicMock) -> None:
        '''
            Tests that cancelling open dialog aborts import.

            :exceptions: None.
        '''
        mock_open_dialog.return_value = ''

        self.handler.import_binary_file()

        self.mocks.loader.load_binary_file.assert_not_called()
        self.mocks.decompiler.decompile_bytes.assert_not_called()

    @patch(
        'scarajectory.infrastructure.gui.dsl.handler.binary.handler.askopenfilename'
    )
    def test_import_success(self, mock_open_dialog: MagicMock) -> None:
        '''
            Tests successful loading, decompilation, and loading into editor.

            :exceptions: None.
        '''
        mock_open_dialog.return_value = '/path/to/prog.bin'
        self.mocks.loader.load_binary_file.return_value = b'BIN_BYTES'
        self.mocks.decompiler.decompile_bytes.return_value = (
            'MOVE LINEAR X=10.0 Y=20.0'
        )

        self.handler.import_binary_file()

        self.mocks.loader.load_binary_file.assert_called_once_with(
            filepath='/path/to/prog.bin'
        )
        self.mocks.decompiler.decompile_bytes.assert_called_once_with(
            data=b'BIN_BYTES'
        )
        self.mocks.editor.set_text.assert_called_once_with(
            'MOVE LINEAR X=10.0 Y=20.0'
        )
        self.mocks.console.append_log.assert_called_once()
        call_args = self.mocks.console.append_log.call_args
        self.assertIn(
            'Successfully decompiled binary program', call_args[0][0]
        )
        self.assertEqual(call_args.kwargs['level'], 'success')

    @patch(
        'scarajectory.infrastructure.gui.dsl.handler.binary.handler.askopenfilename'
    )
    def test_import_decompilation_failure(
        self, mock_open_dialog: MagicMock
    ) -> None:
        '''
            Tests that decompiler or storage failure is logged to console.

            :exceptions: None.
        '''
        mock_open_dialog.return_value = '/path/to/corrupt.bin'
        self.mocks.loader.load_binary_file.side_effect = OSError(
            'Corrupted file'
        )

        self.handler.import_binary_file()

        self.mocks.editor.set_text.assert_not_called()
        self.mocks.console.append_log.assert_called_once_with(
            '❌ Binary decompile failed: Corrupted file',
            level='error',
        )


if __name__ == '__main__':
    main()
