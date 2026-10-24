# -*- coding: UTF-8 -*-

'''
Module
    catalog_test.py
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
    Unit tests for DslExampleCatalog component.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.infrastructure.gui.dsl.catalog.catalog import DslExampleCatalog
from scarajectory.infrastructure.gui.dsl.catalog.icatalog import IDslExampleCatalog

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslExampleCatalogTestCase(TestCase):
    '''
        Unit test suite validating DslExampleCatalog functionality.

        It defines:

            :methods:
                | test_protocol_compliance - Validates structural protocol satisfaction.
                | test_examples_dir - Tests directory property getter.
                | test_get_example_files - Tests discovering .scara files.
                | test_load_example_content - Tests loading content from storage.
                | test_load_missing_example - Tests fallback for non-existent file.
                | test_get_version - Tests component version string.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Tests that DslExampleCatalog satisfies IDslExampleCatalog structurally.

            :exceptions: None.
        '''
        loader = MagicMock(spec=IPlanLoader)
        catalog = DslExampleCatalog(examples_dir=Path('/tmp'), loader=loader)
        self.assertIsInstance(catalog, IDslExampleCatalog)

    def test_examples_dir(self) -> None:
        '''
            Tests directory getter returns path instance.

            :exceptions: None.
        '''
        path = Path('/tmp')
        loader = MagicMock(spec=IPlanLoader)
        catalog = DslExampleCatalog(examples_dir=path, loader=loader)
        self.assertEqual(catalog.examples_dir(), path)

    def test_get_example_files(self) -> None:
        '''
            Tests discovering .scara files in existing directory.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / 'alpha.scara').write_text('content', encoding='utf-8')
            (tmp_path / 'beta.scara').write_text('content', encoding='utf-8')
            (tmp_path / 'other.txt').write_text('content', encoding='utf-8')

            loader = MagicMock(spec=IPlanLoader)
            catalog = DslExampleCatalog(examples_dir=tmp_path, loader=loader)
            files = catalog.get_example_files()
            self.assertEqual(files, ('alpha.scara', 'beta.scara'))

    def test_load_example_content(self) -> None:
        '''
            Tests loading content from storage when file exists.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            file_path = tmp_path / 'test.scara'
            file_path.write_text('DSL code', encoding='utf-8')

            loader = MagicMock(spec=IPlanLoader)
            loader.load_text_file.return_value = 'DSL code'

            catalog = DslExampleCatalog(examples_dir=tmp_path, loader=loader)
            content = catalog.load_example_content('test.scara')
            self.assertEqual(content, 'DSL code')
            loader.load_text_file.assert_called_once_with(filepath=str(file_path))

            loader.load_text_file.side_effect = OSError('Read failure')
            self.assertEqual(catalog.load_example_content('test.scara'), '')

    def test_load_missing_example(self) -> None:
        '''
            Tests loading non-existent example file returns empty string.

            :exceptions: None.
        '''
        loader = MagicMock(spec=IPlanLoader)
        catalog = DslExampleCatalog(
            examples_dir=Path('/non_existent_dir_12345'),
            loader=loader,
        )
        self.assertEqual(catalog.get_example_files(), ())
        self.assertEqual(catalog.load_example_content('missing.scara'), '')

    def test_get_version(self) -> None:
        '''
            Tests component version getter.

            :exceptions: None.
        '''
        loader = MagicMock(spec=IPlanLoader)
        catalog = DslExampleCatalog(examples_dir=Path('/tmp'), loader=loader)
        self.assertEqual(catalog.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
