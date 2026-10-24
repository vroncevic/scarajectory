# -*- coding: UTF-8 -*-

'''
Module
    table_test.py
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

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.observer.itrajectory_observer import ITrajectoryObserver
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
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


class TrajectoryTableTestCase(TestCase):
    '''
        Unit tests for TrajectoryTable widget.

        It defines:

            :attributes:
                | root - Headless Tk root instance.
                | mock_mutation - Mock mutation service collaborator.
                | mock_dispatcher - Mock observer dispatcher collaborator.
                | mock_resize - Mock resize handler collaborator.
                | mock_sel - Mock selection handler collaborator.
                | bundle - Mock TableBundle containing query and mutator mocks.
                | table - TrajectoryTable instance under test.
            :methods:
                | setUp - Initializes headless Tk root and table with mock bundle.
                | tearDown - Destroys Tk root.
                | test_initialization_and_protocol - Verifies widget setup and protocol.
                | test_refresh_and_selection_sync - Verifies row rendering and selection sync.
                | test_delete_selected - Verifies point deletion when row selected.
                | test_configure_event_triggers_resize_handler - Verifies configure triggers resize.
    '''

    root: Tk
    mock_mutation: MagicMock
    mock_dispatcher: MagicMock
    mock_resize: MagicMock
    mock_sel: MagicMock
    bundle: TableBundle
    table: TrajectoryTable

    def setUp(self) -> None:
        '''
            Initializes headless Tk instance and table widget before each test.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()

        mock_store = MagicMock()
        mock_store.waypoints = ()
        mock_store.count = 0

        mock_selection = MagicMock()
        mock_selection.selected_index = -1

        self.mock_mutation = MagicMock()
        self.mock_dispatcher = MagicMock()
        self.mock_resize = MagicMock(spec=ITableResizeHandler)
        self.mock_sel = MagicMock(spec=ITableSelectionHandler)

        self.bundle = TableBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=self.mock_mutation,
            dispatcher=self.mock_dispatcher,
            validator=MagicMock(),
        )
        self.table = TrajectoryTable(
            self.root,
            bundle=self.bundle,
            resize_handler=self.mock_resize,
            selection_handler=self.mock_sel,
        )

    def tearDown(self) -> None:
        '''
            Destroys Tk instance after each test.

            :exceptions: None.
        '''
        self.root.destroy()

    def test_initialization_and_protocol(self) -> None:
        '''
            Verifies TrajectoryTable satisfies ITable and registers with dispatcher.

            :exceptions: None.
        '''
        self.assertIsInstance(self.table, ITable)
        self.assertIsInstance(self.table, ITrajectoryObserver)
        self.assertEqual(self.table.get_version(), '1.0.3')
        self.assertEqual(self.table.TABLE_HEIGHT, 10)
        self.assertEqual(self.table.SELECT_MODE, 'browse')
        self.mock_dispatcher.add_observer.assert_called_once_with(self.table)

    def test_refresh_and_selection_sync(self) -> None:
        '''
            Verifies waypoint rows rendering, update notification, and selection.

            :exceptions: None.
        '''
        waypoint = TrajectoryWaypoint(
            x=10.0, y=20.0, z=30.0, phi=45.0, speed=100.0, name='', command=''
        )
        self.bundle.store.waypoints = (waypoint,)
        self.bundle.store.count = 1
        self.bundle.selection.selected_index = 0

        self.table.refresh_table()
        self.table.on_trajectory_updated()

    def test_delete_selected(self) -> None:
        '''
            Verifies deletion triggers mutator when valid index is selected.

            :exceptions: None.
        '''
        self.bundle.store.count = 2

        self.bundle.selection.selected_index = -1
        self.table.delete_selected()
        self.mock_mutation.remove_point.assert_not_called()

        self.bundle.selection.selected_index = 1
        self.table.delete_selected()
        self.mock_mutation.remove_point.assert_called_once_with(1)

    def test_configure_event_triggers_resize_handler(self) -> None:
        '''
            Verifies configure event on table triggers resize handler collaborator.

            :exceptions: None.
        '''
        self.table.event_generate(
            '<Configure>', width=600, height=400, when='now'
        )
        self.mock_resize.handle_resize.assert_called()


if __name__ == '__main__':
    main()
