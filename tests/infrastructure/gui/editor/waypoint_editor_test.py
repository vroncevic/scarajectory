# -*- coding: UTF-8 -*-

'''
Module
    waypoint_editor_test.py
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
    Unit testing for WaypointEditor component.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Entry
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.waypoint_editor import WaypointEditor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditorTestCase(TestCase):
    '''
        Unit tests for WaypointEditor widget.

        It defines:

            :methods:
                | setUp - Initializes headless Tk root and WaypointEditor.
                | tearDown - Destroys Tk root.
                | test_initialization_and_observer - Verifies observer registration.
                | test_delete_and_refresh - Verifies table delegation methods.
                | test_apply_point_edit - Verifies coordinate edit applier trigger.
                | test_on_trajectory_updated_and_selected - Verifies entry fields update.
    '''

    def setUp(self) -> None:
        '''Initializes headless Tk instance and editor widget before each test.'''
        self.root: Tk = Tk()
        self.root.withdraw()

        self.mock_store = MagicMock()
        self.mock_store.count = 0
        self.mock_store.waypoints = ()

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
        self.editor = WaypointEditor(self.root, bundle=bundle)

    def tearDown(self) -> None:
        '''Destroys Tk instance after each test.'''
        self.root.destroy()

    def test_initialization_and_observer(self) -> None:
        '''Verifies WaypointEditor registers as observer with dispatcher.'''
        self.mock_dispatcher.add_observer.assert_any_call(self.editor)

    def test_delete_and_refresh(self) -> None:
        '''Verifies delete_selected and refresh_table delegate to table.'''
        self.editor.delete_selected()
        self.editor.refresh_table()

    @patch(
        'scarajectory.infrastructure.gui.editor.waypoint_editor.'
        'WaypointEditApplier.apply_edit'
    )
    def test_apply_point_edit(self, mock_apply_edit: MagicMock) -> None:
        '''Verifies apply_point_edit invokes WaypointEditApplier.'''
        self.editor.apply_point_edit()
        self.assertTrue(mock_apply_edit.called)

    def test_on_trajectory_updated_and_selected(self) -> None:
        '''Verifies entry fields population on plan update and point selection.'''
        waypoint = Waypoint(
            x=12.5,
            y=24.0,
            z=6.5,
            phi=30.0,
            speed=75.0,
            name='WP1',
            command='MOVE',
        )
        self.mock_store.count = 1
        self.mock_store.waypoints = (waypoint,)
        self.mock_selection.selected_index = 0

        self.editor.on_trajectory_updated()

        entries = [
            w for child in self.editor.winfo_children()
            for w in child.winfo_children()
            if isinstance(w, Entry)
        ]
        self.assertEqual(len(entries), 5)
        self.assertEqual(entries[0].get(), '12.50')
        self.assertEqual(entries[1].get(), '24.00')

        self.editor.on_point_selected(0)

        self.mock_selection.selected_index = -1
        self.editor.on_trajectory_updated()


if __name__ == '__main__':
    main()
