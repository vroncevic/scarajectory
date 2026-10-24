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
    Unit tests for TableResizeHandler component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.editor.table.resize.handler import TableResizeHandler
from scarajectory.infrastructure.gui.editor.table.resize.ihandler import ITableResizeHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TableResizeHandlerTestCase(TestCase):
    '''
        Test cases for TableResizeHandler.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies conformance to ITableResizeHandler.
                | test_handle_resize_zero_width - Verifies ignore of non-positive width.
                | test_handle_resize_valid_width - Verifies proportional column resizing.
                | test_constants_and_version - Verifies ClassVar constants and version string.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies TableResizeHandler conforms to ITableResizeHandler structurally.

            :exceptions: None.
        '''
        handler = TableResizeHandler()
        self.assertIsInstance(handler, ITableResizeHandler)

    def test_handle_resize_zero_width(self) -> None:
        '''
            Verifies handle_resize ignores non-positive width events.

            :exceptions: None.
        '''
        mock_tree = MagicMock()
        mock_event = MagicMock()
        mock_event.width = 0

        handler = TableResizeHandler()
        handler.handle_resize(mock_tree, mock_event)
        mock_tree.column.assert_not_called()

    def test_handle_resize_valid_width(self) -> None:
        '''
            Verifies handle_resize updates column widths proportionally.

            :exceptions: None.
        '''
        mock_tree = MagicMock()
        mock_event = MagicMock()
        mock_event.width = 1000

        handler = TableResizeHandler()
        handler.handle_resize(mock_tree, mock_event)
        self.assertEqual(mock_tree.column.call_count, 7)

    def test_constants_and_version(self) -> None:
        '''
            Verifies ClassVar constants and version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(TableResizeHandler.OFFSET_WIDTH, 24)
        self.assertEqual(TableResizeHandler.MIN_TOTAL_WIDTH, 450)
        self.assertEqual(TableResizeHandler.ATTR_WIDTH, 'width')
        self.assertEqual(TableResizeHandler.DEFAULT_WIDTH, 0)
        handler = TableResizeHandler()
        ver: str = handler.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
