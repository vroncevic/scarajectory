# -*- coding: UTF-8 -*-

'''
Module
    editor_pane_builder_test.py
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
    Unit tests for EditorPaneBuilder and EditorPaneBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.layout.editor_pane_builder import EditorPaneBuilder
from scarajectory.infrastructure.gui.layout.editor_pane_builder_factory import EditorPaneBuilderFactory
from scarajectory.infrastructure.gui.layout.ieditor_pane_builder import IEditorPaneBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestEditorPaneBuilder(TestCase):
    '''
        Unit test cases verifying EditorPaneBuilder component and factory.
    '''

    mock_bundle: MagicMock

    def setUp(self) -> None:
        self.mock_bundle = MagicMock()

    def test_factory_interface(self) -> None:
        '''
            Verifies factory constructs instance implementing IEditorPaneBuilder.
        '''
        builder = EditorPaneBuilderFactory.create()
        self.assertIsInstance(builder, IEditorPaneBuilder)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(EditorPaneBuilderFactory.get_version(), str)

    @patch('scarajectory.infrastructure.gui.layout.editor_pane_builder.WaypointEditor')
    @patch('scarajectory.infrastructure.gui.layout.editor_pane_builder.PanedWindow')
    @patch('scarajectory.infrastructure.gui.layout.editor_pane_builder.Frame')
    def test_build(
        self,
        _mock_frame: MagicMock,
        _mock_paned: MagicMock,
        mock_editor_cls: MagicMock,
    ) -> None:
        '''
            Verifies build creates and returns table editor and controls.
        '''
        mock_editor = MagicMock()
        mock_editor_cls.return_value = mock_editor

        mock_controls = MagicMock()
        mock_factory = MagicMock()
        mock_factory.create.return_value = mock_controls

        builder = EditorPaneBuilder(controls_factory=mock_factory)
        parent = MagicMock()
        table, controls = builder.build(parent, bundle=self.mock_bundle)
        self.assertEqual(table, mock_editor)
        self.assertEqual(controls, mock_controls)
        self.assertIsInstance(builder.get_version(), str)


if __name__ == '__main__':
    main()
