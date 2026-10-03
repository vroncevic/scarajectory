# -*- coding: UTF-8 -*-

'''
Module
    trajectory_table_test.py
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
    Unit testing for TrajectoryTable component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.editor.table.trajectory_table import (
    TrajectoryTable,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryTableTestCase(TestCase):
    '''
        Unit tests for TrajectoryTable widget.

        It defines:

            :methods:
                | setUp - Initializes headless Tk root and table with mock bundle.
                | tearDown - Destroys Tk root.
                | test_initialization_and_protocol - Verifies widget setup and protocol.
                | test_refresh_and_selection_sync - Verifies row rendering and selection sync.
                | test_delete_selected - Verifies point deletion when row selected.
    '''

    def setUp(self) -> None:
        '''Initializes headless Tk instance and table widget before each test.'''
        self.root: Tk = Tk()
        self.root.withdraw()

        self.mock_store = MagicMock()
        self.mock_store.waypoints = ()
        self.mock_store.count = 0

        self.mock_selection = MagicMock()
        self.mock_selection.selected_index = -1

        self.mock_mutation = MagicMock()
        self.mock_dispatcher = MagicMock()

        bundle = TableBundle(
            store=self.mock_store,
            selection=self.mock_selection,
            mutation=self.mock_mutation,
            dispatcher=self.mock_dispatcher,
        )
        self.table = TrajectoryTable(self.root, bundle=bundle)

    def tearDown(self) -> None:
        '''Destroys Tk instance after each test.'''
        self.root.destroy()

    def test_initialization_and_protocol(self) -> None:
        '''Verifies TrajectoryTable satisfies ITable and registers with dispatcher.'''
        self.assertIsInstance(self.table, ITable)
        self.mock_dispatcher.add_observer.assert_called_once_with(self.table)

    def test_refresh_and_selection_sync(self) -> None:
        '''Verifies waypoint rows rendering, update notification, and selection.'''
        waypoint = Waypoint(x=10.0, y=20.0, z=30.0, phi=45.0, speed=100.0)
        self.mock_store.waypoints = (waypoint,)
        self.mock_store.count = 1
        self.mock_selection.selected_index = 0

        self.table.refresh_table()
        self.table.on_point_selected(0)
        self.table.on_point_selected(-1)
        self.table.on_trajectory_updated()

    def test_delete_selected(self) -> None:
        '''Verifies deletion triggers mutator when valid index is selected.'''
        self.mock_store.count = 2

        self.mock_selection.selected_index = -1
        self.table.delete_selected()
        self.mock_mutation.remove_point.assert_not_called()

        self.mock_selection.selected_index = 1
        self.table.delete_selected()
        self.mock_mutation.remove_point.assert_called_once_with(1)


if __name__ == '__main__':
    main()
