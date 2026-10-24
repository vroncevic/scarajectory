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
    Unit testing for WaypointEditorFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.editor.applier.iapplier import IWaypointEditApplier
from scarajectory.infrastructure.gui.editor.editor import WaypointEditor
from scarajectory.infrastructure.gui.editor.factory import WaypointEditorFactory
from scarajectory.infrastructure.gui.editor.ieditor import IWaypointEditor
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.table.factory import TrajectoryTableFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditorFactoryTestCase(TestCase):
    '''
        Unit tests for WaypointEditorFactory.

        It defines:

            :methods:
                | test_factory_version - Verifies factory version string.
                | test_factory_creates_instance - Verifies factory creates valid WaypointEditor.
                | test_factory_create_with_collaborators - Verifies creation with custom collaborators.
    '''

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        ver: str = WaypointEditorFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies WaypointEditorFactory instantiates valid WaypointEditor.

            :exceptions: None.
        '''
        try:
            root = Tk()
            root.withdraw()
        except Exception:
            return

        mock_bundle = MagicMock(spec=TableBundle)
        mock_bundle.store = MagicMock()
        mock_bundle.store.waypoints = []
        mock_bundle.store.count = 0
        mock_bundle.selection = MagicMock()
        mock_bundle.selection.selected_index = -1
        mock_bundle.mutation = MagicMock()
        mock_bundle.dispatcher = MagicMock()

        try:
            editor: WaypointEditor = WaypointEditorFactory.create(
                root, bundle=mock_bundle
            )
            self.assertIsInstance(editor, WaypointEditor)
            self.assertIsInstance(editor, IWaypointEditor)
        finally:
            root.destroy()

    def test_factory_create_with_collaborators(self) -> None:
        '''
            Verifies creation with explicit collaborator objects.

            :exceptions: None.
        '''
        try:
            root = Tk()
            root.withdraw()
        except Exception:
            return

        mock_bundle = MagicMock(spec=TableBundle)
        mock_bundle.store = MagicMock()
        mock_bundle.store.waypoints = []
        mock_bundle.store.count = 0
        mock_bundle.selection = MagicMock()
        mock_bundle.selection.selected_index = -1
        mock_bundle.mutation = MagicMock()
        mock_bundle.dispatcher = MagicMock()

        mock_applier = MagicMock(spec=IWaypointEditApplier)

        try:
            editor: WaypointEditor = (
                WaypointEditorFactory.create_with_collaborators(
                    root,
                    bundle=mock_bundle,
                    table_factory=TrajectoryTableFactory,
                    applier=mock_applier,
                )
            )
            self.assertIsInstance(editor, WaypointEditor)
            self.assertIsInstance(editor, IWaypointEditor)
        finally:
            root.destroy()


if __name__ == '__main__':
    main()
