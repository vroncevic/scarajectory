# -*- coding: UTF-8 -*-

'''
Module
    dsl_document_manager_test.py
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
    Unit tests for DslExampleCatalog and DslDocumentManager components.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

pkg_dir: str = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.infrastructure.gui.dsl.dsl_document_manager import (
    DslDocumentManager,
)
from scarajectory.infrastructure.gui.dsl.dsl_example_catalog import (
    DslExampleCatalog,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslDocumentManager(TestCase):
    '''
        Test suite validating DslExampleCatalog and DslDocumentManager operations.
    '''

    def setUp(self) -> None:
        '''
            Prepares catalog and document manager instances for testing.
        '''
        self._catalog = DslExampleCatalog()
        self._doc_manager = DslDocumentManager()

    def test_catalog_default_script(self) -> None:
        '''
            Verifies default script content and basic commands.
        '''
        script = self._catalog.get_default_script()
        self.assertIn('CONFIG ELBOW', script)
        self.assertIn('HOME', script)
        self.assertIn('JUMP', script)

    def test_catalog_example_files_discovery(self) -> None:
        '''
            Verifies that example files are discovered and sorted.
        '''
        files = self._catalog.get_example_files()
        self.assertIsInstance(files, list)

    def test_catalog_load_nonexistent_example(self) -> None:
        '''
            Verifies that loading non-existent example returns None.
        '''
        result = self._catalog.load_example_content(
            filename='nonexistent_example_file.scara'
        )
        self.assertIsNone(result)

    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.askopenfilename')
    def test_open_document_cancelled(self, mock_askopen: MagicMock) -> None:
        '''
            Verifies that user cancelling open dialog returns None.
        '''
        mock_askopen.return_value = ''
        mock_widget = MagicMock()
        result = self._doc_manager.open_document(parent=mock_widget)
        self.assertIsNone(result)

    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.askopenfilename')
    def test_open_document_success(self, mock_askopen: MagicMock) -> None:
        '''
            Verifies successful script file loading.
        '''
        mock_askopen.return_value = '/dummy/test.scara'
        mock_storage = MagicMock()
        mock_storage.load_text_file.return_value = 'HOME\nMOVE_L X=10.0'
        manager = DslDocumentManager(storage=mock_storage)
        mock_widget = MagicMock()

        result = manager.open_document(parent=mock_widget)
        self.assertIsNotNone(result)
        if result is not None:
            content, filepath = result
            self.assertEqual(content, 'HOME\nMOVE_L X=10.0')
            self.assertEqual(filepath, '/dummy/test.scara')

    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.showerror')
    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.askopenfilename')
    def test_open_document_os_error(
        self, mock_askopen: MagicMock, mock_showerror: MagicMock
    ) -> None:
        '''
            Verifies graceful handling of OSError during document open.
        '''
        mock_askopen.return_value = '/dummy/error.scara'
        mock_storage = MagicMock()
        mock_storage.load_text_file.side_effect = OSError('Disk read error')
        manager = DslDocumentManager(storage=mock_storage)
        mock_widget = MagicMock()

        result = manager.open_document(parent=mock_widget)
        self.assertIsNone(result)
        mock_showerror.assert_called_once()

    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.asksaveasfilename')
    def test_save_document_cancelled(self, mock_asksave: MagicMock) -> None:
        '''
            Verifies that user cancelling save dialog returns None.
        '''
        mock_asksave.return_value = ''
        mock_widget = MagicMock()
        result = self._doc_manager.save_document(
            parent=mock_widget, content='HOME'
        )
        self.assertIsNone(result)

    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.asksaveasfilename')
    def test_save_document_success(self, mock_asksave: MagicMock) -> None:
        '''
            Verifies successful script saving.
        '''
        mock_asksave.return_value = '/dummy/out.scara'
        mock_storage = MagicMock()
        manager = DslDocumentManager(storage=mock_storage)
        mock_widget = MagicMock()

        result = manager.save_document(
            parent=mock_widget, content='HOME\nMOVE_L X=10.0'
        )
        self.assertEqual(result, '/dummy/out.scara')
        mock_storage.save_text_file.assert_called_once_with(
            'HOME\nMOVE_L X=10.0', '/dummy/out.scara'
        )

    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.showerror')
    @patch('scarajectory.infrastructure.gui.dsl.dsl_document_manager.asksaveasfilename')
    def test_save_document_os_error(
        self, mock_asksave: MagicMock, mock_showerror: MagicMock
    ) -> None:
        '''
            Verifies graceful error handling on save file error.
        '''
        mock_asksave.return_value = '/dummy/out.scara'
        mock_storage = MagicMock()
        mock_storage.save_text_file.side_effect = OSError('Write permission denied')
        manager = DslDocumentManager(storage=mock_storage)
        mock_widget = MagicMock()

        result = manager.save_document(
            parent=mock_widget, content='HOME'
        )
        self.assertIsNone(result)
        mock_showerror.assert_called_once()


if __name__ == '__main__':
    main()
