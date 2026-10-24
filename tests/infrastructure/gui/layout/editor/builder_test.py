# -*- coding: UTF-8 -*-

'''
Module
    builder_test.py
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
    Unit testing for EditorPaneBuilder component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.controls.panel import ControlsPanel
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.editor.editor import WaypointEditor
from scarajectory.infrastructure.gui.layout.editor.builder import EditorPaneBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EditorPaneBuilderTestCase(TestCase):
    '''
        Unit tests for EditorPaneBuilder.

        It defines:

            :methods:
                | test_build_editor_pane - Verifies editor and controls layout assembly.
                | test_get_version - Verifies version string retrieval.
    '''

    @patch('scarajectory.infrastructure.gui.layout.editor.builder.WaypointEditorFactory.create')
    @patch('scarajectory.infrastructure.gui.layout.editor.builder.PanedWindow')
    @patch('scarajectory.infrastructure.gui.layout.editor.builder.Frame')
    def test_build_editor_pane(
        self,
        mock_frame_cls: MagicMock,
        mock_paned_cls: MagicMock,
        mock_create_editor: MagicMock,
    ) -> None:
        '''
            Verifies build mounts frames, waypoint editor, and controls panel.

            :param mock_frame_cls: Mock Frame constructor.
            :param mock_paned_cls: Mock PanedWindow constructor.
            :param mock_create_editor: Mock WaypointEditorFactory.create.
            :exceptions: None.
        '''
        mock_parent = MagicMock()
        mock_right_frame = MagicMock()
        mock_ctl_frame = MagicMock()
        mock_frame_cls.side_effect = [mock_right_frame, mock_ctl_frame]

        mock_right_paned = MagicMock()
        mock_paned_cls.return_value = mock_right_paned

        mock_table = MagicMock(spec=WaypointEditor)
        mock_create_editor.return_value = mock_table

        mock_controls = MagicMock(spec=ControlsPanel)
        mock_factory = MagicMock()
        mock_factory.create.return_value = mock_controls

        mock_bundle = MagicMock(spec=GUIDependencies)

        builder = EditorPaneBuilder(controls_factory=mock_factory)
        table, controls = builder.build(mock_parent, bundle=mock_bundle)

        mock_parent.add.assert_called_once_with(
            mock_right_frame, weight=EditorPaneBuilder.WEIGHT_PANE
        )
        mock_factory.create.assert_called_once()
        mock_controls.pack.assert_called_once()
        self.assertIs(table, mock_table)
        self.assertIs(controls, mock_controls)
        self.assertIs(
            mock_create_editor.call_args.kwargs['bundle'].mutation,
            mock_bundle.plan.point_mutator,
        )


    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = EditorPaneBuilder(controls_factory=MagicMock()).get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
