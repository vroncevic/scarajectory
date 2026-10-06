# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_file_handler_test.py
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
    Unit tests for DslEditorFileHandler and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.handler.file_handler import DslEditorFileHandler
from scarajectory.infrastructure.gui.dsl.handler.file_handler_bundle import FileHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.file_handler_factory import DslEditorFileHandlerFactory
from scarajectory.infrastructure.gui.dsl.handler.ifile_delegate import IDslFileDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorFileHandler(TestCase):
    '''
        Test cases verifying DslEditorFileHandler open, save, and example loading operations.
    '''

    def setUp(self) -> None:
        self.mock_parent = MagicMock()
        self.mock_editor = MagicMock()
        self.mock_console = MagicMock()
        self.mock_catalog = MagicMock()
        self.mock_catalog.examples_dir = '/path/to/workspace'
        self.mock_doc_manager = MagicMock()

        bundle = FileHandlerBundle(
            parent=self.mock_parent,
            editor=self.mock_editor,
            console=self.mock_console,
            catalog=self.mock_catalog,
            document_manager=self.mock_doc_manager,
        )
        self.handler: DslEditorFileHandler = (
            DslEditorFileHandlerFactory.create(bundle=bundle)
        )

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance against IDslFileDelegate.
        '''
        self.assertIsInstance(self.handler, IDslFileDelegate)
        self.assertIsInstance(DslEditorFileHandlerFactory.get_version(), str)

    def test_open_file_success(self) -> None:
        '''
            Tests open_file loads document content into editor and logs status.
        '''
        self.mock_doc_manager.open_document.return_value = (
            'CONTENT_FROM_FILE',
            '/path/to/script.scara',
        )

        self.handler.open_file()

        self.mock_doc_manager.open_document.assert_called_once_with(
            parent=self.mock_parent,
            initial_dir='/path/to/workspace',
        )
        self.mock_editor.set_text.assert_called_once_with('CONTENT_FROM_FILE')
        self.mock_console.log.assert_called_once_with(
            'ℹ️ Loaded file: /path/to/script.scara',
            is_error=False,
        )

    def test_open_file_cancelled(self) -> None:
        '''
            Tests open_file when user cancels dialog does not update editor or log.
        '''
        self.mock_doc_manager.open_document.return_value = ('', '')

        self.handler.open_file()

        self.mock_editor.set_text.assert_not_called()
        self.mock_console.log.assert_not_called()

    def test_save_file_success(self) -> None:
        '''
            Tests save_file passes editor content to document manager and logs status.
        '''
        self.mock_editor.get_text.return_value = 'CODE_TO_SAVE'
        self.mock_doc_manager.save_document.return_value = '/path/to/saved.scara'

        self.handler.save_file()

        self.mock_doc_manager.save_document.assert_called_once_with(
            parent=self.mock_parent,
            content='CODE_TO_SAVE',
            initial_dir='/path/to/workspace',
        )
        self.mock_console.log.assert_called_once_with(
            'ℹ️ Saved file: /path/to/saved.scara',
            is_error=False,
        )

    def test_save_file_cancelled(self) -> None:
        '''
            Tests save_file when user cancels dialog does not log success status.
        '''
        self.mock_editor.get_text.return_value = 'CODE_TO_SAVE'
        self.mock_doc_manager.save_document.return_value = ''

        self.handler.save_file()

        self.mock_console.log.assert_not_called()

    def test_on_example_selected_found(self) -> None:
        '''
            Tests on_example_selected loads content from catalog when present.
        '''
        self.mock_catalog.load_example_content.return_value = 'EXAMPLE_SCRIPT_BODY'

        self.handler.on_example_selected('pick_place.scara')

        self.mock_catalog.load_example_content.assert_called_once_with(
            filename='pick_place.scara'
        )
        self.mock_editor.set_text.assert_called_once_with('EXAMPLE_SCRIPT_BODY')
        self.mock_console.log.assert_called_once_with(
            'ℹ️ Loaded example: pick_place.scara',
            is_error=False,
        )

    def test_on_example_selected_fallback_to_default(self) -> None:
        '''
            Tests on_example_selected loads default demonstration script when file not found.
        '''
        self.mock_catalog.load_example_content.return_value = ''
        self.mock_catalog.get_default_script.return_value = 'DEFAULT_DEMO_SCRIPT'

        self.handler.on_example_selected('non_existent.scara')

        self.mock_catalog.get_default_script.assert_called_once()
        self.mock_editor.set_text.assert_called_once_with('DEFAULT_DEMO_SCRIPT')
        self.mock_console.log.assert_called_once_with(
            'ℹ️ Demonstration SCARA DSL script loaded.',
            is_error=False,
        )

    def test_on_example_selected_empty_name_loads_default(self) -> None:
        '''
            Tests on_example_selected with empty filename immediately falls back to default.
        '''
        self.mock_catalog.get_default_script.return_value = 'DEFAULT_DEMO_SCRIPT'

        self.handler.on_example_selected('')

        self.mock_catalog.load_example_content.assert_not_called()
        self.mock_catalog.get_default_script.assert_called_once()
        self.mock_editor.set_text.assert_called_once_with('DEFAULT_DEMO_SCRIPT')


if __name__ == '__main__':
    main()
