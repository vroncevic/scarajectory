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
    Unit testing for MainContentBuilder component.
'''

from __future__ import annotations

from tkinter import BOTH
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.layout.builder import MainContentBuilder
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MainContentBuilderTestCase(TestCase):
    '''
        Unit tests for MainContentBuilder.

        It defines:

            :attributes:
                | bundle - GUI initialization dependencies bundle test fixture.
                | root - Mock Tkinter root window test fixture.
            :methods:
                | setUp - Prepares test dependencies and fixtures.
                | test_build_content_orchestrates_collaborators - Verifies build_content orchestration.
                | test_constants_and_version - Verifies ClassVar padding and version retrieval.
    '''

    bundle: GUIDependencies
    root: MagicMock

    def setUp(self) -> None:
        '''
            Prepares test dependencies and fixtures.

            :exceptions: None.
        '''
        validator = MagicMock()
        validator.bounds.speeds.default_speed = 50.0
        validator.r_min = 30.0
        validator.r_max = 270.0
        self.root = MagicMock()
        plan_bundle = PlanPipelineBundle(
            store=MagicMock(),
            selection=MagicMock(),
            point_mutator=MagicMock(),
            bulk_mutator=MagicMock(),
            history=MagicMock(),
            dispatcher=MagicMock(),
        )
        self.bundle = GUIDependencies(
            plan=plan_bundle,
            validator=validator,
            streaming=MagicMock(),
            storage=MagicMock(),
            dsl=MagicMock(),
            connection_repository=MagicMock(),
            scaralang=MagicMock(),
        )

    @patch('scarajectory.infrastructure.gui.layout.builder.PanedWindow')
    def test_build_content_orchestrates_collaborators(
        self,
        mock_paned_cls: MagicMock,
    ) -> None:
        '''
            Verifies build_content orchestrates sub-builders and returns components.

            :param mock_paned_cls: Mock class for ttk PanedWindow.
            :exceptions: None.
        '''
        mock_paned = MagicMock()
        mock_paned_cls.return_value = mock_paned

        mock_canvas = MagicMock()
        mock_canvas_builder = MagicMock()
        mock_canvas_builder.build.return_value = mock_canvas

        mock_toolbar = MagicMock()
        mock_toolbar_builder = MagicMock()
        mock_toolbar_builder.build.return_value = mock_toolbar

        mock_editor = MagicMock()
        mock_controls = MagicMock()
        mock_editor_builder = MagicMock()
        mock_editor_builder.build.return_value = (mock_editor, mock_controls)

        builder = MainContentBuilder(
            canvas_pane_builder=mock_canvas_builder,
            toolbar_builder=mock_toolbar_builder,
            editor_pane_builder=mock_editor_builder,
        )
        canvas, toolbar, editor, controls = builder.build_content(
            self.root,
            bundle=self.bundle,
        )

        self.assertEqual(canvas, mock_canvas)
        self.assertEqual(toolbar, mock_toolbar)
        self.assertEqual(editor, mock_editor)
        self.assertEqual(controls, mock_controls)
        mock_paned.pack.assert_called_once_with(
            fill=BOTH,
            expand=True,
            padx=MainContentBuilder.PAD_X,
            pady=MainContentBuilder.PAD_Y,
        )

    def test_constants_and_version(self) -> None:
        '''
            Verifies ClassVar padding constants and version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(MainContentBuilder.PAD_X, 8)
        self.assertEqual(MainContentBuilder.PAD_Y, 4)
        builder = MainContentBuilder(
            canvas_pane_builder=MagicMock(),
            toolbar_builder=MagicMock(),
            editor_pane_builder=MagicMock(),
        )
        ver = builder.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
