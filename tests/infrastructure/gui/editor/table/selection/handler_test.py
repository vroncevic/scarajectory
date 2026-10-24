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
    Unit tests for TableSelectionHandler component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.editor.table.selection.handler import TableSelectionHandler
from scarajectory.infrastructure.gui.editor.table.selection.ihandler import ITableSelectionHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TableSelectionHandlerTestCase(TestCase):
    '''
        Test cases for TableSelectionHandler.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies conformance to ITableSelectionHandler.
                | test_handle_selection_updates_coordinator - Verifies index update.
                | test_handle_selection_empty_values - Verifies empty row handling.
                | test_handle_selection_invalid_value - Verifies invalid value handling.
                | test_constants_and_version - Verifies ClassVar constants and version string.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies TableSelectionHandler conforms to ITableSelectionHandler structurally.

            :exceptions: None.
        '''
        handler = TableSelectionHandler()
        self.assertIsInstance(handler, ITableSelectionHandler)

    def test_handle_selection_updates_coordinator(self) -> None:
        '''
            Verifies handle_selection extracts row index and updates coordinator.

            :exceptions: None.
        '''
        mock_tree = MagicMock()
        mock_tree.selection.return_value = ('item1',)
        mock_tree.item.return_value = ['3', '10.0', '20.0']
        mock_selection = MagicMock()

        handler = TableSelectionHandler()
        handler.handle_selection(mock_tree, mock_selection)
        mock_selection.set_selected_index.assert_called_once_with(2)

    def test_handle_selection_empty_values(self) -> None:
        '''
            Verifies handle_selection handles empty item values.

            :exceptions: None.
        '''
        mock_tree = MagicMock()
        mock_tree.selection.return_value = ('item1',)
        mock_tree.item.return_value = []
        mock_selection = MagicMock()

        handler = TableSelectionHandler()
        handler.handle_selection(mock_tree, mock_selection)
        mock_selection.set_selected_index.assert_not_called()

    def test_handle_selection_invalid_value(self) -> None:
        '''
            Verifies handle_selection handles invalid non-integer values gracefully.

            :exceptions: None.
        '''
        mock_tree = MagicMock()
        mock_tree.selection.return_value = ('item1',)
        mock_tree.item.return_value = ['invalid_number']
        mock_selection = MagicMock()

        handler = TableSelectionHandler()
        handler.handle_selection(mock_tree, mock_selection)
        mock_selection.set_selected_index.assert_not_called()

    def test_constants_and_version(self) -> None:
        '''
            Verifies ClassVar constants and version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(TableSelectionHandler.VAL_INDEX_COL, 0)
        self.assertEqual(TableSelectionHandler.INDEX_OFFSET, 1)
        self.assertEqual(TableSelectionHandler.PROP_VALUES, 'values')
        handler = TableSelectionHandler()
        ver: str = handler.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
