# -*- coding: UTF-8 -*-

'''
Module
    main_content_builder_test.py
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
    Unit tests for MainContentBuilder component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.layout.main_content_builder import MainContentBuilder
from scarajectory.infrastructure.gui.layout.main_content_builder_factory import MainContentBuilderFactory
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMainContentBuilder(TestCase):
    '''
        Test cases verifying MainContentBuilder construction and orchestration.
    '''

    bundle: ScarajectoryGUIInitBundle
    root: MagicMock

    def setUp(self) -> None:
        validator = MagicMock()
        validator.bounds.speeds.default_speed = 50.0
        validator.r_min = 30.0
        validator.r_max = 270.0
        self.root = MagicMock()
        plan_bundle = PlanPipelineBundle(
            store=MagicMock(),
            selection=MagicMock(),
            mutation=MagicMock(),
            history=MagicMock(),
            dispatcher=MagicMock(),
        )
        self.bundle = ScarajectoryGUIInitBundle(
            plan=plan_bundle,
            validator=validator,
            streaming=MagicMock(),
            storage=MagicMock(),
            dsl=MagicMock(),
            connection_repository=MagicMock(),
        )

    def test_factory_creation(self) -> None:
        '''
            Verifies factory creates MainContentBuilder.
        '''
        builder = MainContentBuilderFactory.create()
        self.assertIsInstance(builder, MainContentBuilder)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(MainContentBuilderFactory.get_version(), str)

    @patch('scarajectory.infrastructure.gui.layout.main_content_builder.PanedWindow')
    def test_build_content_returns_components(
        self,
        mock_paned_cls: MagicMock,
    ) -> None:
        '''
            Verifies build_content orchestrates sub-builders and returns tuple.
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

        builder = MainContentBuilderFactory.create_with_collaborators(
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
        mock_paned.pack.assert_called_once()
        self.assertIsInstance(builder.get_version(), str)


if __name__ == '__main__':
    main()
