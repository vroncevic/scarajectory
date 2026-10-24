# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for FileHandlerBundle parameter container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.handler.file.bundle import FileHandlerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFileHandlerBundle(TestCase):
    '''
        Tests verifying FileHandlerBundle fields and immutability.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Tests bundle fields initialization.

            :exceptions: None.
        '''
        mock_parent = MagicMock()
        mock_editor = MagicMock()
        mock_console = MagicMock()
        mock_catalog = MagicMock()
        mock_doc_manager = MagicMock()

        bundle = FileHandlerBundle(
            parent=mock_parent,
            editor=mock_editor,
            console=mock_console,
            catalog=mock_catalog,
            document_manager=mock_doc_manager,
        )

        self.assertIs(bundle.parent, mock_parent)
        self.assertIs(bundle.editor, mock_editor)
        self.assertIs(bundle.console, mock_console)
        self.assertIs(bundle.catalog, mock_catalog)
        self.assertIs(bundle.document_manager, mock_doc_manager)


if __name__ == '__main__':
    main()
