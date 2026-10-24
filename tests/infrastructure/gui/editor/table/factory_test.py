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
    Unit testing for TrajectoryTableFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.factory import TrajectoryTableFactory
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.editor.table.resize.ihandler import ITableResizeHandler
from scarajectory.infrastructure.gui.editor.table.selection.ihandler import ITableSelectionHandler
from scarajectory.infrastructure.gui.editor.table.table import TrajectoryTable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryTableFactoryTestCase(TestCase):
    '''
        Unit tests for TrajectoryTableFactory.

        It defines:

            :methods:
                | test_factory_version - Verifies factory version string.
                | test_factory_creates_instance - Verifies factory creates valid TrajectoryTable.
                | test_factory_create_with_collaborators - Verifies creation with explicit handlers.
    '''

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        ver: str = TrajectoryTableFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies TrajectoryTableFactory instantiates valid TrajectoryTable.

            :exceptions: None.
        '''
        try:
            root = Tk()
            root.withdraw()
        except Exception:
            return

        mock_store = MagicMock()
        mock_store.waypoints = ()
        mock_store.count = 0
        bundle = TableBundle(
            store=mock_store,
            selection=MagicMock(),
            mutation=MagicMock(),
            dispatcher=MagicMock(),
            validator=MagicMock(),
        )

        try:
            table: TrajectoryTable = TrajectoryTableFactory.create(
                root, bundle=bundle
            )
            self.assertIsInstance(table, TrajectoryTable)
            self.assertIsInstance(table, ITable)
        finally:
            root.destroy()

    def test_factory_create_with_collaborators(self) -> None:
        '''
            Verifies creation with explicit handler collaborators.

            :exceptions: None.
        '''
        try:
            root = Tk()
            root.withdraw()
        except Exception:
            return

        mock_store = MagicMock()
        mock_store.waypoints = ()
        mock_store.count = 0
        bundle = TableBundle(
            store=mock_store,
            selection=MagicMock(),
            mutation=MagicMock(),
            dispatcher=MagicMock(),
            validator=MagicMock(),
        )

        mock_resize = MagicMock(spec=ITableResizeHandler)
        mock_sel = MagicMock(spec=ITableSelectionHandler)

        try:
            table: TrajectoryTable = (
                TrajectoryTableFactory.create_with_collaborators(
                    root,
                    bundle=bundle,
                    resize_handler=mock_resize,
                    selection_handler=mock_sel,
                )
            )
            self.assertIsInstance(table, TrajectoryTable)
            self.assertIsInstance(table, ITable)
        finally:
            root.destroy()


if __name__ == '__main__':
    main()
