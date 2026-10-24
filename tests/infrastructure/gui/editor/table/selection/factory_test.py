# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for TableSelectionHandlerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.editor.table.selection.factory import TableSelectionHandlerFactory
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


class TableSelectionHandlerFactoryTestCase(TestCase):
    '''
        Unit tests for TableSelectionHandlerFactory.

        It defines:

            :methods:
                | test_factory_version - Verifies factory version string.
                | test_factory_creates_instance - Verifies factory creates valid instance.
    '''

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        ver: str = TableSelectionHandlerFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies TableSelectionHandlerFactory instantiates valid handler.

            :exceptions: None.
        '''
        handler: ITableSelectionHandler = TableSelectionHandlerFactory.create()
        self.assertIsInstance(handler, ITableSelectionHandler)
        self.assertIsInstance(handler, TableSelectionHandler)


if __name__ == '__main__':
    main()
