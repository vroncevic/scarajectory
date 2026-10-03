# -*- coding: UTF-8 -*-

'''
Module
    canvas_pane_builder_test.py
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
    Unit tests for CanvasPaneBuilder and CanvasPaneBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.layout.canvas_pane_builder import CanvasPaneBuilder
from scarajectory.infrastructure.gui.layout.canvas_pane_builder_factory import CanvasPaneBuilderFactory
from scarajectory.infrastructure.gui.layout.icanvas_pane_builder import ICanvasPaneBuilder
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasPaneBuilder(TestCase):
    '''
        Unit test cases verifying CanvasPaneBuilder component and factory.
    '''

    bundle: ScarajectoryGUIInitBundle

    def setUp(self) -> None:
        validator = MagicMock()
        validator.bounds.default_speed = 50.0
        validator.r_min = 30.0
        validator.r_max = 270.0
        plan = PlanPipelineBundle(
            store=MagicMock(),
            selection=MagicMock(),
            mutation=MagicMock(),
            history=MagicMock(),
            dispatcher=MagicMock(),
        )
        self.bundle = ScarajectoryGUIInitBundle(
            plan=plan,
            validator=validator,
            streaming=MagicMock(),
            storage=MagicMock(),
            dsl_service=MagicMock(),
            connection_repository=MagicMock(),
        )

    def test_factory_interface(self) -> None:
        '''
            Verifies factory constructs instance implementing ICanvasPaneBuilder.
        '''
        builder = CanvasPaneBuilderFactory.create()
        self.assertIsInstance(builder, ICanvasPaneBuilder)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(CanvasPaneBuilderFactory.get_version(), str)

    @patch('scarajectory.infrastructure.gui.layout.canvas_pane_builder.Frame')
    def test_build(self, mock_frame_cls: MagicMock) -> None:
        '''
            Verifies build creates and packs canvas inside parent PanedWindow.
        '''
        mock_frame = MagicMock()
        mock_frame_cls.return_value = mock_frame

        mock_canvas = MagicMock()
        mock_factory = MagicMock()
        mock_factory.create.return_value = mock_canvas

        builder = CanvasPaneBuilder(canvas_factory=mock_factory)
        parent = MagicMock()
        settings = CanvasSettings(
            default_z=20.0,
            default_speed=50.0,
            enforce_deadzone=True,
        )
        result = builder.build(parent, bundle=self.bundle, settings=settings)
        self.assertEqual(result, mock_canvas)
        parent.add.assert_called_once_with(mock_frame, weight=3)
        mock_canvas.pack.assert_called_once()
        self.assertIsInstance(builder.get_version(), str)


if __name__ == '__main__':
    main()
