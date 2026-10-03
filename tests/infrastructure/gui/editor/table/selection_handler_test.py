# -*- coding: UTF-8 -*-

'''
Module
    selection_handler_test.py
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

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.editor.table.selection_handler import TableSelectionHandler
from scarajectory.infrastructure.gui.editor.table.selection_handler_factory import TableSelectionHandlerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTableSelectionHandler(TestCase):
    '''
        Test cases for TableSelectionHandler.
    '''

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies factory creates TableSelectionHandler.
        '''
        handler = TableSelectionHandlerFactory.create()
        self.assertIsInstance(handler, TableSelectionHandler)

    def test_handle_selection_updates_coordinator(self) -> None:
        '''
            Verifies handle_selection extracts row index and updates coordinator.
        '''
        mock_tree = MagicMock()
        mock_tree.selection.return_value = ('item1',)
        mock_tree.item.return_value = ['3', '10.0', '20.0']
        mock_selection = MagicMock()

        handler = TableSelectionHandler()
        handler.handle_selection(mock_tree, mock_selection)

        mock_selection.set_selected_index.assert_called_once_with(2)
