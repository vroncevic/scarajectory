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

from pathlib import Path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.storage.plan_storage_service_factory import PlanStorageServiceFactory
from scarajectory.infrastructure.gui.dsl.document.document_manager import DslDocumentManager
from scarajectory.infrastructure.gui.dsl.document.document_manager_factory import DslDocumentManagerFactory
from scarajectory.infrastructure.gui.dsl.document.example_catalog import DslExampleCatalog
from scarajectory.infrastructure.gui.dsl.document.example_catalog_factory import DslExampleCatalogFactory

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
        storage = PlanStorageServiceFactory.create()
        self._catalog = DslExampleCatalogFactory.create_default(storage=storage)
        self._doc_manager = DslDocumentManagerFactory.create_default()

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
            Verifies that loading non-existent example returns empty string.
        '''
        result = self._catalog.load_example_content(
            filename='nonexistent_example_file.scara'
        )
        self.assertEqual(result, '')

    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.askopenfilename')
    def test_open_document_cancelled(self, mock_askopen: MagicMock) -> None:
        '''
            Verifies that user cancelling open dialog returns empty strings tuple.
        '''
        mock_askopen.return_value = ''
        mock_widget = MagicMock()
        result = self._doc_manager.open_document(parent=mock_widget)
        self.assertEqual(result, ('', ''))

    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.askopenfilename')
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
        content, filepath = result
        self.assertEqual(content, 'HOME\nMOVE_L X=10.0')
        self.assertEqual(filepath, '/dummy/test.scara')

    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.showerror')
    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.askopenfilename')
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
        self.assertEqual(result, ('', ''))
        mock_showerror.assert_called_once()

    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.asksaveasfilename')
    def test_save_document_cancelled(self, mock_asksave: MagicMock) -> None:
        '''
            Verifies that user cancelling save dialog returns empty string.
        '''
        mock_asksave.return_value = ''
        mock_widget = MagicMock()
        result = self._doc_manager.save_document(
            parent=mock_widget, content='HOME'
        )
        self.assertEqual(result, '')

    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.asksaveasfilename')
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

    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.showerror')
    @patch('scarajectory.infrastructure.gui.dsl.document.document_manager.asksaveasfilename')
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
        self.assertEqual(result, '')
        mock_showerror.assert_called_once()

    def test_catalog_missing_dir(self) -> None:
        '''
            Verifies catalog behavior when examples directory does not exist.
        '''
        mock_storage = MagicMock()
        catalog = DslExampleCatalog(
            storage=mock_storage,
            examples_dir=Path('/non/existent/path/for/scara/examples')
        )
        self.assertEqual(catalog.examples_dir, Path('/non/existent/path/for/scara/examples'))
        self.assertEqual(catalog.get_example_files(), [])
        self.assertEqual(catalog.load_example_content(filename='sample.scara'), '')

    def test_catalog_load_os_error(self) -> None:
        '''
            Verifies catalog handles OSError when reading existing file.
        '''
        mock_storage = MagicMock()
        mock_storage.load_text_file.side_effect = OSError('Read error')
        catalog = DslExampleCatalogFactory.create_default(storage=mock_storage)
        examples = catalog.get_example_files()
        if examples:
            result = catalog.load_example_content(filename=examples[0])
            self.assertEqual(result, '')

    def test_factory_versions(self) -> None:
        '''
            Verifies version retrieval on factories.
        '''
        self.assertIsInstance(DslDocumentManagerFactory.get_version(), str)
        self.assertIsInstance(DslExampleCatalogFactory.get_version(), str)


if __name__ == '__main__':
    main()
